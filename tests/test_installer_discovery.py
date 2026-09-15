"""Discovery tests use temporary fake games, never the user's installation."""
import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / "tools/aniimo_it_installer.py"
SPEC = importlib.util.spec_from_file_location("aniimo_discovery_test", SOURCE)
installer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = installer
SPEC.loader.exec_module(installer)


def fake_game(root):
    archive = root / installer.LUA_RELS[0]
    archive.mkdir(parents=True)
    (archive / installer.XDF_NAME).write_bytes(b"archive")
    (archive / installer.XDT_NAME).write_bytes(b"index")
    (root / "Aniimo.exe").write_bytes(b"not executable")
    return root


def steam_manifest(library, name="Cartella personalizzata", downloaded=100, total=100):
    steamapps = library / "steamapps"
    steamapps.mkdir(parents=True, exist_ok=True)
    (steamapps / "appmanifest_4126040.acf").write_text(
        '"AppState"\n{\n"appid" "4126040"\n"name" "Aniimo"\n'
        f'"installdir" "{name}"\n"buildid" "0"\n'
        f'"BytesToDownload" "{total}"\n"BytesDownloaded" "{downloaded}"\n}}', encoding="utf-8")
    return steamapps / "common" / name


class DiscoveryTests(unittest.TestCase):
    def test_empty_data_folder_is_not_a_ready_game(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "Aniimo_Data").mkdir()
            (root / "Aniimo.exe").write_bytes(b"stub")
            self.assertFalse(installer.looks_like_game_dir(root))

    def test_archive_without_index_is_not_ready(self):
        with tempfile.TemporaryDirectory() as temp:
            root = fake_game(Path(temp))
            (root / installer.LUA_RELS[0] / installer.XDT_NAME).unlink()
            self.assertFalse(installer.looks_like_game_dir(root))

    def test_quoted_dragged_game_exe_is_accepted(self):
        with tempfile.TemporaryDirectory() as temp:
            root = fake_game(Path(temp) / "Il mio gioco è qui")
            found, source = installer.resolve_game_dir_with_source(f'"{root / "Aniimo.exe"}"')
            self.assertEqual(found, root.resolve())
            self.assertEqual(source, "manuale")

    def test_installer_beside_game_overrides_saved_other_game(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            saved, intended = fake_game(root / "old"), fake_game(root / "new")
            with patch.object(installer, "APP_DIR", intended), patch.object(
                installer, "load_settings", return_value={"game_dir": str(saved)}
            ), patch.object(installer, "candidate_game_dirs") as search:
                found, _ = installer.resolve_game_dir_with_source(None)
            self.assertEqual(found, intended.resolve())
            search.assert_not_called()

    def test_stale_saved_folder_falls_back_to_discovery(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            current = fake_game(root / "fresh")
            with patch.object(installer, "APP_DIR", root / "desktop"), patch.object(
                installer, "load_settings", return_value={"game_dir": str(root / "gone")}
            ), patch.object(installer, "candidate_game_dirs", return_value=[current]):
                self.assertEqual(installer.resolve_game_dir(None), current.resolve())

    def test_launcher_pref_can_point_to_an_unrelated_custom_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            launcher, game = root / "Pawprint", fake_game(root / "Disco esterno/Giochi/Creature")
            (launcher / "prefs").mkdir(parents=True)
            (launcher / "prefs/worldx_global_setting.ini").write_text(
                f"[game]\nnative_game_path={game / 'Aniimo.exe'}\n", encoding="utf-8")
            self.assertEqual(installer.resolve_game_dir(str(launcher)), game.resolve())

    def test_steam_manifest_custom_install_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            lib = Path(temp)
            game = fake_game(steam_manifest(lib))
            result = installer.steam_aniimo_installations([lib])
            self.assertEqual(result[0]["path"], game)
            self.assertTrue(result[0]["files_ready"])

    def test_steam_downloaded_but_locked_preload_is_not_ready(self):
        with tempfile.TemporaryDirectory() as temp:
            lib = Path(temp)
            steam_manifest(lib)
            result = installer.steam_aniimo_installations([lib])
            self.assertTrue(result[0]["download_complete"])
            self.assertFalse(result[0]["files_ready"])

    def test_steam_incomplete_download_is_distinct(self):
        with tempfile.TemporaryDirectory() as temp:
            lib = Path(temp)
            steam_manifest(lib, downloaded=5)
            self.assertFalse(installer.steam_aniimo_installations([lib])[0]["download_complete"])

    def test_steam_manifest_path_traversal_is_ignored(self):
        with tempfile.TemporaryDirectory() as temp:
            lib = Path(temp)
            steam_manifest(lib, name="../../elsewhere")
            self.assertEqual(installer.steam_aniimo_installations([lib]), [])

    def test_custom_nested_folder_found_without_registered_path(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            game = fake_game(root / "Personalizzata/Raccolta/Gioco")
            self.assertEqual(installer.search_custom_game_dirs([root]), [game])

    def test_deep_search_has_a_directory_limit(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fake_game(root / "a/b/c")
            self.assertEqual(installer.search_custom_game_dirs([root], max_dirs=1), [])

    def test_deep_search_has_a_time_limit(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(installer.os, "scandir") as scan:
                self.assertEqual(installer.search_custom_game_dirs([Path(temp)], max_seconds=0), [])
                scan.assert_not_called()

    def test_missing_game_has_nontechnical_recovery_message(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(installer, "APP_DIR", Path(temp)), patch.object(
            installer, "load_settings", return_value={}
        ), patch.object(installer, "candidate_game_dirs", return_value=[]), patch.object(
            installer, "search_custom_game_dirs", return_value=[]
        ):
            with self.assertRaisesRegex(FileNotFoundError, "Aniimo.exe") as error:
                installer.resolve_game_dir(None)
            self.assertNotIn("--game-dir", str(error.exception))

    def test_preload_menu_does_not_offer_install_after_cancelling_folder(self):
        status = {"game_dir": None, "steam_pending": [{"download_complete": True}], "update": {}}
        output = io.StringIO()
        with (patch.object(installer, "collect_startup_status", return_value=status), patch.object(
            installer, "print_status_panel"
        ), patch("builtins.input", return_value="n"), patch.object(installer, "cmd_install") as install,
            redirect_stdout(output)):
            self.assertEqual(installer.run_menu(), 1)
        self.assertIn("Attendi lo sblocco da Steam", output.getvalue())
        install.assert_not_called()


if __name__ == "__main__":
    unittest.main()
