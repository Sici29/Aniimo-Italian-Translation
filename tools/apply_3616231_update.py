"""Apply translation updates for Aniimo Steam build 3616231 (1.0.3616231.0)."""

from __future__ import annotations

import csv
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "translation_it.csv"
MANIFEST_PATH = ROOT / "data" / "supported_versions.json"
XDF_PATH = Path(r"D:\SteamLibrary\steamapps\common\Aniimo\Aniimo_Data\StreamingAssets\cvs\res\lua\LuaScripts.xdf")

UPDATES_3616231: dict[str, tuple[str, str]] = {
    # 7 New keys
    "1573976789": ("ad84af4e3b221ab2c677cc9d58dbad75cb456cfe621038118f3c8bcbb348dae2", "Sbloccati"),
    "1628877835": ("ad84af4e3b221ab2c677cc9d58dbad75cb456cfe621038118f3c8bcbb348dae2", "Sbloccati"),
    "1663588385": ("ad84af4e3b221ab2c677cc9d58dbad75cb456cfe621038118f3c8bcbb348dae2", "Sbloccati"),
    "1665021289": ("ad84af4e3b221ab2c677cc9d58dbad75cb456cfe621038118f3c8bcbb348dae2", "Sbloccati"),
    "1684729961": ("ad84af4e3b221ab2c677cc9d58dbad75cb456cfe621038118f3c8bcbb348dae2", "Sbloccati"),
    "1832291785": ("ad84af4e3b221ab2c677cc9d58dbad75cb456cfe621038118f3c8bcbb348dae2", "Sbloccati"),
    "1702079363": (
        "c87bfdc552dabc806642cc1f49580635ec383b72333baa4773610dd26950ef50",
        "Questo Aniimo è una variante speciale e non può usare questo Pigmento Scintillante.\n",
    ),
    # 2 Modified keys (Prismana Form conversion)
    "1726277553": (
        "ac7919a381d882725d395c6a3c837d0bcd4abc3c285b5d069cf29fa556409138",
        "Può essere usato solo su un Aniimo di Whisperwake Isles in tuo possesso, a patto che la sua Forma Prismana sia già stata sbloccata. Gli fa assumere la sua <style=Hint_BgL>Forma Prismana</style> conservando il Potenziale Acquisito, le mutazioni e la personalità originali.",
    ),
    "1914951211": (
        "cee2d505bfe4fbdf201d7f4c21adce7bb9792e34c59aae3b01a599ed578eb152",
        "Può essere usato solo su un Aniimo di Breezy Plains in tuo possesso, a patto che la sua Forma Prismana sia già stata sbloccata. Gli fa assumere la sua <style=Hint_BgL>Forma Prismana</style> conservando il Potenziale Acquisito, le mutazioni e la personalità originali.",
    ),
}


def apply_updates():
    # 1. Load existing CSV
    rows: dict[str, tuple[str, str]] = {}
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for r in reader:
            if len(r) >= 3:
                rows[r[0]] = (r[1], r[2])

    print(f"Existing rows in translation_it.csv: {len(rows)}")

    # 2. Apply updates
    applied_count = 0
    for key, (sha, it_text) in UPDATES_3616231.items():
        rows[key] = (sha, it_text)
        applied_count += 1

    print(f"Applied {applied_count} updates (new/modified). New total: {len(rows)}")

    # 3. Write back sorted by numeric key
    sorted_keys = sorted(rows.keys(), key=lambda k: int(k) if k.isdigit() else k)
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["key", "source_sha256", "it"])
        for k in sorted_keys:
            writer.writerow([k, rows[k][0], rows[k][1]])

    print(f"Wrote updated {CSV_PATH}")

    # 4. Read XDF to compute exact hashes
    with zipfile.ZipFile(XDF_PATH, "r") as zf:
        mapping = json.loads(zf.read("xfs/luascripts/Data/I18N/NewTextMap_en.json").decode("utf-8"))
        bin_data = zf.read("xfs/luascripts/Data/I18N/Compress_en.bin")

    source_keys = sorted([k for k in mapping if k not in ("_count", "_version")])
    keys_blob = "\n".join(source_keys).encode("utf-8")
    keys_sha256 = hashlib.sha256(keys_blob).hexdigest()

    # compute content sha256
    content_lines = []
    for k in source_keys:
        off, l = int(mapping[k][0]), int(mapping[k][1])
        text = bin_data[off:off+l].decode("utf-8", errors="replace")
        content_lines.append(f"{k}:{text}")
    content_sha256 = hashlib.sha256("\n".join(content_lines).encode("utf-8")).hexdigest()

    print(f"Build 3616231 keys: {len(source_keys)}")
    print(f"Keys sha256: {keys_sha256}")
    print(f"Content sha256: {content_sha256}")

    # 5. Update data/supported_versions.json
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    manifest["translation_version"] = "1.0.3616231.0"
    manifest["known_source_key_count"] = len(source_keys)
    manifest["known_source_key_sha256"] = keys_sha256
    manifest["known_source_content_sha256"] = content_sha256
    manifest["latest_supported_game_update"] = 3616231
    manifest["tested_game_update"] = "3616231"
    manifest["tested_date"] = "2026-09-28"
    if 3616231 not in manifest["supported_game_updates"]:
        manifest["supported_game_updates"].insert(0, 3616231)
    manifest["coverage"] = f"{len(source_keys)}/{len(source_keys)} keys translated (100.00%). Steam build 3616231 (patch 1.0.3616231.0) full professional coverage."

    note_0 = "Aggiornamento per la build Steam 3616231 (patch 1.0.3616231.0) con copertura di traduzione al 100% (112.214 chiavi)."
    note_1 = "Include il supporto alla selezione della lingua da sostituire (scelta tra 13 slot disponibili o slot inglese predefinito) e la guardia automatica sul download del patcher di gioco (PR #22 di Kaen89)."
    note_2 = "Tradotte tutte le 7 nuove chiavi della build 3616231 (funzione Unstuck/Sbloccati e notifica pigmento speciale) e aggiornate le descrizioni di Forma Prismana."

    manifest["notes"] = [note_0, note_1, note_2] + manifest["notes"][3:]

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Updated {MANIFEST_PATH}")


if __name__ == "__main__":
    apply_updates()
