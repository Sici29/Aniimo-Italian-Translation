#!/usr/bin/env python3
"""Consolidate and replay the final post-audit editorial corrections."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


TOKEN_RE = re.compile(
    r"<[^>]+>|#[A-Za-z0-9_]+#|\{[^{}]+\}|(?<!\d)%(?:\d+\$)?[-+0#]*\d*(?:\.\d+)?[diuoxXfFeEgGaAcs%]"
)


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


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


def load_master(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0]) if rows else []
    if not rows or not {"key", "source_en", "it", "note"}.issubset(fieldnames):
        raise ValueError(f"Master non valido: {path}")
    for row in rows:
        for field in fieldnames:
            row[field] = normalize(row[field])
    if len({row["key"] for row in rows}) != len(rows):
        raise ValueError("Il master contiene chiavi duplicate")
    return rows, fieldnames


def load_proposals(paths: list[Path]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    required = {"key", "current_it", "proposed_it", "reason", "confidence"}
    for path in paths:
        category = path.parent.name
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        if not rows or not required.issubset(rows[0]):
            raise ValueError(f"Proposte non valide: {path}")
        for row in rows:
            row = {key: normalize(value) for key, value in row.items()}
            row["category"] = category
            grouped[row["key"]].append(row)
    return grouped


def replay_entries(path: Path) -> dict[str, dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        str(item["key"]): {
            "key": str(item["key"]),
            "current_it": item["current_it"],
            "proposed_it": item["proposed_it"],
            "reason": item["reason"],
            "confidence": item.get("confidence", "alta"),
            "category": item.get("category", "post_editorial"),
        }
        for item in data["entries"]
    }


def build_selected(
    master: list[dict[str, str]],
    grouped: dict[str, list[dict[str, str]]],
    decisions: dict,
    prior: dict[str, dict[str, str]] | None = None,
) -> tuple[dict[str, dict[str, str]], list[dict[str, str]], int]:
    prior = prior or {}
    by_key = {row["key"]: row for row in master}
    overrides = {str(item["key"]): item for item in decisions.get("override", [])}
    rejected = {str(item["key"]): item for item in decisions.get("reject", [])}
    selected: dict[str, dict[str, str]] = {}
    conflicts_resolved = 0

    for key, candidates in grouped.items():
        if key not in by_key:
            raise KeyError(f"Chiave proposta assente dal master: {key}")
        currents = {item["current_it"] for item in candidates}
        if len(currents) != 1:
            raise ValueError(f"Testi correnti discordanti fra audit per {key}")
        proposals = {item["proposed_it"] for item in candidates}
        if len(proposals) > 1 and key not in overrides:
            raise ValueError(f"Proposte discordanti senza decisione editoriale per {key}")
        if len(proposals) > 1:
            conflicts_resolved += 1
        chosen = candidates[0].copy()
        chosen["category"] = "+".join(sorted({item["category"] for item in candidates}))
        chosen["reason"] = " ".join(dict.fromkeys(item["reason"] for item in candidates))
        chosen["alternative_proposals"] = list(proposals)
        selected[key] = chosen

    rejected_manifest: list[dict[str, str]] = []
    for key, item in rejected.items():
        if key not in selected:
            raise KeyError(f"Decisione di rifiuto senza proposta: {key}")
        rejected_manifest.append({"key": key, "reason": item["reason"]})
        del selected[key]

    for key, item in overrides.items():
        if key not in selected:
            raise KeyError(f"Riscrittura editoriale senza proposta: {key}")
        selected[key]["proposed_it"] = normalize(item["proposed_it"])
        selected[key]["reason"] = item["reason"]
        selected[key]["adjudicated"] = "true"

    for rule in decisions.get("source_group_override", []):
        source = rule["source_en"]
        matches = [row for row in master if row["source_en"] == source]
        if not matches:
            raise ValueError(f"Famiglia sorgente assente: {source}")
        for row in matches:
            key = row["key"]
            current = selected.get(key, {}).get(
                "current_it", prior.get(key, {}).get("current_it", row["it"])
            )
            selected[key] = {
                "key": key,
                "current_it": current,
                "proposed_it": normalize(rule["proposed_it"]),
                "reason": rule["reason"],
                "confidence": "alta",
                "category": "source_group",
                "adjudicated": "true",
                "alternative_proposals": selected.get(key, {}).get(
                    "alternative_proposals", []
                ),
            }

    for rule in decisions.get("target_replacement", []):
        old = rule["old"]
        new = rule["new"]
        for raw_key in rule["keys"]:
            key = str(raw_key)
            if key not in by_key:
                raise KeyError(f"Chiave della sostituzione assente: {key}")
            previous = selected.get(key, prior.get(key, {}))
            base = previous.get(
                "proposed_it", prior.get(key, {}).get("proposed_it", by_key[key]["it"])
            )
            if old not in base:
                if key in prior:
                    selected[key] = prior[key]
                    continue
                raise ValueError(f"Frammento {old!r} assente nella chiave {key}")
            current = previous.get(
                "current_it", prior.get(key, {}).get("current_it", by_key[key]["it"])
            )
            category = rule.get("category", "target_replacement")
            if previous.get("category") and previous["category"] != category:
                category = "+".join(sorted({previous["category"], category}))
            reason = rule["reason"]
            if previous.get("reason") and previous["reason"] != reason:
                reason = previous["reason"] + " " + reason
            selected[key] = {
                "key": key,
                "current_it": current,
                "proposed_it": base.replace(old, new),
                "reason": reason,
                "confidence": "alta",
                "category": category,
                "adjudicated": "true",
                "alternative_proposals": selected.get(key, {}).get(
                    "alternative_proposals", []
                ),
            }

    for key, item in prior.items():
        selected.setdefault(key, item)

    return selected, rejected_manifest, conflicts_resolved


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--proposal", type=Path, action="append", default=[])
    parser.add_argument("--decisions", type=Path)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()

    master, fieldnames = load_master(args.csv)
    by_key = {row["key"]: row for row in master}
    if args.replay:
        selected = replay_entries(args.manifest)
        rejected_manifest: list[dict[str, str]] = []
        conflicts_resolved = 0
        decisions = json.loads(args.manifest.read_text(encoding="utf-8"))
    else:
        if not args.proposal or args.decisions is None:
            parser.error("--proposal e --decisions sono obbligatori senza --replay")
        decisions = json.loads(args.decisions.read_text(encoding="utf-8"))
        grouped = load_proposals(args.proposal)
        prior = replay_entries(args.manifest) if args.manifest.exists() else {}
        selected, rejected_manifest, conflicts_resolved = build_selected(
            master, grouped, decisions, prior
        )

    marker = decisions.get("review_marker", "review_v0.3.12_post_editorial")
    changed = 0
    already_applied = 0
    for key, item in selected.items():
        if key not in by_key:
            raise KeyError(f"Chiave assente dal master: {key}")
        current = normalize(item["current_it"])
        proposed = normalize(item["proposed_it"])
        if current == proposed:
            raise ValueError(f"Operazione senza modifica: {key}")
        if structural_signature(current) != structural_signature(proposed):
            raise ValueError(f"Struttura alterata nella correzione {key}")
        row = by_key[key]
        alternatives = [normalize(value) for value in item.get("alternative_proposals", [])]
        if row["it"] == proposed:
            already_applied += 1
        elif row["it"] == current or row["it"] in alternatives:
            row["it"] = proposed
            changed += 1
        else:
            raise ValueError(f"Testo inatteso nel master per {key}")
        row["note"] = append_marker(row["note"], marker)

    with args.csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\r\n")
        writer.writeheader()
        writer.writerows(master)

    if not args.replay:
        categories = Counter(item["category"] for item in selected.values())
        manifest = {
            "version": decisions.get("version", "0.3.12-beta"),
            "scope_rows": len(master),
            "review_marker": marker,
            "input_proposals": sum(len(items) for items in grouped.values()),
            "input_unique_keys": len(grouped),
            "accepted_unique_fixes": len(selected),
            "rejected_after_adjudication": len(rejected_manifest),
            "conflicts_resolved": conflicts_resolved,
            "counts": dict(sorted(categories.items())),
            "rejected": sorted(rejected_manifest, key=lambda item: int(item["key"])),
            "entries": [
                {
                    "key": key,
                    "current_it": item["current_it"],
                    "proposed_it": item["proposed_it"],
                    "reason": item["reason"],
                    "confidence": item.get("confidence", "alta"),
                    "category": item["category"],
                    "adjudicated": item.get("adjudicated", "false") == "true",
                }
                for key, item in sorted(selected.items(), key=lambda pair: int(pair[0]))
            ],
        }
        args.manifest.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print(f"accepted_unique_fixes={len(selected)}")
    print(f"changed={changed}")
    print(f"already_applied={already_applied}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
