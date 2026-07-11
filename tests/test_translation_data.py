from __future__ import annotations

import csv
from collections import Counter
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_CSV = ROOT / "data" / "translation_it.csv"
SINGLE_LINE_NOTIFICATIONS = ROOT / "data" / "single_line_notifications.json"
FLOATING_CLUES = ROOT / "data" / "floating_clues.json"
CLUE_PANEL_INSTRUCTIONS = ROOT / "data" / "clue_panel_instructions.json"


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
        self.assertEqual(by_key["1631125284"], "Tre...")
        text = "\n".join(by_key.values())
        for residue in (
            "Roar of the Bouldus",
            "A Chance Encounter of Waves and Song",
            "An Encounter of Tides and Song",
            "[Song of Ice and Fire]",
        ):
            self.assertNotIn(residue, text)

    def test_v037_global_english_residue_audit(self) -> None:
        audited = [
            row for row in self.production if row["note"] == "review_v0.3.7_english_residue"
        ]
        self.assertEqual(151, len(audited))
        by_key = {row["key"]: row["it"] for row in self.production}
        self.assertEqual("Tre...", by_key["1631125284"])
        self.assertEqual("Maggio", by_key["1091429581"])
        self.assertEqual("Marzo", by_key["1600061307"])
        self.assertEqual("Costruisci", by_key["1192241871"])
        self.assertEqual("Configurazione", by_key["1832531669"])
        self.assertEqual("Registra", by_key["1753058341"])
        self.assertEqual("Frequenza fotogrammi", by_key["1486528807"])
        self.assertEqual("Timoroso", by_key["2131735144"])
        self.assertEqual("Palla di fango rotolante", by_key["1393914635"])
        self.assertEqual("Città Vecchia", by_key["1275514751"])
        self.assertIn("Sala dei Ricordi", by_key["1840485426"])
        self.assertEqual("Cioccolata Calda", by_key["1137332435"])
        self.assertEqual("Tempesta di Ghiaccio", by_key["1505371280"])
        self.assertEqual("Tappetino per Mouse", by_key["1528377006"])
        self.assertEqual("Chat: {0}", by_key["1629777850"])

        text = "\n".join(row["it"] for row in self.production)
        self.assertIsNone(
            re.search(r"(?i)\b(?:sigh|yawn|sniff|sob)\b", text),
            "Didascalia inglese rimasta nel testo italiano",
        )
        for residue in (
            "Three...",
            "*cough cough*",
            "open house",
            "open day",
            "max two lines",
            "<Affected by",
            "Upload completato",
            "must-have",
            "Workload",
            "Skittish",
            "Seal-off",
            "ricompensa follow",
            "community ufficiale",
            "Manager Ben",
            "Director Ling",
            "Hall of Memories",
            "Old Town",
            "Roll Out",
            "Gull Dad",
            "Gull Mom",
            "Gull Jr.",
            "Hot Cocoa",
            "Ice Burst",
            "Ice Storm",
            "Mouse Pad",
            "Hype crew",
        ):
            self.assertNotIn(residue, text)

        # I toponimi autorizzati dal glossario restano invariati.
        for key in (
            "485845125",
            "1156222793",
            "1411042912",
            "1455411606",
            "1745545241",
            "1877102031",
            "1975904113",
            "2055027862",
            "2067297521",
        ):
            self.assertEqual("Sea of Flowers", by_key[key])

    def test_repaired_effect_brackets(self) -> None:
        accented_by_key = {row["key"]: row["it"] for row in self.production}
        for key in ("1250973533", "1277595319"):
            self.assertIn("【Parassitico】", accented_by_key[key])
            self.assertIn("【Maturo】", accented_by_key[key])

    def test_v035_english_audit_rows_are_fully_localized(self) -> None:
        audited = [
            row for row in self.production if row["note"] == "review_v0.3.5_english_audit"
        ]
        # Due delle 220 righe storiche sono state revisionate di nuovo nelle versioni successive.
        self.assertEqual(218, len(audited))

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

    def test_reported_choice_fallbacks_and_branch_notice_are_natural(self) -> None:
        by_key = {row["key"]: row["it"] for row in self.production}
        self.assertEqual("Il tempismo è strano...", by_key["1409838404"])
        self.assertEqual(
            "Il suo comportamento sembra strano...", by_key["1832874807"]
        )
        notice = by_key["1166609928"]
        self.assertEqual(
            "Il Ramo di questa Fioritura è di livello basso. "
            "Vitalizzazione non disponibile.",
            notice,
        )
        self.assertLessEqual(len(notice), 80)

        mobility_notices = {
            "1693628054": "Equipaggia un Aniimo da nuoto nella scheda Esplorazione.",
            "1703220940": "Equipaggia un Aniimo volante nella scheda Esplorazione.",
            "1776315852": "Equipaggia un Aniimo da arrampicata nella scheda Esplorazione.",
        }
        for key, expected in mobility_notices.items():
            self.assertEqual(expected, by_key[key])
            self.assertLessEqual(len(by_key[key]), 80)

    def test_single_line_notifications_fit_the_toast(self) -> None:
        config = json.loads(SINGLE_LINE_NOTIFICATIONS.read_text(encoding="utf-8"))
        by_key = {row["key"]: row["it"] for row in self.production}
        tag_pattern = re.compile(r"<[^>]+>")
        limit = int(config["max_visible_characters"])
        self.assertEqual(726, len(config["keys"]))
        for key in config["keys"]:
            visible = tag_pattern.sub("", by_key[key]).replace("\n", " ")
            self.assertLessEqual(
                len(visible), limit, f"Notifica troppo lunga: {key} ({len(visible)})"
            )

    def test_shortened_notifications_preserve_markup(self) -> None:
        audited = [
            row
            for row in self.production
            if row["note"]
            in {
                "review_v0.3.7_ui_length",
                "review_v0.3.7_toast_length",
                "review_v0.3.7_clue_length",
                "review_v0.3.9_clue_bubble_wrap",
            }
        ]
        tag_pattern = re.compile(r"<[^>]+>")
        self.assertEqual(82, len(audited))
        for row in audited:
            self.assertEqual(
                Counter(tag_pattern.findall(row["source_en"])),
                Counter(tag_pattern.findall(row["it"])),
                f"Tag alterati nella notifica {row['key']}",
            )

    def test_floating_clues_fit_the_bubble(self) -> None:
        config = json.loads(FLOATING_CLUES.read_text(encoding="utf-8"))
        by_key = {row["key"]: row["it"] for row in self.production}
        tag_pattern = re.compile(r"<[^>]+>")
        line_limit = int(config["max_visible_characters_per_line"])
        max_lines = int(config["max_lines"])
        self.assertEqual(14, len(config["keys"]))
        self.assertEqual("Flutternym vivacissimo!", by_key["1299869420"])
        self.assertEqual("Fragranza misteriosa!", by_key["2018801363"])
        for key in config["keys"]:
            visible = tag_pattern.sub("", by_key[key]).replace("\n", " ")
            lines: list[str] = []
            current = ""
            for word in visible.split():
                self.assertLessEqual(
                    len(word), line_limit, f"Parola troppo larga nella bolla {key}: {word}"
                )
                candidate = word if not current else f"{current} {word}"
                if len(candidate) <= line_limit:
                    current = candidate
                else:
                    lines.append(current)
                    current = word
            if current:
                lines.append(current)
            self.assertLessEqual(
                len(lines), max_lines, f"Bolla su troppe righe: {key} ({lines})"
            )
            self.assertTrue(
                all(len(line) <= line_limit for line in lines),
                f"Riga troppo larga nella bolla {key}: {lines}",
            )

    def test_clue_panel_instructions_fit_the_header(self) -> None:
        config = json.loads(CLUE_PANEL_INSTRUCTIONS.read_text(encoding="utf-8"))
        by_key = {row["key"]: row["it"] for row in self.production}
        limit = int(config["max_visible_characters"])
        self.assertEqual(32, len(config["keys"]))
        self.assertEqual("Analizza gli indizi già trovati", by_key["1561084673"])
        self.assertEqual("Analizza gli indizi già trovati", by_key["2122732584"])
        self.assertEqual("Nome indizio (segnaposto)", by_key["1223374372"])
        self.assertEqual("Cerca altri indizi (segnaposto)", by_key["1506846237"])
        self.assertEqual("Indizio comune sbloccato: riprova", by_key["2030211050"])
        for key in config["keys"]:
            visible = re.sub(r"<[^>]+>", "", by_key[key]).replace("\n", " ")
            self.assertLessEqual(
                len(visible), limit, f"Istruzione indizi troppo lunga: {key} ({len(visible)})"
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
        # Due delle 419 righe storiche sono state nuovamente revisionate nella v0.3.7.
        self.assertEqual(417, len(audited))

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
