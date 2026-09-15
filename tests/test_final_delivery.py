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
        self.assertEqual(len(rows),112065)
        self.assertEqual(len({r["key"] for r in rows}),112065)
        self.assertEqual(sum(not r["it"] for r in rows),124)
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

    def test_source_hash_compatibility_and_unknown_text_rejection(self):
        catalog={"1":{"source_en":"","source_sha256":hashlib.sha256(b"Hello").hexdigest(),"it":"Ciao"}}
        manifest={"known_source_key_count":1,"known_source_key_sha256":installer.sha256_keys(["1"]),"known_source_content_sha256":installer.sha256_keyed_text({"1":"Hello"}),"runtime_profile":"final-native-text-only"}
        result=installer.classify_text_resources([{"key":"1","text":"Hello"}],catalog,manifest)
        self.assertTrue(result["supported"]);self.assertEqual(result["mode"],"official_exact")
        result=installer.classify_text_resources([{"key":"1","text":"New"}],catalog,manifest)
        self.assertFalse(result["supported"])

    def test_final_mostly_italian_does_not_allow_unknown_changes(self):
        catalog={str(i):{"source_en":"English","it":"Italiano"} for i in range(100)}
        manifest={"known_source_key_count":100,"known_source_key_sha256":installer.sha256_keys(list(catalog)),"runtime_profile":"final-native-text-only"}
        records=[{"key":str(i),"text":"Italiano" if i else "Unverified"} for i in range(100)]
        self.assertFalse(installer.classify_text_resources(records,catalog,manifest)["supported"])

if __name__=="__main__":unittest.main()

