from __future__ import annotations

import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_CSV = ROOT / "data" / "translation_it.csv"
ACCENTED_CSV = ROOT / "data" / "translation_it_accented.csv"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class TranslationDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.production = load_rows(PRODUCTION_CSV)
        cls.accented = load_rows(ACCENTED_CSV)

    def test_masters_have_matching_structure(self) -> None:
        self.assertEqual(92_954, len(self.production))
        self.assertEqual(self.accented, self.production)

    def test_sea_of_flowers_form_is_localized_and_compact(self) -> None:
        matches = [row for row in self.production if row["source_en"] == "Sea of Flowers Form"]
        self.assertEqual(10, len(matches))
        self.assertTrue(all(row["it"] == "Forma Fiorita" for row in matches))

    def test_malformed_accent_regressions_are_absent(self) -> None:
        public_text = "\n".join(row["it"] for row in self.production)
        for invalid in ("E'lite", "e'lite", "Timothe'e", "De'ja'", "Molie're", "Portugue's"):
            self.assertNotIn(invalid, public_text)

        accented_text = "\n".join(row["it"] for row in self.accented)
        self.assertNotIn("Élite", accented_text)
        self.assertNotIn("élite", accented_text)

    def test_official_accented_names_survive(self) -> None:
        text = "\n".join(row["it"] for row in self.production)
        for expected in ("Timothée", "Déjà Vu", "Molière", "Café", "Português"):
            self.assertIn(expected, text)

    def test_compact_form_labels_are_consistent(self) -> None:
        expected = {
            "Cloudmist Form": (3, "Forma Nebbiosa"),
            "Mountain Woods Form": (16, "Forma Boschiva"),
            "Mudflat Form": (3, "Forma Fangosa"),
            "Rainstorm Form": (8, "Forma Piovosa"),
            "Thunderstorm Form": (7, "Forma Tonante"),
            "Highland Form": (18, "Forma d'Altura"),
        }
        for source, (count, translation) in expected.items():
            matches = [row for row in self.production if row["source_en"] == source]
            self.assertEqual(count, len(matches))
            self.assertTrue(all(row["it"] == translation for row in matches))

    def test_confirmed_english_residues_are_translated(self) -> None:
        by_key = {row["key"]: row["it"] for row in self.production}
        self.assertEqual(by_key["1351062798"], "Sposta lotto")
        self.assertEqual(by_key["1268800582"], "Nuovo Mondo")
        self.assertEqual(by_key["1471560215"], "Vietnamita")
        text = "\n".join(by_key.values())
        for residue in (
            "Roar of the Bouldus",
            "A Chance Encounter of Waves and Song",
            "An Encounter of Tides and Song",
            "[Song of Ice and Fire]",
        ):
            self.assertNotIn(residue, text)

    def test_repaired_effect_brackets(self) -> None:
        accented_by_key = {row["key"]: row["it"] for row in self.accented}
        for key in ("1250973533", "1277595319"):
            self.assertIn("【Parassitico】", accented_by_key[key])
            self.assertIn("【Maturo】", accented_by_key[key])


if __name__ == "__main__":
    unittest.main()
