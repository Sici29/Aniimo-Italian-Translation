from __future__ import annotations

import argparse
import importlib.util
import json
import struct
import sys
import tempfile
import unittest
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


class MenuTests(unittest.TestCase):
    def test_enter_uses_recommended_install_action(self) -> None:
        with patch("builtins.input", return_value=""), patch.object(
            installer, "cmd_install", return_value=0
        ) as install:
            self.assertEqual(installer.run_menu(), 0)
        install.assert_called_once()

    def test_unknown_choice_does_not_install(self) -> None:
        with patch("builtins.input", return_value="abc"), patch.object(
            installer, "cmd_install", return_value=0
        ) as install:
            self.assertEqual(installer.run_menu(), 1)
        install.assert_not_called()


if __name__ == "__main__":
    unittest.main()
