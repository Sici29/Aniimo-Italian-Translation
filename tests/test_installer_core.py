from __future__ import annotations

import argparse
import hashlib
import io
import importlib.util
import json
import struct
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER_PATH = REPO_ROOT / "tools" / "aniimo_it_installer.py"
SPEC = importlib.util.spec_from_file_location("aniimo_it_installer", INSTALLER_PATH)
assert SPEC and SPEC.loader
installer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = installer
SPEC.loader.exec_module(installer)


class BuildMapAndBinTests(unittest.TestCase):
    def test_versions_are_synchronized_and_extra_header_bytes_survive(self) -> None:
        rows = [{"key": "2", "text": "fallback"}, {"key": "1", "text": "fallback"}]
        with patch.object(installer.time, "time", return_value=0x12345678):
            map_bytes, bin_bytes, stats = installer.build_map_and_bin(
                rows, {"1": "tradotto"}, b"\xaa\xbb\xcc\xdd\x11\x22"
            )
        mapping = json.loads(map_bytes)
        self.assertEqual(mapping["_version"], 0x12345678)
        self.assertEqual(struct.unpack("<I", bin_bytes[:4])[0], 0x12345678)
        self.assertEqual(bin_bytes[4:6], b"\x11\x22")
        self.assertEqual(stats["map_version"], stats["bin_version"])

    def test_headers_shorter_than_four_bytes_are_rejected(self) -> None:
        rows = [{"key": "1", "text": "fallback"}]
        for size in range(4):
            with self.subTest(size=size), self.assertRaises(ValueError):
                installer.build_map_and_bin(rows, {}, b"x" * size)


class RestoreTests(unittest.TestCase):
    def test_restore_removes_only_files_created_by_the_patch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            game = root / "game"
            lua_dir = game / "Aniimo_Data" / "cvs" / "res" / "lua"
            live_i18n = lua_dir / "LuaScripts" / "Data" / "I18N"
            live_i18n.mkdir(parents=True)
            (lua_dir / "LuaScripts.xdf").write_bytes(b"patched-xdf")
            (lua_dir / "LuaScripts.xdt").write_bytes(b"patched-xdt")
            (live_i18n / "Existing.json").write_text("patched", encoding="utf-8")
            (live_i18n / "NewTextMap_en.json").write_text("created", encoding="utf-8")
            (live_i18n / "OtherMod.json").write_text("keep", encoding="utf-8")

            work_dir = root / "user-work"
            backup = work_dir / "backups" / "20260711-000000"
            backup_i18n = backup / "LuaScripts" / "Data" / "I18N"
            backup_i18n.mkdir(parents=True)
            (backup / "LuaScripts.xdf").write_bytes(b"original-xdf")
            (backup / "LuaScripts.xdt").write_bytes(b"original-xdt")
            (backup_i18n / "Existing.json").write_text("original", encoding="utf-8")
            installer.write_json(backup / "backup_manifest.json", {
                "game_dir": str(game),
                "lua_dir": str(lua_dir),
                "original_i18n_files": ["Existing.json"],
                "created_i18n_files": ["NewTextMap_en.json"],
            })
            installer.write_json(work_dir / "installed_state.json", {
                "game_dir": str(game),
                "official_game_revision": "a" * 32,
                "patched_game_revision": "b" * 32,
            })

            args = argparse.Namespace(game_dir=str(game), force_open=True)
            with patch.object(installer, "USER_WORK_DIR", work_dir), patch.object(
                installer, "process_running", return_value=[]
            ):
                self.assertEqual(installer.cmd_restore(args), 0)

            self.assertEqual((lua_dir / "LuaScripts.xdf").read_bytes(), b"original-xdf")
            self.assertEqual((lua_dir / "LuaScripts.xdt").read_bytes(), b"original-xdt")
            self.assertEqual((live_i18n / "Existing.json").read_text(encoding="utf-8"), "original")
            self.assertFalse((live_i18n / "NewTextMap_en.json").exists())
            self.assertEqual((live_i18n / "OtherMod.json").read_text(encoding="utf-8"), "keep")
            self.assertFalse((work_dir / "installed_state.json").exists())


class VersionAndUpdaterTests(unittest.TestCase):
    def test_game_update_is_read_from_verlist(self) -> None:
        self.assertEqual(installer.parse_game_update("3032670,abc,8110\n"), "3032670")
        self.assertIsNone(installer.parse_game_update("invalid,abc,8110"))
        info = installer.parse_game_version_info("3032670,7113f88e39827a2d13591a55b395f1c6,8110\n")
        self.assertEqual(info, {
            "update": "3032670",
            "revision": "7113f88e39827a2d13591a55b395f1c6",
            "manifest_size": 8110,
        })

    def test_installer_asset_is_selected_by_exact_name(self) -> None:
        release = {"assets": [{"name": "notes.zip"}, {"name": installer.INSTALLER_ASSET_NAME, "id": 7}]}
        self.assertEqual(installer.find_installer_asset(release)["id"], 7)

    def test_stable_release_is_newer_than_same_beta(self) -> None:
        self.assertGreater(installer.normalize_version("v0.3.0"), installer.normalize_version("0.3.0-beta"))

    def test_download_requires_and_verifies_github_sha256(self) -> None:
        payload = b"new installer bytes"

        class Response:
            def __init__(self) -> None:
                self.position = 0

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self, size: int = -1) -> bytes:
                if self.position:
                    return b""
                self.position = len(payload)
                return payload

        asset = {
            "browser_download_url": "https://github.com/owner/repo/releases/download/v1/installer.exe",
            "digest": "sha256:" + hashlib.sha256(payload).hexdigest(),
            "size": len(payload),
        }
        with tempfile.TemporaryDirectory() as temp_dir, patch.object(
            installer.urllib.request, "urlopen", return_value=Response()
        ):
            target = Path(temp_dir) / "installer.exe"
            installer.download_update_asset(asset, target)
            self.assertEqual(target.read_bytes(), payload)

    def test_apply_update_keeps_source_and_replaces_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "downloaded.exe"
            target = root / "installed.exe"
            source.write_bytes(b"new")
            target.write_bytes(b"old")
            self.assertTrue(installer.apply_update_payload(source, target, retries=1, delay=0, launch=False))
            self.assertEqual(source.read_bytes(), b"new")
            self.assertEqual(target.read_bytes(), b"new")

    def test_updated_installer_is_relaunched_with_completion_message(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "downloaded.exe"
            target = root / "installed.exe"
            source.write_bytes(b"new")
            target.write_bytes(b"old")
            args = [installer.UPDATE_COMPLETE_COMMAND, "0.3.1-beta"]
            with patch.object(installer.subprocess, "Popen") as launched:
                installer.apply_update_payload(source, target, retries=1, delay=0, launch_args=args)
            launched.assert_called_once_with([str(target.resolve()), *args], cwd=str(target.resolve().parent))

    def test_update_completion_message_reports_versions(self) -> None:
        output = io.StringIO()
        with patch.object(installer, "local_manifest", return_value={"translation_version": "0.3.2-beta"}), patch.object(
            installer, "enable_console_colors", return_value=False
        ), redirect_stdout(output):
            installer.print_update_complete("0.3.1-beta")
        self.assertIn("AGGIORNAMENTO COMPLETATO", output.getvalue())
        self.assertIn("v0.3.1-beta", output.getvalue())
        self.assertIn("v0.3.2-beta", output.getvalue())
        self.assertIn("riavviato automaticamente", output.getvalue())

    def test_tampered_download_is_deleted_and_rejected(self) -> None:
        payload = b"tampered"

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self, size: int = -1) -> bytes:
                returned, payload_holder[0] = payload_holder[0], b""
                return returned

        payload_holder = [payload]
        asset = {
            "browser_download_url": "https://github.com/owner/repo/releases/download/v1/installer.exe",
            "digest": "sha256:" + ("0" * 64),
            "size": len(payload),
        }
        with tempfile.TemporaryDirectory() as temp_dir, patch.object(
            installer.urllib.request, "urlopen", return_value=Response()
        ):
            target = Path(temp_dir) / "installer.exe"
            with self.assertRaises(RuntimeError):
                installer.download_update_asset(asset, target)
            self.assertFalse(target.exists())
            self.assertFalse(target.with_suffix(".exe.download").exists())


class DetectionTests(unittest.TestCase):
    def test_translation_is_detected_from_actual_text_matches(self) -> None:
        translations = {str(i): f"Italiano {i}" for i in range(200)}
        installed = [{"key": str(i), "text": f"Italiano {i}"} for i in range(200)]
        original = [{"key": str(i), "text": f"English {i}"} for i in range(200)]
        self.assertTrue(installer.translation_match_status(installed, translations)["installed"])
        self.assertFalse(installer.translation_match_status(original, translations)["installed"])

    def test_saved_game_path_is_reused(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            game = root / "Aniimo" / "game"
            (game / "Aniimo_Data").mkdir(parents=True)
            work = root / "work"
            with patch.object(installer, "USER_WORK_DIR", work), patch.object(
                installer, "candidate_game_dirs", return_value=[]
            ):
                installer.save_game_dir(game)
                found, source = installer.resolve_game_dir_with_source(None)
            self.assertEqual(found, game.resolve())
            self.assertEqual(source, "salvato")

    def test_chosen_parent_folder_is_validated_and_saved(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            game = root / "Aniimo" / "game"
            (game / "Aniimo_Data").mkdir(parents=True)
            work = root / "work"
            with patch.object(installer, "USER_WORK_DIR", work), patch.object(
                installer, "choose_game_dir_windows", return_value=str(game.parent)
            ):
                selected = installer.configure_game_dir()
                settings = installer.load_settings()
            self.assertEqual(selected, game.resolve())
            self.assertEqual(Path(settings["game_dir"]), game.resolve())

    def test_status_panel_reports_path_and_installation(self) -> None:
        status = {
            "manifest": {
                "supported_game_updates": [3032670],
                "supported_game_revisions": ["7113f88e39827a2d13591a55b395f1c6"],
            },
            "game_dir": Path(r"F:\Pawprint\Aniimo\game"),
            "game_path_source": "automatico",
            "detected_game_update": "3032670",
            "detected_game_revision": "7113f88e39827a2d13591a55b395f1c6",
            "translation_installed": True,
            "text_resources_supported": True,
            "update": {"current": "0.3.2-beta", "latest": "v0.3.2-beta", "update_available": False},
        }
        output = io.StringIO()
        with redirect_stdout(output):
            installer.print_status_panel(status, colors=False)
        self.assertIn("TROVATO AUTOMATICAMENTE", output.getvalue())
        self.assertIn("INSTALLATA", output.getvalue())
        self.assertIn("VERIFICATA", output.getvalue())
        self.assertIn("Compatibilità testi        : ✓ COMPATIBILE", output.getvalue())
        self.assertIn("github.com/Sici29/Aniimo-Italian-Translation", output.getvalue())

    def test_official_revision_survives_patched_verlist(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            game = root / "game"
            game.mkdir()
            work = root / "work"
            official = "a" * 32
            patched = "b" * 32
            with patch.object(installer, "USER_WORK_DIR", work):
                installer.write_json(work / "installed_state.json", {
                    "game_dir": str(game),
                    "official_game_revision": official,
                    "patched_game_revision": patched,
                })
                result = installer.effective_game_revision(game, patched, translation_installed=True)
            self.assertEqual(result, official)

    def test_reinstall_keeps_previously_recorded_official_revision(self) -> None:
        game = Path(r"F:\Pawprint\Aniimo\game")
        official = "a" * 32
        patched = "b" * 32
        paths = installer.GamePaths(game, game / "lua", game / "lua" / "LuaScripts.xdf", game / "lua" / "LuaScripts.xdt")
        with patch.object(
            installer, "read_game_version_info", return_value={"update": "3032670", "revision": patched, "manifest_size": 8110}
        ), patch.object(installer, "detect_translation_installation", return_value={"installed": True}), patch.object(
            installer, "effective_game_revision", return_value=official
        ):
            info = installer.game_info_before_install(paths)
        self.assertEqual(info["revision"], official)

    def test_credits_open_project_github(self) -> None:
        manifest = {
            "github_project_url": "https://github.com/Sici29/Aniimo-Italian-Translation",
            "github_issues_url": "https://github.com/Sici29/Aniimo-Italian-Translation/issues",
            "support_url": "https://buymeacoffee.com/sici29",
        }
        with patch.object(installer, "local_manifest", return_value=manifest), patch(
            "builtins.input", return_value=""
        ), patch.object(installer.webbrowser, "open", return_value=True) as opened:
            self.assertEqual(installer.show_credits(), 0)
        opened.assert_called_once_with(manifest["github_project_url"])


class MenuTests(unittest.TestCase):
    def setUp(self) -> None:
        self.status = {
            "manifest": {
                "supported_game_updates": [3032670],
                "supported_game_revisions": ["7113f88e39827a2d13591a55b395f1c6"],
            },
            "game_dir": Path(r"F:\Pawprint\Aniimo\game"),
            "game_path_source": "automatico",
            "detected_game_update": "3032670",
            "detected_game_revision": "7113f88e39827a2d13591a55b395f1c6",
            "translation_installed": True,
            "text_resources_supported": True,
            "update": {"current": "0.3.2-beta", "latest": "v0.3.2-beta", "update_available": False},
        }

    def test_enter_uses_recommended_install_action(self) -> None:
        with patch("builtins.input", return_value=""), patch.object(
            installer, "cmd_install", return_value=0
        ) as install, patch.object(installer, "collect_startup_status", return_value=self.status):
            self.assertEqual(installer.run_menu(), 0)
        install.assert_called_once()

    def test_unknown_choice_does_not_install(self) -> None:
        with patch("builtins.input", return_value="abc"), patch.object(
            installer, "cmd_install", return_value=0
        ) as install, patch.object(installer, "collect_startup_status", return_value=self.status):
            self.assertEqual(installer.run_menu(), 1)
        install.assert_not_called()

    def test_available_update_is_scheduled_with_default_yes(self) -> None:
        status = dict(self.status)
        status["update"] = {
            "current": "0.3.0-beta",
            "latest": "v0.4.0-beta",
            "update_available": True,
        }
        with patch("builtins.input", return_value=""), patch.object(
            installer, "collect_startup_status", return_value=status
        ), patch.object(installer, "cmd_update", return_value=installer.UPDATE_SCHEDULED) as update:
            self.assertEqual(installer.run_menu(), installer.UPDATE_SCHEDULED)
        update.assert_called_once()


if __name__ == "__main__":
    unittest.main()
