#!/usr/bin/env python3
"""Apply the approved v0.3.12 language-review batches deterministically."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


TOKEN_RE = re.compile(
    r"<[^>]+>|#[A-Za-z0-9_]+#|\{[^{}]+\}|(?<!\d)%(?:\d+\$)?[-+0 #]*\d*(?:\.\d+)?[A-Za-z%]"
)


def structural_signature(text: str) -> tuple[list[str], int]:
    return TOKEN_RE.findall(text), text.count("\n")


def load_review(path: Path, category: str) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"key", "current_it", "proposed_it", "reason", "confidence"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"Review non valido: {path}")
    for row in rows:
        row["category"] = category
    return rows


def append_marker(note: str, marker: str) -> str:
    parts = [part for part in note.split(";") if part]
    if marker not in parts:
        parts.append(marker)
    return ";".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--calques", type=Path, required=True)
    parser.add_argument("--fluency", type=Path, required=True)
    parser.add_argument("--tense", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    # Later batches win on overlapping keys. The fluency batch contains the
    # preferred final wording for the four overlaps with the calque batch.
    selected: dict[str, dict[str, str]] = {}
    for path, category in (
        (args.calques, "literal_calques"),
        (args.fluency, "italian_fluency"),
        (args.tense, "tense_consistency"),
    ):
        for row in load_review(path, category):
            selected[row["key"]] = row

    with args.csv.open("r", encoding="utf-8-sig", newline="") as handle:
        master = list(csv.DictReader(handle))
        fieldnames = list(master[0]) if master else []
    if not master or not {"key", "it", "note"}.issubset(fieldnames):
        raise ValueError(f"Master non valido: {args.csv}")

    by_key = {row["key"]: row for row in master}
    changed = 0
    already_applied = 0
    for key, review in selected.items():
        if key not in by_key:
            raise KeyError(f"Chiave assente dal master: {key}")
        row = by_key[key]
        current = review["current_it"]
        proposed = review["proposed_it"]
        if structural_signature(current) != structural_signature(proposed):
            raise ValueError(f"Struttura alterata nella proposta {key}")
        if row["it"] == current:
            row["it"] = proposed
            changed += 1
        elif row["it"] == proposed:
            already_applied += 1
        else:
            raise ValueError(
                f"Testo inatteso per {key}: il master non coincide con current_it o proposed_it"
            )
        marker = f"review_v0.3.12_{review['category']}"
        row["note"] = append_marker(row["note"], marker)

    with args.csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\r\n")
        writer.writeheader()
        writer.writerows(master)

    counts = Counter(row["category"] for row in selected.values())
    manifest = {
        "version": "0.3.12-beta",
        "scope_rows": 92954,
        "selected_unique_fixes": len(selected),
        "counts": dict(sorted(counts.items())),
        "precedence": ["literal_calques", "italian_fluency", "tense_consistency"],
        "entries": [
            {
                "key": key,
                "category": row["category"],
                "proposed_it": row["proposed_it"],
                "reason": row["reason"],
                "confidence": row["confidence"],
            }
            for key, row in sorted(selected.items(), key=lambda item: int(item[0]))
        ],
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"selected_unique_fixes={len(selected)}")
    print(f"changed={changed}")
    print(f"already_applied={already_applied}")
    print("counts=" + json.dumps(dict(sorted(counts.items()))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
