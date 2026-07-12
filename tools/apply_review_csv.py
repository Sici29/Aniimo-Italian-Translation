#!/usr/bin/env python3
"""Apply a reviewed high-confidence CSV batch to the Italian master."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


TOKEN_RE = re.compile(
    r"<[^>]+>|#[A-Za-z0-9_]+#|\{[^{}]+\}|(?<!\d)%(?:\d+\$)?[-+0#]*\d*(?:\.\d+)?[diuoxXfFeEgGaAcs%]"
)


def signature(text: str) -> tuple[list[str], int, bool, bool]:
    return (
        TOKEN_RE.findall(text),
        text.count("\n"),
        bool(text[:1].isspace()),
        bool(text[-1:].isspace()),
    )


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def append_marker(note: str, marker: str) -> str:
    parts = [part for part in note.split(";") if part]
    if marker not in parts:
        parts.append(marker)
    return ";".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--marker", required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()

    with args.csv.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        master = [{key: normalize(value) for key, value in row.items()} for row in reader]
    with args.review.open("r", encoding="utf-8-sig", newline="") as handle:
        reviews = [
            {key: normalize(value) for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]

    required = {"key", "current_it", "proposed_it", "reason", "confidence"}
    if fields != ["key", "source_en", "it", "note"] or not reviews:
        raise ValueError("Master o batch di revisione non valido")
    if not required.issubset(reviews[0]):
        raise ValueError("Colonne obbligatorie mancanti nel batch")
    if len({row["key"] for row in master}) != len(master):
        raise ValueError("Chiavi duplicate nel master")
    if len({row["key"] for row in reviews}) != len(reviews):
        raise ValueError("Chiavi duplicate nel batch")

    by_key = {row["key"]: row for row in master}
    changed = 0
    already_applied = 0
    entries: list[dict[str, str]] = []
    for review in reviews:
        key = review["key"]
        if review["confidence"].lower() not in {"high", "alta"}:
            raise ValueError(f"Confidenza non alta per {key}")
        if key not in by_key:
            raise KeyError(f"Chiave assente dal master: {key}")
        current = review["current_it"]
        proposed = review["proposed_it"]
        if current == proposed or signature(current) != signature(proposed):
            raise ValueError(f"Struttura alterata nella proposta {key}")
        row = by_key[key]
        if row["it"] == current:
            row["it"] = proposed
            changed += 1
        elif row["it"] == proposed:
            already_applied += 1
        else:
            raise ValueError(f"Testo inatteso nel master per {key}")
        row["note"] = append_marker(row["note"], args.marker)
        entries.append(
            {
                "key": key,
                "proposed_it": proposed,
                "reason": review["reason"],
                "classification": review.get("classification", "reviewed"),
            }
        )

    with args.csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\r\n")
        writer.writeheader()
        writer.writerows(master)

    manifest = {
        "version": args.version,
        "scope_rows": len(master),
        "review_marker": args.marker,
        "accepted_unique_fixes": len(entries),
        "entries": sorted(entries, key=lambda item: int(item["key"])),
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"accepted_unique_fixes={len(entries)}")
    print(f"changed={changed}")
    print(f"already_applied={already_applied}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
