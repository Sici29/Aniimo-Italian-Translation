#!/usr/bin/env python3
"""Create a deterministic full-master editorial QA inventory.

The report deliberately over-selects.  Every candidate still requires human
review, but the same checks can be rerun after each game or translation update.
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import re
from pathlib import Path


WORD = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-'’][A-Za-zÀ-ÖØ-öø-ÿ]+)*")
TAG = re.compile(r"<[^>]+>")
VALUE_TAG = re.compile(r"<(?:customRichText|sprite)\b[^>]*>", re.IGNORECASE)
PLACEHOLDER = re.compile(
    r"\{(?:\d+|param\d+|[A-Za-z_][A-Za-z0-9_]*)(?::[^{}]+)?\}|"
    r"%[sdif]|#k[A-Za-z0-9_/]+#z|#player[A-Za-z0-9_]*#"
)
CONTROL_TAG = re.compile(
    r"</?(?:style|color|size|b|i|u|link|sprite)\b[^>]*>", re.IGNORECASE
)
SLASH_INFLECTION = re.compile(
    r"\b(?:secondo/i|volta/e|giorno/i|ora/e|stella/e|uovo/i|colpo/i|"
    r"ricevuto/i|punto/i|moneta/e|momento/i|prezioso/i|amico/i|caro/a|"
    r"quale/i|impulso/i|accessorio/i|tentativo/i)\b",
    re.IGNORECASE,
)
TRAILING_DEPENDENT = {
    "a", "al", "alla", "alle", "allo", "ai", "agli", "con", "da", "dal",
    "dalla", "dalle", "dallo", "dai", "dagli", "di", "del", "della", "delle",
    "dello", "dei", "degli", "e", "fra", "i", "il", "in", "la", "le", "lo",
    "ma", "o", "per", "questa", "queste", "questi", "questo", "se", "su", "tra",
    "un", "una", "uno",
}
ENGLISH_RESIDUE = re.compile(
    r"\b(?:Aniimology|build|client|cooldown|cutscene|display|drop|feedback|"
    r"holo-gizmo|matchmaking|offline|online|outfit|quest(?!['’])|reset|sanctum|skin|"
    r"sparkling|spawn|stage|team|upgrade|workload)\b|"
    r"\b(?:ATK|DMG|HP|Fast and Furious|Gravity Pull|RV Park|Starbound Journey)\b",
    re.IGNORECASE,
)


def visible(text: str) -> str:
    # Some tags render a value or an icon by themselves.  Keep a sentinel so
    # an otherwise complete string is not misread as ending in a preposition.
    text = VALUE_TAG.sub(" X ", text)
    text = PLACEHOLDER.sub(" X ", text)
    return TAG.sub("", text).strip()


def item(row: dict[str, str], issue: str, detail: str) -> dict[str, str]:
    return {
        "key": row["key"],
        "source_en": row["source_en"],
        "it": row["it"],
        "note": row["note"],
        "issue": issue,
        "detail": detail,
    }


def audit(rows: list[dict[str, str]]) -> dict:
    candidates: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
    source_variants: dict[str, dict[str, list[str]]] = collections.defaultdict(
        lambda: collections.defaultdict(list)
    )

    for row in rows:
        source = row["source_en"]
        target = row["it"]
        source_variants[source][target].append(row["key"])

        if source != "0":
            source_placeholders = collections.Counter(PLACEHOLDER.findall(source))
            target_placeholders = collections.Counter(PLACEHOLDER.findall(target))
            if source_placeholders != target_placeholders:
                candidates["placeholder_mismatch"].append(
                    item(row, "placeholder_mismatch", f"{source_placeholders} != {target_placeholders}")
                )

            source_tags = collections.Counter(CONTROL_TAG.findall(source))
            target_tags = collections.Counter(CONTROL_TAG.findall(target))
            if source_tags != target_tags:
                candidates["control_tag_mismatch"].append(
                    item(row, "control_tag_mismatch", f"{source_tags} != {target_tags}")
                )

        slash = sorted(set(match.lower() for match in SLASH_INFLECTION.findall(target)))
        if slash:
            candidates["slash_inflection"].append(
                item(row, "slash_inflection", ", ".join(slash))
            )

        clean_target = visible(target)
        residues = sorted(set(match.group(0) for match in ENGLISH_RESIDUE.finditer(clean_target)))
        if residues:
            candidates["english_residue"].append(
                item(row, "english_residue", ", ".join(residues))
            )

        target_words = WORD.findall(clean_target)
        source_words = WORD.findall(visible(source))
        if (
            source != "0"
            and target_words
            and target_words[-1].lower() in TRAILING_DEPENDENT
            and (not source_words or source_words[-1].lower() not in {"a", "an", "and", "for", "in", "of", "on", "or", "the", "to", "with"})
        ):
            candidates["suspicious_ending"].append(
                item(row, "suspicious_ending", target_words[-1])
            )

        source_len = len(visible(source))
        target_len = len(clean_target)
        if source != "0" and source_len >= 24:
            ratio = target_len / source_len
            if ratio < 0.32 or ratio > 2.35:
                candidates["extreme_length_ratio"].append(
                    item(row, "extreme_length_ratio", f"{ratio:.3f}")
                )

    inconsistent = []
    for source, variants in source_variants.items():
        if source == "0" or len(variants) < 2:
            continue
        inconsistent.append(
            {
                "source_en": source,
                "variants": [
                    {"it": target, "keys": keys}
                    for target, keys in sorted(variants.items(), key=lambda pair: (-len(pair[1]), pair[0]))
                ],
            }
        )

    return {
        "format": 1,
        "rows": len(rows),
        "unique_keys": len({row["key"] for row in rows}),
        "unique_source_texts": len({row["source_en"] for row in rows}),
        "unique_italian_texts": len({row["it"] for row in rows}),
        "candidate_counts": {name: len(items) for name, items in sorted(candidates.items())},
        "candidates": {name: items for name, items in sorted(candidates.items())},
        "inconsistent_source_count": len(inconsistent),
        "inconsistent_sources": inconsistent,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=Path("data/translation_it.csv"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with args.csv.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    report = audit(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("rows", "unique_keys", "candidate_counts", "inconsistent_source_count")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
