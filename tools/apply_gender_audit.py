#!/usr/bin/env python3
"""Apply a reviewed gender-audit manifest to the Aniimo master CSV."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=Path("data/translation_it.csv"))
    parser.add_argument(
        "--audit", type=Path, default=Path("data/gender_audit_v0.3.10.json")
    )
    parser.add_argument("--marker", default="review_v0.3.10_full_gender_audit")
    args = parser.parse_args()

    with args.csv.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    if fields != ["key", "source_en", "it", "note"]:
        raise ValueError(f"Colonne CSV inattese: {fields}")

    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    operations = audit["operations"]
    by_key = {row["key"]: row for row in rows}
    if len(by_key) != len(rows):
        raise ValueError("Il master contiene chiavi duplicate")

    applied = 0
    for operation in operations:
        key = str(operation["key"])
        row = by_key.get(key)
        if row is None:
            raise KeyError(f"Chiave audit assente dal master: {key}")
        value = row["it"]
        changed = False
        for replacement in operation["replacements"]:
            old = replacement["old"]
            new = replacement["new"]
            occurrences = value.count(old)
            if occurrences == 0:
                if new in value:
                    continue
                raise ValueError(f"Testo atteso non trovato per {key}: {old!r}")
            if occurrences != 1:
                raise ValueError(
                    f"Sostituzione non univoca per {key}: {old!r} ({occurrences} occorrenze)"
                )
            value = value.replace(old, new, 1)
            changed = True
        if changed:
            row["it"] = value
            if args.marker not in row["note"].split(";"):
                row["note"] = ";".join(part for part in (row["note"], args.marker) if part)
            applied += 1

    with args.csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(
        json.dumps(
            {
                "audit": str(args.audit),
                "master": str(args.csv),
                "operations": len(operations),
                "rows_changed": applied,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
