from __future__ import annotations

import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_CSV = ROOT / "data" / "translation_it.csv"
ACCENTED_CSV = ROOT / "data" / "translation_it_accented.csv"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class TranslationDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.public = load_rows(PUBLIC_CSV)
        cls.accented = load_rows(ACCENTED_CSV)

    def test_masters_have_matching_structure(self) -> None:
        self.assertEqual(92_954, len(self.public))
        self.assertEqual(len(self.accented), len(self.public))
        for accented, public in zip(self.accented, self.public, strict=True):
            self.assertEqual(accented["key"], public["key"])
            self.assertEqual(accented["source_en"], public["source_en"])
            self.assertEqual(accented["note"], public["note"])

    def test_sea_of_flowers_form_is_localized_and_compact(self) -> None:
        for rows in (self.accented, self.public):
            matches = [row for row in rows if row["source_en"] == "Sea of Flowers Form"]
            self.assertEqual(10, len(matches))
            self.assertTrue(all(row["it"] == "Forma Fiorita" for row in matches))

    def test_internal_apostrophe_regressions_are_absent(self) -> None:
        public_text = "\n".join(row["it"] for row in self.public)
        for invalid in ("E'lite", "e'lite", "Timothe'e", "De'ja'", "Molie're", "Portugue's"):
            self.assertNotIn(invalid, public_text)

        accented_text = "\n".join(row["it"] for row in self.accented)
        self.assertNotIn("Élite", accented_text)
        self.assertNotIn("élite", accented_text)

    def test_repaired_effect_brackets(self) -> None:
        accented_by_key = {row["key"]: row["it"] for row in self.accented}
        public_by_key = {row["key"]: row["it"] for row in self.public}
        for key in ("1250973533", "1277595319"):
            self.assertIn("【Parassitico】", accented_by_key[key])
            self.assertIn("【Maturo】", accented_by_key[key])
            self.assertIn("[Parassitico]", public_by_key[key])
            self.assertIn("[Maturo]", public_by_key[key])


if __name__ == "__main__":
    unittest.main()
