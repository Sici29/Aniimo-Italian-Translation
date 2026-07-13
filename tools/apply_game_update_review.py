#!/usr/bin/env python3
"""Apply a verified Aniimo text update and its human-reviewed Italian changes."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def key_sha256(keys: list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(keys)).encode("utf-8")).hexdigest()


def append_marker(note: str, marker: str) -> str:
    parts = [part for part in note.split(";") if part]
    if marker not in parts:
        parts.append(marker)
    return ";".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", type=Path, required=True)
    parser.add_argument("--update-report", type=Path, required=True)
    parser.add_argument("--new-review", type=Path, required=True)
    parser.add_argument("--changed-review", type=Path, action="append", default=[])
    parser.add_argument("--additional-review", type=Path, action="append", default=[])
    parser.add_argument("--audit-output", type=Path, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--game-update", required=True)
    parser.add_argument("--observed-local-digest", required=True)
    args = parser.parse_args()

    master_raw = args.master.read_bytes()
    master_line_ending = "\r\n" if b"\r\n" in master_raw else "\n"
    master_rows = read_csv(args.master)
    by_key = {row["key"]: row for row in master_rows}
    if len(by_key) != len(master_rows):
        raise ValueError("Il master contiene chiavi duplicate")

    report = json.loads(args.update_report.read_text(encoding="utf-8-sig"))
    if int(report["old_count"]) != len(master_rows):
        raise ValueError("Il report non corrisponde alla dimensione del master")
    if str(report["game"]["update"]) != str(args.game_update):
        raise ValueError("La build del report non corrisponde a --game-update")
    if str(report["game"]["revision"]).lower() != args.observed_local_digest.lower():
        raise ValueError(
            "Il digest locale del report non corrisponde a --observed-local-digest"
        )

    changed_by_key = {entry["key"]: entry for entry in report["changed_source"]}
    for key, entry in changed_by_key.items():
        row = by_key.get(key)
        if row is None or row["source_en"] != entry["old_source_en"]:
            raise ValueError(f"Sorgente precedente inattesa per la chiave {key}")
        row["source_en"] = entry["new_source_en"]

    new_review = read_csv(args.new_review)
    expected_new = {entry["key"]: entry for entry in report["added"]}
    reviewed_new = {row["key"]: row for row in new_review}
    if set(reviewed_new) != set(expected_new):
        raise ValueError("La revisione delle nuove chiavi è incompleta o contiene chiavi estranee")
    for key, reviewed in reviewed_new.items():
        source = expected_new[key]["locales"]["en"]
        if reviewed["source_en"] != source or not reviewed["it"].strip():
            raise ValueError(f"Revisione nuova non valida per la chiave {key}")
        by_key[key] = {
            "key": key,
            "source_en": source,
            "it": reviewed["it"],
            "note": f"game_update_{args.game_update}_new",
        }

    semantic_changes: list[dict[str, str]] = []
    reviewed_changed_keys: set[str] = set()
    for review_path in args.changed_review:
        for reviewed in read_csv(review_path):
            key = reviewed["key"]
            if key in reviewed_changed_keys:
                raise ValueError(f"Chiave revisionata più volte: {key}")
            reviewed_changed_keys.add(key)
            entry = changed_by_key.get(key)
            if entry is None:
                raise ValueError(f"Chiave estranea alla revisione dell'aggiornamento: {key}")
            if reviewed["old_source_en"] != entry["old_source_en"]:
                raise ValueError(f"Vecchia sorgente inattesa per la chiave {key}")
            if reviewed["new_source_en"] != entry["new_source_en"]:
                raise ValueError(f"Nuova sorgente inattesa per la chiave {key}")
            if reviewed["current_it"] != entry["current_it"]:
                raise ValueError(f"Italiano precedente inatteso per la chiave {key}")
            proposed = reviewed["proposed_it"]
            if not proposed.strip():
                raise ValueError(f"Proposta italiana vuota per la chiave {key}")
            by_key[key]["it"] = proposed
            by_key[key]["note"] = append_marker(
                by_key[key]["note"], f"game_update_{args.game_update}_revised"
            )
            semantic_changes.append(
                {
                    "key": key,
                    "old_it": reviewed["current_it"],
                    "new_it": proposed,
                    "reason": reviewed["reason"],
                }
            )

    additional_changes: list[dict[str, str]] = []
    reviewed_additional_keys: set[str] = set()
    for review_path in args.additional_review:
        for reviewed in read_csv(review_path):
            key = reviewed["key"]
            if key in reviewed_additional_keys or key in reviewed_changed_keys:
                raise ValueError(f"Chiave revisionata più volte: {key}")
            reviewed_additional_keys.add(key)
            row = by_key.get(key)
            if row is None:
                raise ValueError(f"Chiave aggiuntiva assente dal master: {key}")
            if row["it"] != reviewed["current_it"]:
                raise ValueError(f"Italiano precedente inatteso per la chiave aggiuntiva {key}")
            proposed = reviewed["proposed_it"]
            if not proposed.strip() or proposed == reviewed["current_it"]:
                raise ValueError(f"Proposta aggiuntiva non valida per la chiave {key}")
            row["it"] = proposed
            row["note"] = append_marker(
                row["note"], f"game_update_{args.game_update}_family"
            )
            additional_changes.append(
                {
                    "key": key,
                    "old_it": reviewed["current_it"],
                    "new_it": proposed,
                    "reason": reviewed["reason"],
                }
            )

    existing_order = [row["key"] for row in master_rows]
    existing_key_set = set(existing_order)
    output_rows = [by_key[key] for key in existing_order]
    output_rows.extend(
        sorted(
            (row for key, row in by_key.items() if key not in existing_key_set),
            key=lambda row: int(row["key"]) if row["key"].isdigit() else row["key"],
        )
    )
    if len(output_rows) != int(report["new_count"]):
        raise ValueError("Il master aggiornato non contiene il numero previsto di chiavi")

    with args.master.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["key", "source_en", "it", "note"],
            lineterminator=master_line_ending,
        )
        writer.writeheader()
        writer.writerows(output_rows)

    audit = {
        "version": args.version,
        "game_update": int(args.game_update),
        "observed_local_digest": args.observed_local_digest.lower(),
        "revision_authority": (
            "Digest locale ereditato dal manifest patchato precedente; non trattato "
            "come revisione ufficiale della build."
        ),
        "archive_sha256": report["archive_sha256"],
        "previous_key_count": int(report["old_count"]),
        "key_count": len(output_rows),
        "key_sha256": key_sha256([row["key"] for row in output_rows]),
        "added_keys": len(reviewed_new),
        "removed_keys": len(report["removed"]),
        "refreshed_english_sources": len(changed_by_key),
        "semantic_italian_revisions": len(semantic_changes),
        "additional_family_revisions": len(additional_changes),
        "new_entries": [
            {"key": row["key"], "source_en": row["source_en"], "it": row["it"]}
            for row in new_review
        ],
        "semantic_changes": semantic_changes,
        "additional_changes": additional_changes,
        "date_patch_compatible": report["date_patch_compatible"],
    }
    args.audit_output.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                key: value
                for key, value in audit.items()
                if key not in {"new_entries", "semantic_changes", "additional_changes"}
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
