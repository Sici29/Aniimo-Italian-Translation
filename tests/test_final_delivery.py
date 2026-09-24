import csv, hashlib, json, sys, unittest
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import aniimo_it_installer as installer

class FinalDeliveryTests(unittest.TestCase):
    def test_public_payload_has_hashes_not_original_sources(self):
        with (ROOT / "data/translation_it.csv").open(encoding="utf-8", newline="") as f:
            r=csv.DictReader(f); self.assertEqual(r.fieldnames, ["key","source_sha256","it"]); rows=list(r)
        self.assertEqual(len(rows),112207)
        self.assertEqual(len({r["key"] for r in rows}),112207)
        self.assertEqual(sum(not r["it"] for r in rows),0)
        self.assertTrue(all(len(r["source_sha256"])==64 for r in rows))

    def test_final_workflow_records_remain_byte_identical(self):
        raw=b'[{"id":1,"workflow_state":"no_translation"}]'
        with patch.object(installer,"final_text_profile",return_value=True):
            self.assertEqual(installer.mark_english_fallbacks_as_translated(raw,["1","2"]),(raw,0))

    def test_final_dates_are_not_modified(self):
        with patch.object(installer,"final_text_profile",return_value=True):
            replacements,status=installer.localized_date_replacements(None)
        self.assertEqual(replacements,{})
        self.assertFalse(status["verified_italian_dates"])

    def test_missing_native_font_is_rejected(self):
        with patch.object(installer,"final_text_profile",return_value=True), patch.object(installer,"local_manifest",return_value={"native_font_bundles":[]}):
            from types import SimpleNamespace
            result=installer.technical_compatibility_status(SimpleNamespace(game_dir=Path(".")))
        self.assertFalse(result["supported"])

    def test_source_hash_compatibility_and_unknown_text_fallback(self):
        catalog={"1":{"source_en":"","source_sha256":hashlib.sha256(b"Hello").hexdigest(),"it":"Ciao"}}
        manifest={"known_source_key_count":1,"known_source_key_sha256":installer.sha256_keys(["1"]),"known_source_content_sha256":installer.sha256_keyed_text({"1":"Hello"}),"runtime_profile":"final-native-text-only"}
        result=installer.classify_text_resources([{"key":"1","text":"Hello"}],catalog,manifest)
        self.assertTrue(result["supported"]);self.assertEqual(result["mode"],"official_exact")
        self.assertTrue(result["is_100pct_compatible"])
        result=installer.classify_text_resources([{"key":"1","text":"New"}],catalog,manifest)
        self.assertTrue(result["supported"]);self.assertEqual(result["mode"],"fallback_partial")
        self.assertFalse(result["is_100pct_compatible"])
        self.assertEqual(result["unknown_text_count"],1)
        self.assertEqual(result["modified_keys"],["1"])

    def test_final_mostly_italian_with_unknown_changes_uses_fallback(self):
        catalog={str(i):{"source_en":"English","it":"Italiano"} for i in range(100)}
        manifest={"known_source_key_count":100,"known_source_key_sha256":installer.sha256_keys(list(catalog)),"runtime_profile":"final-native-text-only"}
        records=[{"key":str(i),"text":"Italiano" if i else "Unverified"} for i in range(100)]
        result=installer.classify_text_resources(records,catalog,manifest)
        self.assertTrue(result["supported"])
        self.assertEqual(result["mode"],"fallback_partial")
        self.assertFalse(result["is_100pct_compatible"])
        self.assertEqual(result["unknown_text_count"],1)
        self.assertEqual(result["modified_keys"],["0"])

    def test_verify_archive_pair_fallback_mode(self):
        import tempfile
        import zipfile
        with tempfile.TemporaryDirectory() as td:
            temp_dir = Path(td)
            xdf = temp_dir / "LuaScripts.xdf"
            xdt = temp_dir / "LuaScripts.xdt"
            records = [{"key": "1099705801", "text": "Tempo missione scaduto."}, {"key": "9999999999", "text": "English fallback"}]
            map_bytes, bin_bytes, _ = installer.build_map_and_bin(records, {"1099705801": "Tempo missione scaduto."}, b"\x00\x00\x00\x00")
            with zipfile.ZipFile(xdf, "w") as zf:
                zf.writestr(installer.TEXT_MAP.format(lang="en"), map_bytes)
                zf.writestr(installer.COMPRESS.format(lang="en"), bin_bytes)
            xdt_data = {
                "CMDataLen": xdf.stat().st_size,
                "CMDataMD5": installer.md5_file(xdf),
                "CMEntryNum": 2,
            }
            installer.write_json(xdt, xdt_data)
            res = installer.verify_archive_pair(xdf, xdt, require_current_translation=False)
            self.assertTrue(res["translation_verified"])

    def test_build_patch_fallback_allows_changed_native_resources(self):
        import tempfile, zipfile
        with tempfile.TemporaryDirectory() as td:
            temp_dir = Path(td)
            game_dir = temp_dir / "game"
            game_dir.mkdir()
            (game_dir / "verlist.txt").write_text("3595896\n", encoding="utf-8")
            (game_dir / "md5list.txt").write_text("", encoding="utf-8")
            lua_dir = game_dir / "Aniimo_Data" / "StreamingAssets" / "cvs" / "res" / "lua"
            lua_dir.mkdir(parents=True)
            xdf = lua_dir / "LuaScripts.xdf"
            xdt = lua_dir / "LuaScripts.xdt"
            records = [
                {"key": "1099705801", "text": "Tempo missione scaduto."},
                {"key": "9999999999", "text": "New unknown string"},
            ]
            map_bytes, bin_bytes, _ = installer.build_map_and_bin(records, {"1099705801": "Tempo missione scaduto."}, b"\x00\x00\x00\x00")
            with zipfile.ZipFile(xdf, "w") as zf:
                zf.writestr(installer.TEXT_MAP.format(lang="en"), map_bytes)
                zf.writestr(installer.COMPRESS.format(lang="en"), bin_bytes)
                zf.writestr("test.lua", b"-- dummy")
            xdt_data = {
                "CMDataLen": xdf.stat().st_size,
                "CMDataMD5": installer.md5_file(xdf),
                "CMEntryNum": 3,
            }
            installer.write_json(xdt, xdt_data)
            paths = installer.resolve_paths(game_dir)
            with patch.object(installer, "technical_compatibility_status", return_value={"supported": False, "issues": ["native_font_changed"]}):
                patch_dir, stats = installer.build_patch(paths, ["en"], force=False)
            self.assertEqual(stats["version_check"]["mode"], "fallback_partial")
            self.assertIn("archive_verification", stats)

if __name__=="__main__":unittest.main()


