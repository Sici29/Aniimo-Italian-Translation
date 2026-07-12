#!/usr/bin/env python3
"""Apply a reviewed full-quality audit manifest to the Aniimo master CSV."""

from __future__ import annotations

import argparse
import collections
import csv
import json
import re
from pathlib import Path


STRUCTURAL_TOKEN = re.compile(
    r"<[^>]+>|\{[^{}]+\}|%[sdif]|#k[A-Za-z0-9_/]+#z|#player[A-Za-z0-9_]*#"
)


def signature(text: str) -> collections.Counter[str]:
    return collections.Counter(STRUCTURAL_TOKEN.findall(text))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=Path("data/translation_it.csv"))
    parser.add_argument(
        "--audit", type=Path, default=Path("data/quality_audit_v0.3.11.json")
    )
    parser.add_argument("--marker", default="review_v0.3.11_full_quality_audit")
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
    if len({str(item["key"]) for item in operations}) != len(operations):
        raise ValueError("Il manifesto contiene chiavi duplicate")

    applied = 0
    already_applied = 0
    for operation in operations:
        key = str(operation["key"])
        row = by_key.get(key)
        if row is None:
            raise KeyError(f"Chiave audit assente dal master: {key}")
        old = operation["old_it"]
        new = operation["new_it"]
        if signature(old) != signature(new):
            raise ValueError(f"Tag o segnaposto alterati nel manifesto per {key}")
        accepted_old = operation.get("accepted_old_it", [])
        if any(signature(value) != signature(new) for value in accepted_old):
            raise ValueError(f"Valore intermedio strutturalmente incompatibile per {key}")
        if row["it"] == new:
            already_applied += 1
            continue
        if row["it"] != old and row["it"] not in accepted_old:
            raise ValueError(
                f"Testo corrente inatteso per {key}: {row['it']!r}; atteso {old!r}"
            )
        row["it"] = new
        notes = [part for part in row["note"].split(";") if part]
        if args.marker not in notes:
            notes.append(args.marker)
        row["note"] = ";".join(notes)
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
                "already_applied": already_applied,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
