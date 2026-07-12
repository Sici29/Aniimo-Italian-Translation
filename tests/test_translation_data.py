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
GENDER_AUDIT_V0310 = ROOT / "data" / "gender_audit_v0.3.10.json"
QUALITY_AUDIT_V0311 = ROOT / "data" / "quality_audit_v0.3.11.json"
PUNCTUATION_AUDIT_V0312 = ROOT / "data" / "punctuation_audit_v0.3.12.json"
FLUENCY_AUDIT_V0312 = ROOT / "data" / "fluency_audit_v0.3.12.json"
DEEP_FLUENCY_AUDIT_V0312 = ROOT / "data" / "deep_fluency_audit_v0.3.12.json"
POST_EDITORIAL_AUDIT_V0312 = ROOT / "data" / "post_editorial_audit_v0.3.12.json"
DASH_AUDIT_V0313 = ROOT / "data" / "dash_audit_v0.3.13.json"
TOPONYM_AUDIT_V0313 = ROOT / "data" / "toponym_audit_v0.3.13.json"
TOPONYM_FACILITY_AUDIT_V0313 = ROOT / "data" / "toponym_facility_audit_v0.3.13.json"


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
            row
            for row in self.production
            if "review_v0.3.7_english_residue" in row["note"].split(";")
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
        self.assertEqual("Old Town", by_key["1275514751"])
        self.assertIn("Hall of Memories", by_key["1840485426"])
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
            row
            for row in self.production
            if "review_v0.3.5_english_audit" in row["note"].split(";")
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
            all(
                "review_v0.3.5_zero_fallback" in row["note"].split(";")
                for row in recovered
            )
        )
        self.assertEqual(
            {"454126242", "1113377644", "1126959664", "1660409882", "1975988662"},
            technical,
        )

    def test_instructor_dream_fallback_is_localized(self) -> None:
        by_key = {row["key"]: row["it"] for row in self.production}
        self.assertEqual(
            "L'Istruttore ci racconta cos'è successo...\n"
            "E infatti tutto coincide con ciò che abbiamo visto in quel sogno.",
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
            if any(
                marker in row["note"].split(";")
                for marker in {
                "review_v0.3.7_ui_length",
                "review_v0.3.7_toast_length",
                "review_v0.3.7_clue_length",
                "review_v0.3.9_clue_bubble_wrap",
                }
            )
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
            row
            for row in self.production
            if "review_v0.3.6_gender_audit" in row["note"].split(";")
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
        self.assertIn("Lunara e io ci siamo svegliati, quindi", by_key["1351163866"])
        self.assertEqual("Ah! Mi sento piena di felicità! Ahah!", by_key["1605896421"])
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

    def test_v0310_full_cast_gender_audit_manifest_is_applied(self) -> None:
        audit = json.loads(GENDER_AUDIT_V0310.read_text(encoding="utf-8"))
        operations = audit["operations"]
        by_key = {row["key"]: row for row in self.production}

        self.assertEqual(290, audit["speaker_count_checked"])
        self.assertEqual(7_672, audit["dialogue_attributions_checked"])
        self.assertEqual(550, audit["candidate_lines_reviewed"])
        self.assertEqual(158, len(operations))
        self.assertEqual(158, len({operation["key"] for operation in operations}))

        expected_scope_counts = {
            "female_reference": 11,
            "female_speaker": 49,
            "male_speaker": 2,
            "variable_player": 1,
            "variable_player_address": 69,
            "variable_player_group": 1,
            "variable_player_self": 25,
        }
        self.assertEqual(expected_scope_counts, Counter(op["scope"] for op in operations))

        for operation in operations:
            row = by_key[operation["key"]]
            notes = row["note"].split(";")
            self.assertIn("review_v0.3.10_full_gender_audit", notes)
            for replacement in operation["replacements"]:
                self.assertNotIn(replacement["old"], row["it"], operation["key"])
                if replacement["new"] not in row["it"]:
                    self.assertTrue(
                        "review_v0.3.12_deep_editorial" in notes
                        or any(note.startswith("review_v0.3.13_") for note in notes),
                        f"La revisione successiva non è tracciata per {operation['key']}",
                    )

    def test_v0310_named_character_gender_regressions(self) -> None:
        by_key = {row["key"]: row["it"] for row in self.production}

        self.assertIn("Sono nata qualche anno dopo il festival", by_key["1698602738"])
        self.assertIn("Fin da piccola", by_key["1617447663"])
        self.assertIn("ero nata per questo", by_key["1617447663"])
        self.assertIn("mi sono svegliata", by_key["1636136911"])
        self.assertIn("mi sono arresa", by_key["1867126519"])
        self.assertIn("sono arrivata in anticipo", by_key["1431315230"])
        self.assertIn("sono così toccata", by_key["1463105099"])
        self.assertIn("Sono arrivata fin qui e sono giunta", by_key["1526283551"])
        self.assertIn("una profumiera", by_key["1948062580"])
        self.assertIn("sono un pittore", by_key["1127303739"])
        self.assertIn("mi ha aiutato", by_key["1513612855"])

    def test_v0310_variable_player_lines_are_neutral(self) -> None:
        by_key = {row["key"]: row["it"] for row in self.production}

        self.assertEqual("Ci sono!", by_key["1121352836"])
        self.assertEqual("Ci sono!", by_key["1468043655"])
        self.assertEqual("Eccomi di nuovo!", by_key["1364683127"])
        self.assertIn("Hai riportato ferite?", by_key["1466640855"])
        self.assertIn("ti do il benvenuto a Idyll", by_key["1673724252"])
        self.assertIn("Accesso al canale vocale effettuato", by_key["2123236433"])

    def test_v0311_quality_manifest_is_fully_applied(self) -> None:
        audit = json.loads(QUALITY_AUDIT_V0311.read_text(encoding="utf-8"))
        operations = audit["operations"]
        by_key = {row["key"]: row for row in self.production}
        token_pattern = re.compile(
            r"<[^>]+>|\{[^{}]+\}|%[sdif]|#k[A-Za-z0-9_/]+#z|#player[A-Za-z0-9_]*#"
        )

        self.assertEqual(92_954, audit["master_rows_scanned"])
        self.assertEqual(audit["operation_count"], len(operations))
        self.assertEqual(len(operations), len({str(item["key"]) for item in operations}))
        self.assertGreaterEqual(len(operations), 650)

        for operation in operations:
            key = str(operation["key"])
            row = by_key[key]
            self.assertIn(
                "review_v0.3.11_full_quality_audit", row["note"].split(";"), key
            )
            if operation["new_it"] != row["it"]:
                self.assertTrue(
                    any(
                        note.startswith(("review_v0.3.12_", "review_v0.3.13_"))
                        for note in row["note"].split(";")
                    ),
                    f"La chiave {key} differisce dall'audit v0.3.11 senza una revisione successiva",
                )
            self.assertEqual(
                Counter(token_pattern.findall(operation["old_it"])),
                Counter(token_pattern.findall(operation["new_it"])),
                f"Tag o segnaposto alterati nella chiave {key}",
            )

    def test_v0311_confirmed_residues_and_slash_forms_are_absent(self) -> None:
        public_text = "\n".join(row["it"] for row in self.production)
        visible = re.sub(r"<[^>]+>", "", public_text)

        slash_pattern = re.compile(
            r"(?i)\b(?:secondo/i|volta/e|giorno/i|ora/e|stella/e|uovo/i|"
            r"colpo/i|ricevuto/i|punto/i|moneta/e|momento/i|prezioso/i|"
            r"amico/i|caro/a|quale/i|impulso/i|accessorio/i|tentativo/i)\b"
        )
        self.assertIsNone(slash_pattern.search(visible))

        for residue in (
            "Aniimology",
            "Holo-gizmo",
            "holo-gizmo",
            "Holo-gadget",
            "Sparkling",
            "Fast and Furious",
            "Gravity Pull",
            "Starbound Journey",
            "cutscene",
            "Stamina",
            "stamina",
            "ATTaccare",
            "fifteen characters",
            "streamer signature",
            "[NPC Name]",
            "Sono intelligence!",
        ):
            self.assertNotIn(residue, visible)

        self.assertIsNone(re.search(r"(?i)\bquest(?!['’])\b", visible))
        self.assertIsNone(re.search(r"(?i)\bstage\b", visible))
        self.assertIsNone(re.search(r"(?i)\bupgrade\b", visible))
        self.assertIsNone(re.search(r"(?i)\bmatchmaking\b", visible))

    def test_v0311_truncated_and_placeholder_content_is_repaired(self) -> None:
        by_key = {row["key"]: row["it"] for row in self.production}
        self.assertEqual(
            "L'Hummin stonato si nasconde quando gli altri lo sentono. "
            "Che cos'è, secondo te?",
            by_key["1973348169"],
        )
        self.assertEqual("Un dipinto", by_key["1635962688"])
        self.assertEqual("Sconfiggi", by_key["2039845645"])
        self.assertEqual("È apparso uno strano Aniimo!", by_key["2059160538"])
        self.assertIn("Esplora un dungeon emozionante", by_key["2000957290"])
        self.assertIn("Esplora un vivace dungeon", by_key["2072163332"])

    def test_v0311_player_gender_and_terminology_regressions(self) -> None:
        by_key = {row["key"]: row["it"] for row in self.production}
        self.assertIn("Vuoi ordinare?", by_key["1091328287"])
        self.assertNotIn("Pronto a ordinare", by_key["1091328287"])
        self.assertIn("ti darà ancora più coraggio", by_key["1227085316"])
        self.assertNotIn("impavido", by_key["1227085316"])
        self.assertEqual("Furia Sfrenata", by_key["1083242828"])
        self.assertEqual("Attrazione Gravitazionale", by_key["1104159043"])
        self.assertEqual("Viaggio tra le Stelle", by_key["1932764260"])
        self.assertEqual("Aspetto", by_key["1504123594"])
        self.assertEqual("Vigore attuale", by_key["1101324669"])

    def test_v0312_trailing_em_dashes_follow_italian_style(self) -> None:
        audit = json.loads(PUNCTUATION_AUDIT_V0312.read_text(encoding="utf-8"))
        marker = audit["note_marker"]
        audited = [
            row for row in self.production if marker in row["note"].split(";")
        ]
        source_final = [
            row for row in self.production if row["source_en"].rstrip().endswith("—")
        ]

        self.assertEqual(197, len(source_final))
        self.assertEqual(190, len(audited))
        self.assertTrue(all(row["it"].rstrip().endswith("...") for row in audited))
        self.assertFalse(any(row["it"].rstrip().endswith("—") for row in self.production))
        self.assertFalse(
            any("—" in row["it"] and "—" not in row["source_en"] for row in self.production)
        )
        by_key = {row["key"]: row["it"] for row in self.production}
        self.assertEqual(
            "Quella notte feci un sogno bellissimo. Mi ritrovai in un mondo pieno di colori...",
            by_key["1850841320"],
        )
        self.assertEqual(
            "L'Istruttore ci racconta cos'è successo...\n"
            "E infatti tutto coincide con ciò che abbiamo visto in quel sogno.",
            by_key["1863202957"],
        )

    def test_v0313_dialogue_dash_audit_is_applied(self) -> None:
        audit = json.loads(DASH_AUDIT_V0313.read_text(encoding="utf-8"))
        by_key = {row["key"]: row["it"] for row in self.production}
        self.assertEqual(92_954, audit["scope_rows"])
        self.assertEqual(65, audit["accepted_unique_fixes"])
        self.assertEqual(65, len(audit["entries"]))
        for entry in audit["entries"]:
            current = by_key[str(entry["key"])]
            if entry["proposed_it"] != current:
                self.assertIn(
                    "review_v0.3.13_toponym_audit",
                    next(
                        row["note"].split(";")
                        for row in self.production
                        if row["key"] == str(entry["key"])
                    ),
                )
            self.assertNotRegex(current, "[—–]")
        self.assertEqual("Io voglio...\nOh, Snowy, vieni qui!", by_key["1227953231"])
        self.assertEqual(
            "Vi serve una mano con il trasloco? \n"
            "Con le nostre ali sarà tutto molto più facile.",
            by_key["1909530372"],
        )

    def test_v0312_full_fluency_audit_is_applied(self) -> None:
        audit = json.loads(FLUENCY_AUDIT_V0312.read_text(encoding="utf-8"))
        entries = audit["entries"]
        by_key = {row["key"]: row for row in self.production}

        self.assertEqual(92_954, audit["scope_rows"])
        self.assertEqual(175, audit["selected_unique_fixes"])
        self.assertEqual(
            {
                "italian_fluency": 65,
                "literal_calques": 106,
                "tense_consistency": 4,
            },
            audit["counts"],
        )
        self.assertEqual(175, len(entries))
        self.assertEqual(175, len({str(entry["key"]) for entry in entries}))
        for entry in entries:
            key = str(entry["key"])
            row = by_key[key]
            if entry["proposed_it"] != row["it"]:
                self.assertTrue(
                    "review_v0.3.12_post_editorial" in row["note"].split(";")
                    or any(
                        note.startswith("review_v0.3.13_")
                        for note in row["note"].split(";")
                    ),
                    key,
                )
            self.assertIn(
                f"review_v0.3.12_{entry['category']}", row["note"].split(";"), key
            )

    def test_v0313_toponym_audit_is_applied(self) -> None:
        audit = json.loads(TOPONYM_AUDIT_V0313.read_text(encoding="utf-8"))
        by_key = {row["key"]: row["it"] for row in self.production}
        self.assertEqual(92_954, audit["scope_rows"])
        self.assertEqual(153, audit["accepted_unique_fixes"])
        self.assertEqual(153, len(audit["entries"]))
        for entry in audit["entries"]:
            self.assertEqual(entry["proposed_it"], by_key[str(entry["key"])])
        exact_labels = {
            "The Argent Strait": "Argent Strait",
            "Tideblossom Coast": "Tideblossom Coast",
            "Zephyrus Landbridge": "Zephyrus Landbridge",
        }
        for source, expected in exact_labels.items():
            matches = [row["it"] for row in self.production if row["source_en"] == source]
            self.assertTrue(matches, source)
            self.assertTrue(all(value == expected for value in matches), source)

        facility_audit = json.loads(
            TOPONYM_FACILITY_AUDIT_V0313.read_text(encoding="utf-8")
        )
        self.assertEqual(23, facility_audit["accepted_unique_fixes"])
        self.assertEqual(23, len(facility_audit["entries"]))
        for entry in facility_audit["entries"]:
            self.assertEqual(entry["proposed_it"], by_key[str(entry["key"])])
        hall_labels = [
            row["it"]
            for row in self.production
            if row["source_en"] == "Astra Hall of Memories"
        ]
        self.assertEqual(10, len(hall_labels))
        self.assertTrue(all(value == "Astra Hall of Memories" for value in hall_labels))

    def test_v0312_deep_editorial_audit_is_fully_applied(self) -> None:
        audit = json.loads(DEEP_FLUENCY_AUDIT_V0312.read_text(encoding="utf-8"))
        entries = audit["entries"]
        by_key = {row["key"]: row for row in self.production}

        self.assertEqual(92_954, audit["scope_rows"])
        self.assertEqual(42_637, audit["unique_source_texts_reviewed"])
        self.assertEqual(426, audit["proposals_received"])
        self.assertEqual(423, audit["accepted_unique_fixes"])
        self.assertEqual(3, audit["rejected_after_adjudication"])
        self.assertEqual(29, audit["overridden_after_adjudication"])
        self.assertEqual({"1": 77, "2": 201, "3": 145}, audit["accepted_by_block"])
        self.assertEqual(423, len(entries))
        self.assertEqual(423, len({str(entry["key"]) for entry in entries}))

        marker = audit["review_marker"]
        for entry in entries:
            key = str(entry["key"])
            row = by_key[key]
            self.assertEqual(entry["source_en"], row["source_en"], key)
            if entry["proposed_it"] != row["it"]:
                self.assertTrue(
                    "review_v0.3.12_post_editorial" in row["note"].split(";")
                    or any(
                        note.startswith("review_v0.3.13_")
                        for note in row["note"].split(";")
                    ),
                    key,
                )
            self.assertIn(marker, row["note"].split(";"), key)

        self.assertEqual(
            "Ho dimenticato le buone maniere. Mi chiamo Sorora e sono un pittore.\n"
            "Per qualche motivo sconosciuto... ho perso la memoria.",
            by_key["1127303739"]["it"],
        )
        self.assertNotIn(marker, by_key["1127303739"]["note"].split(";"))
        self.assertIn("cercare il <style=Hint_BgD>Dr. Lewis</style>", by_key["1103960172"]["it"])
        self.assertIn("cercare il Dr. Lewis", by_key["1117663681"]["it"])

    def test_v0312_deep_editorial_regressions(self) -> None:
        by_key = {row["key"]: row["it"] for row in self.production}
        self.assertEqual(
            "L'Aniimo evocato non conosce un'abilità così potente e non può imitarla...",
            by_key["1080838903"],
        )
        self.assertLessEqual(len(by_key["1080838903"]), 80)
        self.assertEqual("Mmh...? Ehm...", by_key["1292501930"])
        self.assertEqual("Eheh... Ben fatto!", by_key["1868387415"])
        self.assertIn("sono arrivata in anticipo", by_key["1431315230"])
        self.assertIn("un Ramo a Idyll", by_key["1239339132"])
        self.assertNotIn(" AM", by_key["1185180588"])
        for key, level in (
            ("1694173301", 2),
            ("1764535657", 3),
            ("2125442768", 4),
            ("1777218078", 5),
        ):
            self.assertIn("Completa la Valutazione per la Promozione", by_key[key])
            self.assertIn(f"Abilità di Livello {level}", by_key[key])

    def test_v0312_post_editorial_audit_is_fully_applied(self) -> None:
        audit = json.loads(POST_EDITORIAL_AUDIT_V0312.read_text(encoding="utf-8"))
        entries = audit["entries"]
        by_key = {row["key"]: row for row in self.production}

        self.assertEqual(92_954, audit["scope_rows"])
        self.assertEqual(422, audit["input_proposals"])
        self.assertEqual(401, audit["input_unique_keys"])
        self.assertEqual(443, audit["accepted_unique_fixes"])
        self.assertEqual(1, audit["rejected_after_adjudication"])
        self.assertEqual(5, audit["conflicts_resolved"])
        self.assertEqual(
            {
                "date_format": 22,
                "families": 16,
                "families+global": 21,
                "global": 63,
                "interjections": 295,
                "interjections+line_spacing": 2,
                "line_spacing": 1,
                "source_group": 23,
            },
            audit["counts"],
        )
        self.assertEqual(443, len(entries))
        self.assertEqual(443, len({str(entry["key"]) for entry in entries}))

        marker = audit["review_marker"]
        for entry in entries:
            key = str(entry["key"])
            if entry["proposed_it"] != by_key[key]["it"]:
                self.assertTrue(
                    any(
                        note.startswith("review_v0.3.13_")
                        for note in by_key[key]["note"].split(";")
                    ),
                    key,
                )
            self.assertIn(marker, by_key[key]["note"].split(";"), key)

        visible = "\n".join(re.sub(r"<[^>]+>", "", row["it"]) for row in self.production)
        self.assertIsNone(re.search(r"(?i)(?<![A-Za-z])(?:AM|PM)(?![A-Za-z])", visible))
        self.assertIsNone(re.search(r"(?i)\b(?:abilità|livello|talenti) personaggio\b", visible))
        self.assertNotIn("Where Gulls Sing", visible)
        self.assertNotIn("Segnaposto Nome Pet", visible)

        intentional_interjections = {
            "1097427818",
            "1255537025",
            "1229726896",
            "1431594257",
            "1444226420",
            "1324024883",
            "1412046249",
            "1543909684",
            "1701527619",
            "1399824867",
            "1619359011",
            "1801230274",
            "1805510827",
        }
        residue_pattern = re.compile(r"\b(?:Hmm|Hehe|Haha|Hahaha|Uh|Umm|Woof|Chirp|Beep|Three)\b")
        actual = {
            row["key"]
            for row in self.production
            if residue_pattern.search(re.sub(r"<[^>]+>", "", row["it"]))
        }
        self.assertEqual(intentional_interjections, actual)

    def test_v0312_aniipod_transport_wording_is_consistent(self) -> None:
        by_key = {row["key"]: row for row in self.production}
        keys = ("1138335818", "1973721313", "1982247871", "2002227621")
        for key in keys:
            self.assertIn("portala con te nel tuo Aniipod.", by_key[key]["it"], key)
            self.assertNotIn("fare un passaggio", by_key[key]["it"].lower(), key)
        self.assertEqual(
            "Snowy non sa volare...\n#playerName#, portala con te nel tuo Aniipod.",
            by_key["1982247871"]["it"],
        )


if __name__ == "__main__":
    unittest.main()
