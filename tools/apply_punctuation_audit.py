#!/usr/bin/env python3
"""Apply the reviewed Italian trailing-punctuation policy to the Aniimo master."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def replace_trailing(text: str, old: str, new: str) -> str:
    stripped = text.rstrip()
    trailing_space = text[len(stripped) :]
    if not stripped.endswith(old):
        return text
    return stripped[: -len(old)] + new + trailing_space


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=Path("data/translation_it.csv"))
    parser.add_argument(
        "--audit", type=Path, default=Path("data/punctuation_audit_v0.3.12.json")
    )
    args = parser.parse_args()

    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    source_suffix = str(audit["source_suffix"])
    italian_suffix = str(audit["italian_suffix"])
    marker = str(audit["note_marker"])
    expected_source = int(audit["source_rows_ending_with_em_dash"])
    expected_changes = int(audit["rows_to_normalize"])

    with args.csv.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    if fields != ["key", "source_en", "it", "note"]:
        raise ValueError(f"Colonne CSV inattese: {fields}")

    source_rows = 0
    changed = 0
    already_applied = 0
    for row in rows:
        if not row["source_en"].rstrip().endswith(source_suffix):
            continue
        source_rows += 1
        notes = [part for part in row["note"].split(";") if part]
        if row["it"].rstrip().endswith(source_suffix):
            row["it"] = replace_trailing(row["it"], source_suffix, italian_suffix)
            if marker not in notes:
                notes.append(marker)
            row["note"] = ";".join(notes)
            changed += 1
        elif marker in notes:
            already_applied += 1

    if source_rows != expected_source:
        raise ValueError(
            f"Conteggio sorgenti inatteso: {source_rows}; atteso {expected_source}"
        )
    if changed + already_applied != expected_changes:
        raise ValueError(
            "Audit parziale o master inatteso: "
            f"modificate {changed}, già applicate {already_applied}, attese {expected_changes}"
        )

    with args.csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(
        json.dumps(
            {
                "master": str(args.csv),
                "source_rows": source_rows,
                "rows_changed": changed,
                "already_applied": already_applied,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
