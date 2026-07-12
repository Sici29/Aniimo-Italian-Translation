#!/usr/bin/env python3
"""Apply the three independently reviewed v0.3.12 editorial blocks."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


TOKEN_RE = re.compile(
    r"<[^>]+>|#[A-Za-z0-9_]+#|\{[^{}]+\}|(?<!\d)%(?:\d+\$)?[-+0#]*\d*(?:\.\d+)?[diuoxXfFeEgGaAcs%]"
)


def structural_signature(text: str) -> tuple[list[str], int, bool, bool]:
    return (
        TOKEN_RE.findall(text),
        text.count("\n"),
        bool(text[:1].isspace()),
        bool(text[-1:].isspace()),
    )


def append_marker(note: str, marker: str) -> str:
    parts = [part for part in note.split(";") if part]
    if marker not in parts:
        parts.append(marker)
    return ";".join(parts)


def remove_marker(note: str, marker: str) -> str:
    return ";".join(part for part in note.split(";") if part and part != marker)


def load_proposals(paths: list[Path]) -> dict[str, dict[str, str]]:
    required = {
        "key",
        "source_en",
        "current_it",
        "proposed_it",
        "reason",
        "confidence",
    }
    selected: dict[str, dict[str, str]] = {}
    for block_index, path in enumerate(paths, start=1):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        if not rows or not required.issubset(rows[0]):
            raise ValueError(f"Blocco di revisione non valido: {path}")
        for row in rows:
            key = row["key"]
            if key in selected:
                raise ValueError(f"Chiave duplicata nei blocchi: {key}")
            row["block"] = str(block_index)
            selected[key] = row
    return selected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--block", type=Path, action="append", required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    selected = load_proposals(args.block)
    decisions = json.loads(args.decisions.read_text(encoding="utf-8"))
    reject = {item["key"]: item["reason"] for item in decisions.get("reject", [])}
    overrides = {item["key"]: item for item in decisions.get("override", [])}
    unknown = (set(reject) | set(overrides)) - set(selected)
    if unknown:
        raise KeyError(f"Decisioni per chiavi non proposte: {sorted(unknown)}")
    if set(reject) & set(overrides):
        raise ValueError("Una chiave non può essere sia rifiutata sia riscritta")

    for key, item in overrides.items():
        selected[key]["original_proposed_it"] = selected[key]["proposed_it"]
        selected[key]["proposed_it"] = item["proposed_it"]
        selected[key]["reason"] = item["reason"]
        selected[key]["adjudicated"] = "true"

    accepted = {key: row for key, row in selected.items() if key not in reject}
    for key, row in accepted.items():
        if structural_signature(row["current_it"]) != structural_signature(
            row["proposed_it"]
        ):
            raise ValueError(f"Struttura alterata nella proposta finale {key}")

    with args.csv.open("r", encoding="utf-8-sig", newline="") as handle:
        master = list(csv.DictReader(handle))
        fieldnames = list(master[0]) if master else []
    if not master or not {"key", "it", "note"}.issubset(fieldnames):
        raise ValueError(f"Master non valido: {args.csv}")
    if len({row["key"] for row in master}) != len(master):
        raise ValueError("Il master contiene chiavi duplicate")
    for master_row in master:
        for field in fieldnames:
            master_row[field] = master_row[field].replace("\r\n", "\n").replace("\r", "\n")

    by_key = {row["key"]: row for row in master}
    marker = decisions.get("review_marker", "review_v0.3.12_deep_editorial")
    changed = 0
    already_applied = 0
    restored_rejections = 0
    for key in reject:
        if key not in by_key:
            raise KeyError(f"Chiave rifiutata assente dal master: {key}")
        row = by_key[key]
        review = selected[key]
        if row["it"] == review["proposed_it"]:
            row["it"] = review["current_it"]
            restored_rejections += 1
        elif row["it"] != review["current_it"]:
            raise ValueError(f"Testo inatteso per la proposta rifiutata {key}")
        row["note"] = remove_marker(row["note"], marker)

    for key, review in accepted.items():
        if key not in by_key:
            raise KeyError(f"Chiave assente dal master: {key}")
        row = by_key[key]
        if row["it"] == review["current_it"]:
            row["it"] = review["proposed_it"]
            changed += 1
        elif row["it"] == review.get("original_proposed_it"):
            row["it"] = review["proposed_it"]
            changed += 1
        elif row["it"] == review["proposed_it"]:
            already_applied += 1
        else:
            raise ValueError(
                f"Testo inatteso per {key}: il master non coincide con current_it o proposed_it"
            )
        row["note"] = append_marker(row["note"], marker)

    # Git stores CRLF between CSV records and LF inside quoted multiline fields.
    # Normalizing field content avoids turning every embedded line break into a
    # repository-wide diff when the master is regenerated on Windows.
    for master_row in master:
        for field in fieldnames:
            master_row[field] = master_row[field].replace("\r\n", "\n").replace("\r", "\n")

    with args.csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\r\n")
        writer.writeheader()
        writer.writerows(master)

    block_counts = Counter(row["block"] for row in accepted.values())
    manifest = {
        "version": decisions.get("version", "0.3.12-beta"),
        "scope_rows": len(master),
        "unique_source_texts_reviewed": 42637,
        "proposals_received": len(selected),
        "accepted_unique_fixes": len(accepted),
        "rejected_after_adjudication": len(reject),
        "overridden_after_adjudication": len(overrides),
        "accepted_by_block": dict(sorted(block_counts.items())),
        "review_marker": marker,
        "rejected": [
            {"key": key, "reason": reason}
            for key, reason in sorted(reject.items(), key=lambda item: int(item[0]))
        ],
        "entries": [
            {
                "key": key,
                "block": row["block"],
                "source_en": row["source_en"],
                "proposed_it": row["proposed_it"],
                "reason": row["reason"],
                "confidence": row["confidence"],
                "adjudicated": row.get("adjudicated", "false") == "true",
            }
            for key, row in sorted(accepted.items(), key=lambda item: int(item[0]))
        ],
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"proposals_received={len(selected)}")
    print(f"accepted_unique_fixes={len(accepted)}")
    print(f"rejected={len(reject)}")
    print(f"overridden={len(overrides)}")
    print(f"restored_rejections={restored_rejections}")
    print(f"changed={changed}")
    print(f"already_applied={already_applied}")
    print("accepted_by_block=" + json.dumps(dict(sorted(block_counts.items()))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
