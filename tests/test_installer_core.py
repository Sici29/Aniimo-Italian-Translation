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

    def test_english_is_redirected_to_vietnamese_font(self) -> None:
        tree = {"entries": [{"variants": [
            {"language": 4, "fontResID": "$UI_Font_Japan.asset"},
            {"language": 5, "fontResID": installer.VIETNAMESE_FONT_RESOURCE},
        ]}]}
        self.assertTrue(installer.redirect_english_font_variant(tree))
        self.assertEqual(tree["entries"][0]["variants"][1]["language"], 2)
        self.assertFalse(installer.redirect_english_font_variant(tree))

    def test_unexpected_font_mapping_is_rejected(self) -> None:
        tree = {"entries": [{"variants": [
            {"language": 2, "fontResID": "$Some_Other_Font.asset"},
            {"language": 5, "fontResID": installer.VIETNAMESE_FONT_RESOURCE},
        ]}]}
        with self.assertRaises(ValueError):
            installer.redirect_english_font_variant(tree)

    def test_supported_font_bundle_is_found_in_game_cache(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            game = Path(temp_dir)
            digest = installer.FONT_BUNDLE_HASHES[0]
            bundle = game / installer.FONT_CACHE_RELS[0] / digest[:2] / digest / "cdata.uab"
            bundle.parent.mkdir(parents=True)
            bundle.write_bytes(b"bundle")
            self.assertEqual(installer.find_font_bundle(game), bundle)

    def test_3053563_font_bundle_is_supported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            game = Path(temp_dir)
            digest = "c3aa9ce8cbbd8c1c6f9a26b09d202ad9"
            bundle = game / installer.FONT_CACHE_RELS[0] / digest[:2] / digest / "cdata.uab"
            bundle.parent.mkdir(parents=True)
            bundle.write_bytes(b"bundle")
            self.assertIn(digest, installer.FONT_BUNDLE_HASHES)
            self.assertEqual(installer.find_font_bundle(game), bundle)

    def test_recovered_english_fallbacks_are_marked_as_translated(self) -> None:
        raw = json.dumps([10, 20]).encode("utf-8")
        updated, added = installer.mark_english_fallbacks_as_translated(
            raw, ["20", "30", "40"]
        )
        self.assertEqual(2, added)
        self.assertEqual([10, 20, 30, 40], json.loads(updated))

    def test_current_production_no_longer_needs_english_zero_fallbacks(self) -> None:
        keys = installer.recovered_english_fallback_keys()
        self.assertEqual([], keys)

    def test_dynamic_date_bytecode_is_changed_to_day_month_year(self) -> None:
        original = b"prefix" + installer.DATE_YMD_BYTECODE + b"suffix"
        patched, changed = installer.patch_dynamic_date_order(original)
        self.assertTrue(changed)
        self.assertTrue(installer.dynamic_date_is_italian(patched))
        self.assertNotIn(installer.DATE_YMD_BYTECODE, patched)
        self.assertIn(installer.DATE_DMY_BYTECODE, patched)
        repeated, changed_again = installer.patch_dynamic_date_order(patched)
        self.assertFalse(changed_again)
        self.assertEqual(patched, repeated)

    def test_unknown_dynamic_date_bytecode_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            installer.patch_dynamic_date_order(b"script non verificato")

    def test_shared_ui_date_is_changed_from_month_day_to_day_month(self) -> None:
        original = b"prefix" + installer.DATE_MDY_UI_BYTECODE + b"suffix"
        patched, changed = installer.patch_localized_date_order(original)
        self.assertTrue(changed)
        self.assertTrue(installer.localized_date_is_italian(patched))
        self.assertNotIn(installer.DATE_MDY_UI_BYTECODE, patched)
        self.assertIn(installer.DATE_DMY_UI_BYTECODE, patched)
        repeated, changed_again = installer.patch_localized_date_order(patched)
        self.assertFalse(changed_again)
        self.assertEqual(patched, repeated)

    def test_unknown_shared_ui_date_bytecode_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            installer.patch_localized_date_order(b"script non verificato")

    def test_quest_card_date_is_changed_from_year_first_to_day_first(self) -> None:
        original = b"prefix" + installer.DATE_YMD_QUEST_BYTECODE + b"suffix"
        patched, changed = installer.patch_quest_date_order(original)
        self.assertTrue(changed)
        self.assertTrue(installer.quest_date_is_italian(patched))
        self.assertNotIn(installer.DATE_YMD_QUEST_BYTECODE, patched)
        self.assertIn(installer.DATE_DMY_QUEST_BYTECODE, patched)
        repeated, changed_again = installer.patch_quest_date_order(patched)
        self.assertFalse(changed_again)
        self.assertEqual(patched, repeated)

    def test_unknown_quest_card_date_bytecode_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            installer.patch_quest_date_order(b"script non verificato")

    def test_all_visible_ui_date_patterns_are_patched_idempotently(self) -> None:
        for script_name, pairs in installer.VISIBLE_DATE_PATCHES.items():
            with self.subTest(script=script_name):
                original = b"prefix" + b"middle".join(
                    pair[0] for pair in pairs
                ) + b"suffix"
                patched, changed = installer.patch_verified_byte_pairs(
                    original, pairs, script_name
                )
                self.assertTrue(changed)
                self.assertTrue(
                    installer.verified_byte_pairs_are_applied(patched, pairs)
                )
                repeated, changed_again = installer.patch_verified_byte_pairs(
                    patched, pairs, script_name
                )
                self.assertFalse(changed_again)
                self.assertEqual(patched, repeated)

    def test_ambiguous_visible_ui_date_pattern_is_rejected(self) -> None:
        script_name, pairs = next(iter(installer.VISIBLE_DATE_PATCHES.items()))
        original = pairs[0][0]
        with self.assertRaises(ValueError):
            installer.patch_verified_byte_pairs(
                original + original, (pairs[0],), script_name
            )

    def test_cjk_countdown_units_are_replaced_without_changing_size(self) -> None:
        original = b"prefix" + installer.COUNTDOWN_CJK_PATTERN + b"suffix"
        patched, changed = installer.patch_countdown_units(original)
        self.assertTrue(changed)
        self.assertEqual(len(original), len(patched))
        self.assertTrue(installer.countdown_units_are_italian(patched))
        repeated, changed_again = installer.patch_countdown_units(patched)
        self.assertFalse(changed_again)
        self.assertEqual(patched, repeated)

    def test_ambiguous_cjk_countdown_pattern_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            installer.patch_countdown_units(
                installer.COUNTDOWN_CJK_PATTERN * 2
            )


class LuaArchiveTests(unittest.TestCase):
    def test_hot_update_overlay_stays_primary_and_all_archives_are_returned(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            game = Path(temp_dir)
            overlay = game / installer.LUA_RELS[0]
            base = game / installer.LUA_RELS[1]
            for lua_dir in (overlay, base):
                lua_dir.mkdir(parents=True)
                (lua_dir / installer.XDF_NAME).write_bytes(b"xdf")
                (lua_dir / installer.XDT_NAME).write_bytes(b"xdt")
            # A newer base timestamp must not hide the live XFS overlay.
            (base / installer.XDF_NAME).touch()

            paths = installer.resolve_paths(game)

            self.assertEqual(paths.lua_dir, overlay)
            self.assertEqual(2, len(installer.iter_lua_archives(paths)))
            self.assertEqual(
                [overlay, base],
                [archive.lua_dir for archive in installer.iter_lua_archives(paths)],
            )

    def test_patch_copy_updates_primary_and_secondary_archives(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            game = root / "game"
            overlay = game / installer.LUA_RELS[0]
            base = game / installer.LUA_RELS[1]
            archives = []
            for lua_dir in (overlay, base):
                lua_dir.mkdir(parents=True)
                xdf = lua_dir / installer.XDF_NAME
                xdt = lua_dir / installer.XDT_NAME
                xdf.write_bytes(b"old-xdf")
                xdt.write_bytes(b"old-xdt")
                archives.append(installer.LuaArchivePaths(lua_dir, xdf, xdt))
            paths = installer.GamePaths(
                game,
                overlay,
                archives[0].xdf,
                archives[0].xdt,
                tuple(archives),
            )
            patch_dir = root / "patch"
            patch_dir.mkdir()
            (patch_dir / installer.XDF_NAME).write_bytes(b"new-overlay-xdf")
            (patch_dir / installer.XDT_NAME).write_bytes(b"new-overlay-xdt")
            staged_base = installer.archive_patch_dir(paths, patch_dir, archives[1])
            staged_base.mkdir(parents=True)
            (staged_base / installer.XDF_NAME).write_bytes(b"new-base-xdf")
            (staged_base / installer.XDT_NAME).write_bytes(b"new-base-xdt")
            live_metadata = game / installer.COUNTDOWN_METADATA_REL
            live_metadata.parent.mkdir(parents=True)
            live_metadata.write_bytes(installer.COUNTDOWN_CJK_PATTERN)
            staged_metadata = (
                patch_dir
                / installer.COUNTDOWN_METADATA_PATCH_DIR
                / installer.COUNTDOWN_METADATA_REL.name
            )
            staged_metadata.parent.mkdir(parents=True)
            staged_metadata.write_bytes(installer.COUNTDOWN_IT_PATTERN)

            with patch.object(installer, "verify_archive_pair", return_value={}) as verify:
                installer.copy_patch_into_game(paths, patch_dir)

            self.assertEqual(b"new-overlay-xdf", archives[0].xdf.read_bytes())
            self.assertEqual(b"new-overlay-xdt", archives[0].xdt.read_bytes())
            self.assertEqual(b"new-base-xdf", archives[1].xdf.read_bytes())
            self.assertEqual(b"new-base-xdt", archives[1].xdt.read_bytes())
            self.assertEqual(2, verify.call_count)
            self.assertEqual(installer.COUNTDOWN_IT_PATTERN, live_metadata.read_bytes())

    def test_package_manifest_legacy_alias_keeps_using_the_overlay(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            game = root / "game"
            overlay = game / installer.LUA_RELS[0]
            base = game / installer.LUA_RELS[1]
            archives = []
            for lua_dir in (overlay, base):
                lua_dir.mkdir(parents=True)
                xdf = lua_dir / installer.XDF_NAME
                xdt = lua_dir / installer.XDT_NAME
                xdf.write_bytes(b"old-xdf")
                xdt.write_bytes(b"old-xdt")
                archives.append(installer.LuaArchivePaths(lua_dir, xdf, xdt))
            paths = installer.GamePaths(
                game, overlay, archives[0].xdf, archives[0].xdt, tuple(archives)
            )
            patch_dir = root / "patch"
            patch_dir.mkdir()
            (patch_dir / installer.XDF_NAME).write_bytes(b"patched-overlay")
            (patch_dir / installer.XDT_NAME).write_bytes(b"patched-overlay-index")
            staged_base = installer.archive_patch_dir(paths, patch_dir, archives[1])
            staged_base.mkdir(parents=True)
            (staged_base / installer.XDF_NAME).write_bytes(b"patched-base")
            (staged_base / installer.XDT_NAME).write_bytes(b"patched-base-index")
            manifest_rel = "worldx_Data/StreamingAssets/cvs/res/lua/LuaScripts.xdf"
            (game / "md5list.txt").write_text(
                f"old,1,{manifest_rel}\n", encoding="utf-8"
            )

            result = installer.update_local_manifests(paths, patch_dir)

            expected = installer.md5_file(patch_dir / installer.XDF_NAME)
            line = (patch_dir / "md5list.txt").read_text(encoding="utf-8").strip()
            self.assertEqual(f"{expected},15,{manifest_rel}", line)
            self.assertEqual([manifest_rel], result["touched"])

    def test_package_manifest_updates_legacy_runtime_metadata_alias(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            game = root / "game"
            overlay = game / installer.LUA_RELS[0]
            overlay.mkdir(parents=True)
            xdf = overlay / installer.XDF_NAME
            xdt = overlay / installer.XDT_NAME
            xdf.write_bytes(b"old-xdf")
            xdt.write_bytes(b"old-xdt")
            paths = installer.GamePaths(game, overlay, xdf, xdt)
            patch_dir = root / "patch"
            patch_dir.mkdir()
            (patch_dir / installer.XDF_NAME).write_bytes(b"patched-overlay")
            (patch_dir / installer.XDT_NAME).write_bytes(b"patched-overlay-index")
            metadata = (
                patch_dir
                / installer.COUNTDOWN_METADATA_PATCH_DIR
                / installer.COUNTDOWN_METADATA_REL.name
            )
            metadata.parent.mkdir(parents=True)
            metadata.write_bytes(installer.COUNTDOWN_IT_PATTERN)
            manifest_rel = "worldx_Data/il2cpp_data/Metadata/global-metadata.dat"
            (game / "md5list.txt").write_text(
                f"old,1,{manifest_rel}\n", encoding="utf-8"
            )

            result = installer.update_local_manifests(paths, patch_dir)

            expected = installer.md5_file(metadata)
            line = (patch_dir / "md5list.txt").read_text(encoding="utf-8").strip()
            self.assertEqual(
                f"{expected},{len(installer.COUNTDOWN_IT_PATTERN)},{manifest_rel}", line
            )
            self.assertEqual([manifest_rel], result["touched"])


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
            font_relative = Path("Aniimo_Data") / "cvs" / "font" / "cdata.uab"
            live_font = game / font_relative
            live_font.parent.mkdir(parents=True)
            live_font.write_bytes(b"patched-font")

            work_dir = root / "user-work"
            backup = work_dir / "backups" / "20260711-000000"
            backup_i18n = backup / "LuaScripts" / "Data" / "I18N"
            backup_i18n.mkdir(parents=True)
            (backup / "LuaScripts.xdf").write_bytes(b"original-xdf")
            (backup / "LuaScripts.xdt").write_bytes(b"original-xdt")
            (backup_i18n / "Existing.json").write_text("original", encoding="utf-8")
            (backup / installer.FONT_PATCH_DIR).mkdir(parents=True)
            (backup / installer.FONT_PATCH_DIR / "cdata.uab").write_bytes(b"original-font")
            installer.write_json(backup / "backup_manifest.json", {
                "game_dir": str(game),
                "lua_dir": str(lua_dir),
                "original_i18n_files": ["Existing.json"],
                "created_i18n_files": ["NewTextMap_en.json"],
                "font_bundle_relative": str(font_relative),
                "font_info_present": False,
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
            self.assertEqual(live_font.read_bytes(), b"original-font")
            self.assertFalse((work_dir / "installed_state.json").exists())

    def test_restore_recovers_every_lua_archive_from_new_backup_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            game = root / "game"
            overlay_rel = installer.LUA_RELS[0]
            base_rel = installer.LUA_RELS[1]
            overlay = game / overlay_rel
            base = game / base_rel
            for lua_dir in (overlay, base):
                lua_dir.mkdir(parents=True)
                (lua_dir / installer.XDF_NAME).write_bytes(b"patched-xdf")
                (lua_dir / installer.XDT_NAME).write_bytes(b"patched-xdt")

            work_dir = root / "user-work"
            backup = work_dir / "backups" / "20260713-230000"
            backup.mkdir(parents=True)
            (backup / installer.XDF_NAME).write_bytes(b"overlay-original-xdf")
            (backup / installer.XDT_NAME).write_bytes(b"overlay-original-xdt")
            base_backup_rel = Path("LuaArchives") / base_rel
            base_backup = backup / base_backup_rel
            base_backup.mkdir(parents=True)
            (base_backup / installer.XDF_NAME).write_bytes(b"base-original-xdf")
            (base_backup / installer.XDT_NAME).write_bytes(b"base-original-xdt")
            live_metadata = game / installer.COUNTDOWN_METADATA_REL
            live_metadata.parent.mkdir(parents=True)
            live_metadata.write_bytes(installer.COUNTDOWN_IT_PATTERN)
            metadata_backup_rel = (
                Path(installer.COUNTDOWN_METADATA_PATCH_DIR)
                / installer.COUNTDOWN_METADATA_REL.name
            )
            metadata_backup = backup / metadata_backup_rel
            metadata_backup.parent.mkdir(parents=True)
            metadata_backup.write_bytes(installer.COUNTDOWN_CJK_PATTERN)
            installer.write_json(backup / "backup_manifest.json", {
                "game_dir": str(game),
                "primary_lua_relative": str(overlay_rel),
                "lua_archives": [
                    {"relative_dir": str(overlay_rel), "backup_dir": "."},
                    {"relative_dir": str(base_rel), "backup_dir": str(base_backup_rel)},
                ],
                "created_i18n_files": [],
                "metadata_relative": str(installer.COUNTDOWN_METADATA_REL),
                "metadata_backup": str(metadata_backup_rel),
                "metadata_sha256": installer.sha256_file(metadata_backup),
            })

            args = argparse.Namespace(game_dir=str(game), force_open=True)
            with patch.object(installer, "USER_WORK_DIR", work_dir), patch.object(
                installer, "process_running", return_value=[]
            ):
                self.assertEqual(installer.cmd_restore(args), 0)

            self.assertEqual(
                b"overlay-original-xdf", (overlay / installer.XDF_NAME).read_bytes()
            )
            self.assertEqual(
                b"overlay-original-xdt", (overlay / installer.XDT_NAME).read_bytes()
            )
            self.assertEqual(b"base-original-xdf", (base / installer.XDF_NAME).read_bytes())
            self.assertEqual(b"base-original-xdt", (base / installer.XDT_NAME).read_bytes())
            self.assertEqual(installer.COUNTDOWN_CJK_PATTERN, live_metadata.read_bytes())

    def test_latest_backup_is_scoped_to_selected_game(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            work = root / "work"
            game = root / "game"
            other_game = root / "other-game"
            game.mkdir()
            other_game.mkdir()
            wanted = work / "backups" / "20260713-220000"
            newer_other = work / "backups" / "20260713-230000"
            installer.write_json(wanted / "backup_manifest.json", {"game_dir": str(game)})
            installer.write_json(
                newer_other / "backup_manifest.json", {"game_dir": str(other_game)}
            )

            with patch.object(installer, "USER_WORK_DIR", work):
                self.assertEqual(wanted, installer.latest_backup_for_game(game))

    def test_failed_live_copy_triggers_automatic_restore(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            game = root / "game"
            lua_dir = game / installer.LUA_RELS[0]
            paths = installer.GamePaths(
                game,
                lua_dir,
                lua_dir / installer.XDF_NAME,
                lua_dir / installer.XDT_NAME,
            )
            backup = root / "backup"
            patch_dir = root / "patch"
            args = argparse.Namespace(
                game_dir=str(game),
                no_update_check=True,
                ignore_update=False,
                force_open=True,
                force=False,
                target="en",
            )
            with patch.object(installer, "process_running", return_value=[]), patch.object(
                installer, "resolve_game_dir", return_value=game
            ), patch.object(installer, "resolve_paths", return_value=paths), patch.object(
                installer, "game_info_before_install", return_value={}
            ), patch.object(installer, "backup_live", return_value=backup), patch.object(
                installer, "build_patch", return_value=(patch_dir, {"languages": {}})
            ), patch.object(installer, "record_created_i18n_files"), patch.object(
                installer, "copy_patch_into_game", side_effect=OSError("copia fallita")
            ), patch.object(installer, "cmd_restore", return_value=0) as restore, patch.object(
                installer, "record_installed_state"
            ) as record:
                with self.assertRaisesRegex(RuntimeError, "backup è stato ripristinato"):
                    installer.cmd_install(args)

            restore.assert_called_once()
            record.assert_not_called()


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

    def test_hot_update_manifest_version_takes_priority(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            game = Path(temp_dir)
            (game / "verlist.txt").write_text("3032670," + "a" * 32 + ",8110\n", encoding="utf-8")
            manifest_dir = (
                game / "Aniimo_Data" / "cvs" / "res" / "uab" / "win" / "DefaultPackage" / "ManifestFiles"
            )
            manifest_dir.mkdir(parents=True)
            (manifest_dir / "PackageManifest_DefaultPackage.version").write_text("3036569", encoding="utf-8")
            info = installer.read_game_version_info(game)
        self.assertEqual(info["update"], "3036569")
        self.assertEqual(info["revision"], "a" * 32)

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
            expected_kwargs = {"cwd": str(target.resolve().parent)}
            if installer.os.name == "nt":
                expected_kwargs["creationflags"] = getattr(installer.subprocess, "CREATE_NEW_CONSOLE", 0)
            launched.assert_called_once_with([str(target.resolve()), *args], **expected_kwargs)

    def test_windows_update_restart_requests_a_visible_console(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "downloaded.exe"
            target = root / "installed.exe"
            source.write_bytes(b"new")
            target.write_bytes(b"old")
            with patch.object(installer.os, "name", "nt"), patch.object(installer.subprocess, "Popen") as launched:
                installer.apply_update_payload(source, target, retries=1, delay=0)
            self.assertEqual(
                launched.call_args.kwargs["creationflags"],
                getattr(installer.subprocess, "CREATE_NEW_CONSOLE", 0),
            )

    def test_update_completion_message_reports_versions(self) -> None:
        output = io.StringIO()
        with patch.object(installer, "local_manifest", return_value={"translation_version": "0.3.3-beta"}), patch.object(
            installer, "enable_console_colors", return_value=False
        ), redirect_stdout(output):
            installer.print_update_complete("0.3.2-beta")
        self.assertIn("AGGIORNAMENTO COMPLETATO", output.getvalue())
        self.assertIn("v0.3.2-beta", output.getvalue())
        self.assertIn("v0.3.3-beta", output.getvalue())
        self.assertIn("riavviato automaticamente", output.getvalue())

    def test_each_update_attempt_uses_a_unique_cache_file(self) -> None:
        status = {
            "asset": {"name": installer.INSTALLER_ASSET_NAME},
            "latest": "v0.3.3-beta",
            "current": "0.3.2-beta",
        }
        with patch.object(installer.sys, "frozen", True, create=True), patch.object(
            installer.os, "name", "nt"
        ), patch.object(installer.os, "getpid", return_value=1234), patch.object(
            installer.time, "time", return_value=5678.9
        ), patch.object(installer, "download_update_asset", return_value="a" * 64) as download, patch.object(
            installer.subprocess, "Popen"
        ):
            self.assertTrue(installer.schedule_self_update(status))
        destination = download.call_args.args[1]
        self.assertEqual(destination.name, "Aniimo-Italian-Translation-1234-5678900.exe")

    def test_locked_target_prompts_then_retries(self) -> None:
        args = argparse.Namespace(target_exe=r"C:\Temp\old.exe", previous_version="0.3.2-beta")
        with tempfile.TemporaryDirectory() as temp_dir, patch.object(
            installer, "USER_WORK_DIR", Path(temp_dir)
        ), patch.object(installer, "apply_update_payload", side_effect=[RuntimeError("locked"), True]) as apply, patch.object(
            installer, "prompt_close_other_installers", return_value=True
        ), patch.object(installer, "show_update_failure_message"):
            self.assertEqual(installer.cmd_apply_update(args), 0)
        self.assertEqual(apply.call_count, 2)

    def test_failed_replacement_does_not_launch_cached_exe(self) -> None:
        args = argparse.Namespace(target_exe=r"C:\Temp\old.exe", previous_version="0.3.2-beta")
        with tempfile.TemporaryDirectory() as temp_dir, patch.object(
            installer, "USER_WORK_DIR", Path(temp_dir)
        ), patch.object(installer, "apply_update_payload", side_effect=RuntimeError("locked")), patch.object(
            installer, "prompt_close_other_installers", return_value=False
        ), patch.object(installer, "show_update_failure_message") as warning, patch.object(
            installer.subprocess, "Popen"
        ) as launched:
            self.assertEqual(installer.cmd_apply_update(args), 1)
        warning.assert_called_once()
        launched.assert_not_called()

    def test_update_cache_cleanup_only_removes_installer_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            cache = work / "updates" / "v0.3.3-beta"
            cache.mkdir(parents=True)
            stale = cache / "Aniimo-Italian-Translation-123-456.exe"
            partial = cache / "Aniimo-Italian-Translation.exe.download"
            unrelated = cache / "keep.txt"
            stale.write_bytes(b"stale")
            partial.write_bytes(b"partial")
            unrelated.write_text("keep", encoding="utf-8")
            with patch.object(installer, "USER_WORK_DIR", work):
                self.assertEqual(installer.cleanup_update_cache(), 2)
            self.assertFalse(stale.exists())
            self.assertFalse(partial.exists())
            self.assertTrue(unrelated.exists())

    def test_instance_lock_permission_error_does_not_crash_installer(self) -> None:
        with patch.object(installer, "_INSTANCE_LOCK_HANDLE", None), patch.object(
            installer, "USER_WORK_DIR", Path(r"C:\Denied")
        ), patch.object(Path, "mkdir", side_effect=PermissionError("denied")):
            self.assertTrue(installer.acquire_installer_instance_lock())

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


class TextCompatibilityTests(unittest.TestCase):
    @staticmethod
    def catalog(size: int = 20) -> dict[str, dict[str, str]]:
        return {
            str(index): {
                "source_en": f"English {index}",
                "it": f"Italiano {index}",
            }
            for index in range(size)
        }

    @staticmethod
    def manifest(catalog: dict[str, dict[str, str]]) -> dict:
        keys = list(catalog)
        return {
            "known_source_key_count": len(keys),
            "known_source_key_sha256": installer.sha256_keys(keys),
        }

    @staticmethod
    def records(values: dict[str, str]) -> list[dict]:
        return [{"key": key, "text": text} for key, text in values.items()]

    def test_unseen_build_with_unchanged_official_texts_is_supported(self) -> None:
        catalog = self.catalog()
        records = self.records({key: row["source_en"] for key, row in catalog.items()})
        status = installer.check_supported(
            records, force=False, catalog=catalog, manifest=self.manifest(catalog)
        )
        self.assertTrue(status["supported"])
        self.assertEqual("official_exact", status["mode"])
        self.assertEqual(0, status["unknown_text_count"])

    def test_current_italian_translation_is_supported(self) -> None:
        catalog = self.catalog()
        records = self.records({key: row["it"] for key, row in catalog.items()})
        status = installer.check_supported(
            records, force=False, catalog=catalog, manifest=self.manifest(catalog)
        )
        self.assertTrue(status["supported"])
        self.assertEqual("italian_exact", status["mode"])

    def test_known_official_and_italian_mix_is_supported(self) -> None:
        catalog = self.catalog()
        values = {
            key: row["it"] if int(key) % 2 else row["source_en"]
            for key, row in catalog.items()
        }
        status = installer.check_supported(
            self.records(values), force=False, catalog=catalog, manifest=self.manifest(catalog)
        )
        self.assertTrue(status["supported"])
        self.assertEqual("known_mix", status["mode"])
        self.assertEqual(0, status["unknown_text_count"])

    def test_same_keys_with_a_changed_official_text_are_rejected(self) -> None:
        catalog = self.catalog()
        values = {key: row["source_en"] for key, row in catalog.items()}
        values["7"] = "Brand-new official text"
        with self.assertRaisesRegex(RuntimeError, "Testi nuovi o modificati da verificare: 1"):
            installer.check_supported(
                self.records(values),
                force=False,
                catalog=catalog,
                manifest=self.manifest(catalog),
            )
        status = installer.check_supported(
            self.records(values), force=True, catalog=catalog, manifest=self.manifest(catalog)
        )
        self.assertFalse(status["supported"])
        self.assertEqual("unknown", status["mode"])
        self.assertEqual(["7"], status["unknown_keys"])

    def test_previous_italian_translation_can_upgrade_itself(self) -> None:
        catalog = self.catalog()
        values = {key: row["it"] for key, row in catalog.items()}
        values["3"] = "Vecchia traduzione"
        status = installer.check_supported(
            self.records(values), force=False, catalog=catalog, manifest=self.manifest(catalog)
        )
        self.assertTrue(status["supported"])
        self.assertEqual("installed_translation_upgrade", status["mode"])
        self.assertAlmostEqual(0.95, status["italian_match_ratio"])

    def test_changed_key_set_is_rejected(self) -> None:
        catalog = self.catalog()
        values = {key: row["source_en"] for key, row in catalog.items()}
        values.pop("19")
        status = installer.check_supported(
            self.records(values), force=True, catalog=catalog, manifest=self.manifest(catalog)
        )
        self.assertFalse(status["supported"])
        self.assertEqual("key_mismatch", status["mode"])


class DetectionTests(unittest.TestCase):
    def test_translation_is_detected_from_actual_text_matches(self) -> None:
        translations = {str(i): f"Italiano {i}" for i in range(200)}
        installed = [{"key": str(i), "text": f"Italiano {i}"} for i in range(200)]
        previous = [{"key": str(i), "text": f"Italiano {i}"} for i in range(200)]
        previous[0]["text"] = "Versione precedente"
        original = [{"key": str(i), "text": f"English {i}"} for i in range(200)]
        current_status = installer.translation_match_status(installed, translations)
        previous_status = installer.translation_match_status(previous, translations)
        self.assertTrue(current_status["installed"])
        self.assertTrue(current_status["matches_current"])
        self.assertTrue(previous_status["installed"])
        self.assertFalse(previous_status["matches_current"])
        self.assertFalse(installer.translation_match_status(original, translations)["installed"])

    def test_recorded_translation_version_requires_the_same_game_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            game = root / "game"
            other_game = root / "other-game"
            game.mkdir()
            other_game.mkdir()
            work = root / "work"
            with patch.object(installer, "USER_WORK_DIR", work):
                installer.write_json(work / "installed_state.json", {
                    "game_dir": str(game),
                    "translation_version": "0.3.8-beta",
                })
                self.assertEqual("0.3.8-beta", installer.recorded_translation_version(game))
                self.assertIsNone(installer.recorded_translation_version(other_game))

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
                "translation_version": "0.3.11-beta",
                "supported_game_updates": [3032670],
                "supported_game_revisions": ["7113f88e39827a2d13591a55b395f1c6"],
            },
            "game_dir": Path(r"F:\Pawprint\Aniimo\game"),
            "game_path_source": "automatico",
            "detected_game_update": "3032670",
            "detected_game_revision": "7113f88e39827a2d13591a55b395f1c6",
            "translation_installed": True,
            "translation_matches_installer": False,
            "installed_translation_version": "0.3.8-beta",
            "dynamic_date_italian": False,
            "text_resources_supported": True,
            "update": {"current": "0.3.3-beta", "latest": "v0.3.3-beta", "update_available": False},
        }
        output = io.StringIO()
        with redirect_stdout(output):
            installer.print_status_panel(status, colors=False)
        panel = output.getvalue()
        self.assertIn("↑ TRADUZIONE DA AGGIORNARE", panel)
        self.assertIn("Gioco       : ✓ v3032670 compatibile (trovato automaticamente)", panel)
        self.assertIn("Traduzione  : ⚠ v0.3.8-beta installata → v0.3.11-beta disponibile", panel)
        self.assertIn("Premi Invio per aggiornarla.", panel)
        self.assertNotIn("Revisione hot update", panel)
        self.assertNotIn("Formato date dinamiche", panel)
        self.assertIn("github.com/Sici29/Aniimo-Italian-Translation", panel)

    def test_status_panel_confirms_an_exact_translation_match(self) -> None:
        status = {
            "manifest": {
                "translation_version": "0.3.11-beta",
                "supported_game_updates": [3036569],
                "supported_game_revisions": ["4eb81a98d0e3934af67064cbde06218e"],
            },
            "game_dir": Path(r"F:\Pawprint\Aniimo\game"),
            "game_path_source": "automatico",
            "detected_game_update": "3036569",
            "detected_game_revision": "4eb81a98d0e3934af67064cbde06218e",
            "translation_installed": True,
            "translation_matches_installer": True,
            "installed_translation_version": "0.3.11-beta",
            "dynamic_date_italian": True,
            "text_resources_supported": True,
            "update": {"current": "0.3.11-beta", "latest": "v0.3.11-beta", "update_available": False},
        }
        output = io.StringIO()
        with redirect_stdout(output):
            installer.print_status_panel(status, colors=False)
        panel = output.getvalue()
        self.assertIn("✓ TUTTO AGGIORNATO", panel)
        self.assertIn("Traduzione  : ✓ v0.3.11-beta installata", panel)
        self.assertIn("Non devi fare nulla.", panel)

    def test_current_hot_update_revision_is_verified(self) -> None:
        current_revision = "4eb81a98d0e3934af67064cbde06218e"
        status = {
            "manifest": {
                "supported_game_updates": [3032670, 3036569],
                "supported_game_revisions": [
                    "7113f88e39827a2d13591a55b395f1c6",
                    current_revision,
                ],
            },
            "game_dir": Path(r"F:\Pawprint\Aniimo\game"),
            "game_path_source": "automatico",
            "detected_game_update": "3036569",
            "detected_game_revision": current_revision,
            "translation_installed": True,
            "text_resources_supported": True,
            "update": {
                "current": "0.3.8-beta",
                "latest": "v0.3.8-beta",
                "update_available": False,
            },
        }
        output = io.StringIO()
        with redirect_stdout(output):
            installer.print_technical_status(status, colors=False)
        panel = output.getvalue()
        self.assertIn(current_revision, panel)
        self.assertIn("Testi compatibili  : sì", panel)

    def test_status_panel_explains_a_new_game_update_plainly(self) -> None:
        status = {
            "manifest": {
                "translation_version": "0.3.13-beta",
                "supported_game_updates": [3032670, 3036569],
                "supported_game_revisions": [],
            },
            "game_dir": Path(r"F:\Pawprint\Aniimo\game"),
            "game_path_source": "automatico",
            "detected_game_update": "3048640",
            "detected_game_revision": "87eaffe8c13ec791e4348298ca6e5aa0",
            "translation_installed": False,
            "translation_matches_installer": False,
            "installed_translation_version": None,
            "dynamic_date_italian": False,
            "text_resources_supported": False,
            "update": {"current": "0.3.13-beta", "latest": "v0.3.13-beta", "update_available": False},
        }
        output = io.StringIO()
        with redirect_stdout(output):
            installer.print_status_panel(status, colors=False)
        panel = output.getvalue()
        self.assertIn("⚠ ANIIMO È STATO AGGIORNATO", panel)
        self.assertIn("La versione 3048640 richiede una traduzione aggiornata.", panel)
        self.assertIn("Gioco       : ⚠ v3048640 da verificare", panel)
        self.assertIn("Controlla gli aggiornamenti dell'installer prima di installare.", panel)
        self.assertNotIn("87eaffe8c13e", panel)

    def test_status_panel_blocks_changed_technical_resources(self) -> None:
        status = {
            "manifest": {
                "translation_version": "0.3.17-beta",
                "supported_game_updates": [3053563],
                "supported_game_revisions": [],
            },
            "game_dir": Path(r"F:\Pawprint\Aniimo\game"),
            "game_path_source": "automatico",
            "detected_game_update": "3059000",
            "detected_game_revision": "abc",
            "translation_installed": False,
            "translation_matches_installer": False,
            "installed_translation_version": None,
            "dynamic_date_italian": False,
            "text_resources_supported": True,
            "technical_resources_supported": False,
            "game_resources_supported": False,
            "update": {"current": "0.3.17-beta", "latest": "v0.3.17-beta", "update_available": False},
        }
        output = io.StringIO()
        with redirect_stdout(output):
            installer.print_status_panel(status, colors=False)
        panel = output.getvalue()
        self.assertIn("⚠ FILE DEL GIOCO DA VERIFICARE", panel)
        self.assertIn("I testi sono compatibili, ma un componente tecnico è cambiato o manca.", panel)
        self.assertIn("Gioco       : ⚠ v3059000 da verificare", panel)

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
            "update": {"current": "0.3.3-beta", "latest": "v0.3.3-beta", "update_available": False},
        }

    def test_enter_uses_recommended_install_action(self) -> None:
        with patch("builtins.input", return_value=""), patch.object(
            installer, "cmd_install", return_value=0
        ) as install, patch.object(installer, "collect_startup_status", return_value=self.status):
            self.assertEqual(installer.run_menu(), 0)
        install.assert_called_once()
        self.assertEqual(install.call_args.args[0].target, "en")

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

    def test_second_installer_window_is_blocked_before_menu(self) -> None:
        with patch.object(installer.sys, "argv", ["installer.exe"]), patch.object(
            installer, "acquire_installer_instance_lock", return_value=False
        ), patch.object(installer, "pause_if_needed"), patch.object(installer, "run_menu") as menu:
            self.assertEqual(installer.main(), 4)
        menu.assert_not_called()


if __name__ == "__main__":
    unittest.main()
