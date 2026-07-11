from __future__ import annotations

import csv
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_CSV = ROOT / "data" / "translation_it.csv"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class TranslationDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.production = load_rows(PRODUCTION_CSV)

    def test_master_has_expected_structure(self) -> None:
        self.assertEqual(92_954, len(self.production))

    def test_sea_of_flowers_form_is_localized_and_compact(self) -> None:
        matches = [row for row in self.production if row["source_en"] == "Sea of Flowers Form"]
        self.assertEqual(10, len(matches))
        self.assertTrue(all(row["it"] == "Forma Fiorita" for row in matches))

    def test_malformed_accent_regressions_are_absent(self) -> None:
        public_text = "\n".join(row["it"] for row in self.production)
        for invalid in ("E'lite", "e'lite", "Timothe'e", "De'ja'", "Molie're", "Portugue's"):
            self.assertNotIn(invalid, public_text)

        self.assertNotIn("Élite", public_text)
        self.assertNotIn("élite", public_text)

    def test_official_accented_names_survive(self) -> None:
        text = "\n".join(row["it"] for row in self.production)
        for expected in ("Timothée", "Déjà Vu", "Molière", "Café", "Português"):
            self.assertIn(expected, text)

    def test_school_principal_title_is_localized(self) -> None:
        text = "\n".join(row["it"] for row in self.production)
        self.assertIsNone(re.search(r"\bPrincipal\b", text))
        self.assertIn("Preside Oswen", text)

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
        accented_by_key = {row["key"]: row["it"] for row in self.production}
        for key in ("1250973533", "1277595319"):
            self.assertIn("【Parassitico】", accented_by_key[key])
            self.assertIn("【Maturo】", accented_by_key[key])

    def test_v035_english_audit_rows_are_fully_localized(self) -> None:
        audited = [
            row for row in self.production if row["note"] == "review_v0.3.5_english_audit"
        ]
        # Una delle 220 righe è stata nuovamente revisionata dall'audit v0.3.6.
        self.assertEqual(219, len(audited))

        english_function_words = {
            "after",
            "and",
            "available",
            "before",
            "from",
            "has",
            "have",
            "how",
            "is",
            "level",
            "new",
            "not",
            "of",
            "player",
            "select",
            "team",
            "that",
            "the",
            "this",
            "to",
            "use",
            "what",
            "when",
            "where",
            "which",
            "while",
            "will",
            "with",
            "you",
            "your",
        }
        word_pattern = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-'][A-Za-zÀ-ÖØ-öø-ÿ]+)*")
        for row in audited:
            source_words = {word.lower() for word in word_pattern.findall(row["source_en"])}
            target_words = {word.lower() for word in word_pattern.findall(row["it"])}
            retained = source_words & target_words & english_function_words
            self.assertEqual(set(), retained, f"Residuo inglese nella chiave {row['key']}")

    def test_all_solvent_answers_are_localized(self) -> None:
        by_key = {row["key"]: row["it"] for row in self.production}
        for key in ("1112835788", "1613139744"):
            self.assertEqual("Usa oli come solvente.", by_key[key])
        for key in ("1318527647", "2007572923"):
            self.assertEqual("Usa etanolo come solvente.", by_key[key])
        self.assertEqual("Usa acqua pura come solvente.", by_key["1558654226"])
        self.assertEqual("Usa acqua pura come solvente.", by_key["1755213025"])

    def test_official_zero_fallbacks_are_recovered(self) -> None:
        zero_source = [row for row in self.production if row["source_en"] == "0"]
        recovered = [row for row in zero_source if row["it"] != "0"]
        technical = {row["key"] for row in zero_source if row["it"] == "0"}

        self.assertEqual(364, len(zero_source))
        self.assertEqual(359, len(recovered))
        self.assertTrue(
            all(row["note"] == "review_v0.3.5_zero_fallback" for row in recovered)
        )
        self.assertEqual(
            {"454126242", "1113377644", "1126959664", "1660409882", "1975988662"},
            technical,
        )

    def test_instructor_dream_fallback_is_localized(self) -> None:
        by_key = {row["key"]: row["it"] for row in self.production}
        self.assertEqual(
            "L'Istruttore ci racconta cos'è successo —\n"
            "proprio così: tutto coincide con ciò che abbiamo visto in quel sogno.",
            by_key["1863202957"],
        )

    def test_confirmed_glossary_and_placeholder_residues_are_absent(self) -> None:
        text = "\n".join(row["it"] for row in self.production)
        for residue in (
            "Principal Oswen",
            "Index Unlock",
            "Carica Debuff",
            "Tutorial Prompt",
            "Astra Research Institute",
            "Purgatory Fire Wolf",
            "Missioni Objective",
        ):
            self.assertNotIn(residue, text)

    def test_remaining_cjk_is_limited_to_intentional_labels_and_expressions(self) -> None:
        cjk_pattern = re.compile(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]")
        actual = {row["key"] for row in self.production if cjk_pattern.search(row["it"])}
        self.assertEqual(
            {
                "1194793046",
                "1297606545",
                "1531108945",
                "1553225122",
                "1715234455",
                "1797965531",
                "1805564613",
                "1816045619",
                "1836013998",
                "1845754653",
                "2117181943",
            },
            actual,
        )

    def test_v036_gender_audit_regressions(self) -> None:
        by_key = {row["key"]: row["it"] for row in self.production}
        audited = [
            row for row in self.production if row["note"] == "review_v0.3.6_gender_audit"
        ]
        self.assertEqual(419, len(audited))

        self.assertEqual(
            "Uff... Sono troppo emozionata, non riesco ancora a dormire...",
            by_key["2000094316"],
        )
        self.assertEqual(
            "Dopo che racconti il sogno e ciò che hai visto, Lunara sembra sorpresa.",
            by_key["1498065011"],
        )
        self.assertIn("Lunara e io ci siamo svegliati entrambi", by_key["1351163866"])
        self.assertEqual("Ahh! Mi sento piena di felicità! Ahah!", by_key["1605896421"])
        self.assertIn("non sono sicura", by_key["1329861792"])
        self.assertEqual(
            "Sì! Non l'hai già dimenticato, vero?\n"
            "Siamo qui per indagare sul Festival della Fioritura e sul Flusso Prismana!",
            by_key["1111833223"],
        )
        self.assertIn("Sono Nicole, e con me c'è #playerName#.", by_key["1250467330"])
        self.assertEqual("Buonasera, mia cara allieva, #playerName#!", by_key["1145852353"])
        self.assertEqual("Buonasera, mio caro allievo, #playerName#!", by_key["1865663005"])
        self.assertIn("l'allievo più giovane di Loulla", by_key["1260558076"])
        self.assertIn("l'allieva più giovane di Loulla", by_key["1943916805"])
        self.assertIn("Caro allievo", by_key["1329079495"])
        self.assertIn("Cara allieva", by_key["1607383625"])

        text = "\n".join(row["it"] for row in self.production)
        self.assertNotIn("Lunara sembra sorpreso", text)


if __name__ == "__main__":
    unittest.main()
