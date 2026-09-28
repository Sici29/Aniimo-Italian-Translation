from __future__ import annotations

import importlib.util
import io
import json
import struct
import sys
import tempfile
import unittest
import zipfile
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


def language_table(rows: dict[str, str]) -> tuple[bytes, bytes]:
    """Build a (map, bin) pair the way the game stores one."""
    blob = bytearray(struct.pack("<I", 1))
    mapping: dict[str, object] = {"_count": len(rows), "_version": 1}
    for key, text in rows.items():
        encoded = text.encode("utf-8")
        mapping[key] = [len(blob), len(encoded)]
        blob.extend(encoded)
    return json.dumps(mapping).encode("utf-8"), bytes(blob)


def archive_with_slots(path: Path, slots: dict[str, dict[str, str]]) -> None:
    with zipfile.ZipFile(path, "w") as zf:
        for code, rows in slots.items():
            map_bytes, bin_bytes = language_table(rows)
            zf.writestr(installer.TEXT_MAP.format(lang=code), map_bytes)
            zf.writestr(installer.COMPRESS.format(lang=code), bin_bytes)


class LanguageSlotTableTests(unittest.TestCase):
    def test_table_covers_the_thirteen_selectable_slots_without_overlap(self) -> None:
        codes = [slot.code for slot in installer.LANGUAGE_SLOTS]
        self.assertEqual(len(codes), 13)
        self.assertEqual(len(set(codes)), len(codes))
        self.assertIn("en", codes)
        # The legacy tables carry fewer keys and never show up in the menu.
        self.assertNotIn("ja", codes)
        self.assertNotIn("ko", codes)

    def test_every_label_key_belongs_to_exactly_one_slot(self) -> None:
        seen: dict[str, str] = {}
        for slot in installer.LANGUAGE_SLOTS:
            self.assertTrue(slot.label_keys, slot.code)
            for key in slot.label_keys:
                self.assertTrue(key.isdigit(), key)
                self.assertNotIn(key, seen, f"{key} shared with {seen.get(key)}")
                seen[key] = slot.code

    def test_unknown_slot_is_rejected_with_the_list_of_valid_ones(self) -> None:
        with self.assertRaises(ValueError) as caught:
            installer.language_slot("it_IT")
        message = str(caught.exception)
        self.assertIn("it_IT", message)
        self.assertIn("pt_PT", message)

    def test_only_slots_present_in_the_archive_are_offered(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            xdf = Path(tmp) / "LuaScripts.xdf"
            archive_with_slots(xdf, {"en": {"1": "a"}, "pt_PT": {"1": "b"}})
            with zipfile.ZipFile(xdf) as zf:
                self.assertEqual(installer.archive_language_slots(zf), ["en", "pt_PT"])

    def test_a_slot_missing_its_blob_is_not_offered(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            xdf = Path(tmp) / "LuaScripts.xdf"
            with zipfile.ZipFile(xdf, "w") as zf:
                map_bytes, bin_bytes = language_table({"1": "a"})
                zf.writestr(installer.TEXT_MAP.format(lang="en"), map_bytes)
                zf.writestr(installer.COMPRESS.format(lang="en"), bin_bytes)
                # map without its companion blob: unusable, must be skipped
                zf.writestr(installer.TEXT_MAP.format(lang="fr_FR"), map_bytes)
            with zipfile.ZipFile(xdf) as zf:
                self.assertEqual(installer.archive_language_slots(zf), ["en"])


class MenuLabelTests(unittest.TestCase):
    def test_taking_over_english_keeps_the_historical_labels(self) -> None:
        self.assertEqual(installer.menu_label_overrides("en"), {})
        self.assertEqual(installer.donor_label_overrides("en"), {})

    def test_sacrificed_language_is_renamed_and_english_stays_english(self) -> None:
        overrides = installer.menu_label_overrides("pt_PT")
        self.assertEqual(overrides["1867055166"], installer.ITALIAN_LABEL)
        for key in installer.ENGLISH_SLOT.label_keys:
            self.assertEqual(overrides[key], installer.ENGLISH_LABEL_IT)

    def test_english_table_learns_where_italian_went(self) -> None:
        # The menu is drawn from the active language's table, so a player in
        # English must see "Italiano" in place of the donor language.
        donor = installer.donor_label_overrides("de_DE")
        self.assertEqual(donor, {"1109401513": installer.ITALIAN_LABEL})

    def test_detection_finds_the_slot_renamed_to_italian(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            xdf = Path(tmp) / "LuaScripts.xdf"
            archive_with_slots(xdf, {
                "en": {"1273710177": "Inglese"},
                "pt_PT": {"1867055166": installer.ITALIAN_LABEL},
                "fr_FR": {"1190882430": "Français"},
            })
            with zipfile.ZipFile(xdf) as zf:
                self.assertEqual(installer.italian_label_slots(zf), ["pt_PT"])

    def test_untouched_archive_reports_no_italian_slot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            xdf = Path(tmp) / "LuaScripts.xdf"
            archive_with_slots(xdf, {
                "en": {"1273710177": "English"},
                "pt_PT": {"1867055166": "Português"},
            })
            with zipfile.ZipFile(xdf) as zf:
                self.assertEqual(installer.italian_label_slots(zf), [])


class SlotPreferenceTests(unittest.TestCase):
    def test_manifest_default_is_honoured_and_nonsense_falls_back(self) -> None:
        with patch.object(installer, "local_manifest",
                          return_value={"default_target_language_slot": "pt_PT"}):
            self.assertEqual(installer.default_target_language_slot(), "pt_PT")
        with patch.object(installer, "local_manifest",
                          return_value={"default_target_language_slot": "klingon"}):
            self.assertEqual(installer.default_target_language_slot(), "en")
        with patch.object(installer, "local_manifest", return_value={}):
            self.assertEqual(installer.default_target_language_slot(), "en")

    def test_saved_choice_wins_over_the_manifest_default(self) -> None:
        with patch.object(installer, "load_settings", return_value={"target_slot": "fr_FR"}):
            self.assertEqual(installer.configured_target_slot(), "fr_FR")
        with patch.object(installer, "load_settings", return_value={"target_slot": "nope"}), \
                patch.object(installer, "local_manifest", return_value={}):
            self.assertEqual(installer.configured_target_slot(), "en")

    def test_saving_the_slot_keeps_the_game_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            installer.set_user_work_dir(Path(tmp))
            try:
                installer.save_game_dir(Path(tmp) / "game")
                installer.save_settings(target_slot="pt_PT")
                stored = json.loads((Path(tmp) / "settings.json").read_text(encoding="utf-8"))
            finally:
                installer.set_user_work_dir(installer.default_work_dir())
        self.assertEqual(stored["target_slot"], "pt_PT")
        self.assertIn("game", stored["game_dir"])

    def test_recorded_slot_is_ignored_for_a_different_game_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            game = Path(tmp) / "game"
            game.mkdir()
            other = Path(tmp) / "other"
            other.mkdir()
            state = {"game_dir": str(game.resolve()), "target_slot": "pt_PT"}
            with patch.object(installer, "load_installed_state", return_value=state):
                self.assertEqual(installer.recorded_target_slot(game), "pt_PT")
                self.assertIsNone(installer.recorded_target_slot(other))

    def test_recorded_slot_rejects_a_slot_that_no_longer_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            game = Path(tmp) / "game"
            game.mkdir()
            state = {"game_dir": str(game.resolve()), "target_slot": "sv_SE"}
            with patch.object(installer, "load_installed_state", return_value=state):
                self.assertIsNone(installer.recorded_target_slot(game))


class SlotSwitchGuardTests(unittest.TestCase):
    """Installing over a different slot must be refused, not silently allowed."""

    def _paths(self) -> installer.argparse.Namespace:
        return installer.argparse.Namespace(game_dir=Path("C:/game"))

    def _args(self, target: str | None) -> installer.argparse.Namespace:
        return installer.argparse.Namespace(
            game_dir=None, force=False, no_update_check=True, target=target,
            force_open=True, ignore_update=True,
        )

    def test_switching_slot_without_restoring_is_refused(self) -> None:
        with patch.object(installer, "process_running", return_value=[]), \
                patch.object(installer, "resolve_game_dir", return_value=Path("C:/game")), \
                patch.object(installer, "resolve_paths", return_value=self._paths()), \
                patch.object(installer, "pending_cvs_download", return_value={"pending": False}), \
                patch.object(installer, "detect_translation_installation",
                             return_value={"detected_slot": "pt_PT"}), \
                patch.object(installer, "backup_live") as backup:
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = installer.cmd_install(self._args("fr_FR"))
        self.assertEqual(code, 2)
        backup.assert_not_called()
        self.assertIn("Ripristina", buffer.getvalue())

    def test_reinstalling_on_the_same_slot_is_allowed(self) -> None:
        with patch.object(installer, "process_running", return_value=[]), \
                patch.object(installer, "resolve_game_dir", return_value=Path("C:/game")), \
                patch.object(installer, "resolve_paths", return_value=self._paths()), \
                patch.object(installer, "pending_cvs_download", return_value={"pending": False}), \
                patch.object(installer, "detect_translation_installation",
                             return_value={"detected_slot": "pt_PT"}), \
                patch.object(installer, "game_info_before_install", return_value={}), \
                patch.object(installer, "backup_live", side_effect=RuntimeError("reached")):
            buffer = io.StringIO()
            with redirect_stdout(buffer), self.assertRaises(RuntimeError):
                installer.cmd_install(self._args("pt_PT"))
        self.assertIn("Português", buffer.getvalue())

    def test_unknown_slot_is_refused_before_touching_the_game(self) -> None:
        with patch.object(installer, "process_running", return_value=[]), \
                patch.object(installer, "resolve_game_dir", return_value=Path("C:/game")), \
                patch.object(installer, "resolve_paths", return_value=self._paths()), \
                patch.object(installer, "pending_cvs_download", return_value={"pending": False}), \
                patch.object(installer, "backup_live") as backup:
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = installer.cmd_install(self._args("it_IT"))
        self.assertEqual(code, 2)
        backup.assert_not_called()



class PendingCvsDownloadTests(unittest.TestCase):
    """Steam updates the exe at once; cvs arrives later, from the CDN patcher."""

    def _game(self, tmp: str, steam_build: str, cache_build: str | None) -> "installer.GamePaths":
        game = Path(tmp)/"game"
        lua = game/"Aniimo_Data"/"cvs"/"res"/"lua"
        lua.mkdir(parents=True)
        (lua/"LuaScripts.xdf").write_bytes(b"")
        (lua/"LuaScripts.xdt").write_bytes(b"")
        if cache_build is not None:
            (lua/"LuaCacheVer.txt").write_text(f"1.0.{cache_build},123,abc", encoding="utf-8")
        (game/"verlist.txt").write_text(f"{steam_build},deadbeef,42", encoding="utf-8")
        return installer.resolve_paths(game)

    def test_older_lua_cache_is_reported_as_pending(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._game(tmp, "3616231", "3603741")
            result = installer.pending_cvs_download(paths)
        self.assertTrue(result["pending"])
        self.assertEqual(result["steam_build"], "3616231")
        self.assertEqual(result["stale_archives"][0]["cache_build"], "3603741")

    def test_matching_builds_are_not_pending(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._game(tmp, "3616231", "3616231")
            self.assertFalse(installer.pending_cvs_download(paths)["pending"])

    def test_missing_cache_file_is_not_pending(self) -> None:
        # Nothing to compare against is not evidence of a stale download.
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._game(tmp, "3616231", None)
            self.assertFalse(installer.pending_cvs_download(paths)["pending"])

    def test_verlist_is_read_directly_not_through_read_game_update(self) -> None:
        # The PackageManifest versions read_game_update prefers live inside cvs,
        # so during the window they report the old build and mask the mismatch.
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._game(tmp, "3616231", "3603741")
            manifest = (paths.game_dir/"Aniimo_Data"/"cvs"/"res"/"uab"/"win"/"DefaultPackage"
                        /"ManifestFiles")
            manifest.mkdir(parents=True)
            (manifest/"PackageManifest_DefaultPackage.version").write_text("3603741",
                                                                          encoding="utf-8")
            self.assertEqual(installer.read_game_update(paths.game_dir), "3603741")
            self.assertEqual(installer.steam_build_from_verlist(paths.game_dir), "3616231")
            self.assertTrue(installer.pending_cvs_download(paths)["pending"])

    def test_install_refuses_while_the_download_is_pending(self) -> None:
        pending = {"pending": True, "steam_build": "3616231",
                   "stale_archives": [{"relative_dir": "Aniimo_Data", "cache_build": "3603741"}]}
        args = installer.argparse.Namespace(
            game_dir=None, force=False, no_update_check=True, target="pt_PT",
            force_open=True, ignore_update=True,
        )
        with patch.object(installer, "process_running", return_value=[]),                 patch.object(installer, "resolve_game_dir", return_value=Path("C:/game")),                 patch.object(installer, "resolve_paths",
                             return_value=installer.argparse.Namespace(game_dir=Path("C:/game"))),                 patch.object(installer, "pending_cvs_download", return_value=pending),                 patch.object(installer, "backup_live") as backup:
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                self.assertEqual(installer.cmd_install(args), 2)
        backup.assert_not_called()
        self.assertIn("3616231", buffer.getvalue())

    def test_force_installs_anyway(self) -> None:
        pending = {"pending": True, "steam_build": "3616231",
                   "stale_archives": [{"relative_dir": "Aniimo_Data", "cache_build": "3603741"}]}
        args = installer.argparse.Namespace(
            game_dir=None, force=True, no_update_check=True, target="pt_PT",
            force_open=True, ignore_update=True,
        )
        with patch.object(installer, "process_running", return_value=[]),                 patch.object(installer, "resolve_game_dir", return_value=Path("C:/game")),                 patch.object(installer, "resolve_paths",
                             return_value=installer.argparse.Namespace(game_dir=Path("C:/game"))),                 patch.object(installer, "pending_cvs_download", return_value=pending),                 patch.object(installer, "detect_translation_installation", return_value={}),                 patch.object(installer, "game_info_before_install", return_value={}),                 patch.object(installer, "backup_live", side_effect=RuntimeError("reached")):
            with redirect_stdout(io.StringIO()), self.assertRaises(RuntimeError):
                installer.cmd_install(args)

if __name__ == "__main__":
    unittest.main()
