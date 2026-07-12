#!/usr/bin/env python3
"""Extract Aniimo dialogue attribution and flag Italian gender agreements.

The localization table stores speaker names and dialogue text under independent
keys.  ``pmdata.bin`` is therefore the authoritative bridge between a line and
the NPC that speaks it.  This tool makes that relationship auditable and emits
a deterministic JSON inventory that can be reviewed or used by regression
tests.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import struct
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


PMDATA_MEMBER = "xfs/luascripts/Common/Data/pmdata.bin"
PMDATA_RECORD_MARKER = 16_171_863
RECORD = struct.Struct("<IIIII")

# Terms that can carry the gender of the speaker in first-person Italian.
# The report deliberately over-selects: a human reviewer must reject terms that
# refer to the player, an Aniimo, or another character.
GENDERED_WORD = re.compile(
    r"\b(?:"
    r"nato|nata|nati|nate|entrato|entrata|entrati|entrate|"
    r"passato|passata|passati|passate|tornato|tornata|tornati|tornate|"
    r"rimasto|rimasta|rimasti|rimaste|andato|andata|andati|andate|"
    r"arrivato|arrivata|arrivati|arrivate|venuto|venuta|venuti|venute|"
    r"uscito|uscita|usciti|uscite|caduto|caduta|caduti|cadute|"
    r"salito|salita|saliti|salite|sceso|scesa|scesi|scese|"
    r"fatto|fatta|fatti|fatte|detto|detta|detti|dette|"
    r"scelto|scelta|scelti|scelte|preso|presa|presi|prese|"
    r"ripreso|ripresa|ripresi|riprese|arreso|arresa|arresi|arrese|"
    r"deciso|decisa|decisi|decise|convinto|convinta|convinti|convinte|"
    r"sicuro|sicura|sicuri|sicure|pronto|pronta|pronti|pronte|"
    r"stanco|stanca|stanchi|stanche|sorpreso|sorpresa|sorpresi|sorprese|"
    r"spaventato|spaventata|spaventati|spaventate|preoccupato|preoccupata|"
    r"preoccupati|preoccupate|confuso|confusa|confusi|confuse|"
    r"emozionato|emozionata|emozionati|emozionate|"
    r"fortunato|fortunata|fortunati|fortunate|"
    r"orgoglioso|orgogliosa|orgogliosi|orgogliose|"
    r"contento|contenta|contenti|contente|"
    r"bravo|brava|bravi|brave|capace|capaci|"
    r"solo|sola|soli|sole|vecchio|vecchia|vecchi|vecchie|"
    r"nuovo|nuova|nuovi|nuove|piccolo|piccola|piccoli|piccole|"
    r"un\s+profumiere|una\s+profumiera|un\s+istruttore|un['’]\s*istruttrice"
    r")\b",
    re.IGNORECASE,
)

# First-person signals keep the candidate set useful without claiming that
# every adjective in a speaker's line describes the speaker.
FIRST_PERSON = re.compile(
    r"\b(?:io|sono|ero|sar[oò]|sarei|fossi|mi|me|mio|mia|miei|mie|"
    r"sono\s+stat[oaie]|mi\s+sono|ho|avevo|avr[oò]|potrei|vorrei)\b",
    re.IGNORECASE,
)


def load_master(path: Path) -> tuple[list[dict[str, str]], dict[int, dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows, {int(row["key"]): row for row in rows}


def load_jsonl(path: Path | None) -> dict[int, str]:
    if path is None or not path.exists():
        return {}
    result: dict[int, str] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            item = json.loads(line)
            result[int(item["key"])] = item["text"]
    return result


def load_pmdata(path: Path) -> bytes:
    if path.suffix.lower() == ".bin":
        return path.read_bytes()
    with zipfile.ZipFile(path) as archive:
        names = {name.lower(): name for name in archive.namelist()}
        member = names.get(PMDATA_MEMBER.lower())
        if member is None:
            raise FileNotFoundError(f"{PMDATA_MEMBER} non presente in {path}")
        return archive.read(member)


def iter_dialogue_records(data: bytes) -> Iterable[tuple[int, int, int]]:
    """Yield ``(record_offset, text_key, speaker_key)`` from pmdata."""

    marker = struct.pack("<I", PMDATA_RECORD_MARKER)
    cursor = 0
    while True:
        marker_offset = data.find(marker, cursor)
        if marker_offset < 0:
            return
        cursor = marker_offset + 1
        record_offset = marker_offset - 12
        if record_offset < 0 or record_offset + RECORD.size > len(data):
            continue
        _flags, text_key, speaker_key, constant, self_pointer = RECORD.unpack_from(
            data, record_offset
        )
        if constant != PMDATA_RECORD_MARKER or self_pointer != record_offset:
            continue
        yield record_offset, text_key, speaker_key


def build_inventory(
    data: bytes,
    by_key: dict[int, dict[str, str]],
    ru: dict[int, str],
    ja: dict[int, str],
) -> dict[str, object]:
    lines_by_speaker: dict[str, set[int]] = defaultdict(set)
    speaker_keys: dict[str, set[int]] = defaultdict(set)
    attribution_keys: dict[tuple[str, int], set[int]] = defaultdict(set)
    record_count = 0

    for _offset, text_key, speaker_key in iter_dialogue_records(data):
        text_row = by_key.get(text_key)
        speaker_row = by_key.get(speaker_key)
        if text_row is None or speaker_row is None:
            continue
        speaker = speaker_row["source_en"].strip()
        if not speaker:
            continue
        record_count += 1
        lines_by_speaker[speaker].add(text_key)
        speaker_keys[speaker].add(speaker_key)
        attribution_keys[(speaker, text_key)].add(speaker_key)

    speakers: list[dict[str, object]] = []
    candidates: list[dict[str, object]] = []
    for speaker in sorted(lines_by_speaker, key=str.casefold):
        keys = sorted(lines_by_speaker[speaker])
        name_keys = sorted(speaker_keys[speaker])
        speakers.append(
            {
                "speaker": speaker,
                "speaker_keys": name_keys,
                "ru_names": sorted({ru[key] for key in name_keys if key in ru}),
                "ja_names": sorted({ja[key] for key in name_keys if key in ja}),
                "dialogue_key_count": len(keys),
                "dialogue_keys": keys,
            }
        )
        for key in keys:
            row = by_key[key]
            italian = row["it"]
            terms = sorted({match.group(0) for match in GENDERED_WORD.finditer(italian)})
            if not terms or not FIRST_PERSON.search(italian):
                continue
            line_speaker_keys = sorted(attribution_keys[(speaker, key)])
            candidates.append(
                {
                    "key": key,
                    "speaker": speaker,
                    "speaker_keys": line_speaker_keys,
                    "speaker_ru": sorted(
                        {ru[speaker_key] for speaker_key in line_speaker_keys if speaker_key in ru}
                    ),
                    "speaker_ja": sorted(
                        {ja[speaker_key] for speaker_key in line_speaker_keys if speaker_key in ja}
                    ),
                    "source_en": row["source_en"],
                    "it": italian,
                    "ru": ru.get(key, ""),
                    "ja": ja.get(key, ""),
                    "matched_terms": terms,
                }
            )

    counts = Counter(item["speaker"] for item in candidates)
    return {
        "format": 1,
        "pmdata_records_with_known_text_and_speaker": record_count,
        "unique_speakers": len(speakers),
        "unique_dialogue_keys": len({key for keys in lines_by_speaker.values() for key in keys}),
        "candidate_count": len(candidates),
        "candidate_speakers": dict(sorted(counts.items(), key=lambda pair: pair[0].casefold())),
        "speakers": speakers,
        "candidates": candidates,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xdf", type=Path, required=True, help="LuaScripts.xdf o pmdata.bin")
    parser.add_argument("--csv", type=Path, default=Path("data/translation_it.csv"))
    parser.add_argument("--ru", type=Path)
    parser.add_argument("--ja", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    _rows, by_key = load_master(args.csv)
    report = build_inventory(
        load_pmdata(args.xdf), by_key, load_jsonl(args.ru), load_jsonl(args.ja)
    )
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
