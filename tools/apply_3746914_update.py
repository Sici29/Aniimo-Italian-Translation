import csv
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
XDF = Path(r"D:\SteamLibrary\steamapps\common\Aniimo\Aniimo_Data\StreamingAssets\cvs\res\lua\LuaScripts.xdf")

# 1. Load official English records from 3746914 LuaScripts.xdf
with zipfile.ZipFile(XDF, "r") as zf:
    mapping = json.loads(zf.read("xfs/luascripts/Data/I18N/NewTextMap_en.json").decode("utf-8-sig"))
    bin_data = zf.read("xfs/luascripts/Data/I18N/Compress_en.bin")

official_en = {}
for k, v in mapping.items():
    if not str(k).startswith("_") and isinstance(v, list) and len(v) == 2:
        off, length = int(v[0]), int(v[1])
        text = bin_data[off : off + length].decode("utf-8", errors="replace")
        official_en[str(k)] = text

print(f"Loaded {len(official_en)} official English strings from build 3746914.")

# 2. Verify all keys match existing translation_it.csv
csv_path = ROOT / "data" / "translation_it.csv"
with csv_path.open("r", encoding="utf-8", newline="") as f:
    existing_rows = list(csv.DictReader(f))

old_catalog = {row["key"]: row for row in existing_rows}
assert len(official_en) == len(old_catalog), f"Count mismatch: {len(official_en)} vs {len(old_catalog)}"

for k, en_text in official_en.items():
    assert k in old_catalog, f"Missing key: {k}"
    cur_sha = hashlib.sha256(en_text.encode("utf-8")).hexdigest()
    assert cur_sha == old_catalog[k]["source_sha256"], f"SHA mismatch for key {k}"

print(f"Verified 100.00% exact match across all {len(official_en)} strings.")

# 3. Compute manifest hashes
sys_path = ROOT / "tools"
import sys
sys.path.insert(0, str(sys_path))
import aniimo_it_installer as inst

sorted_keys = sorted(old_catalog.keys(), key=lambda x: int(x) if x.isdigit() else 999999999)
keys_sha = inst.sha256_keys(sorted_keys)
content_sha = inst.sha256_keyed_text(official_en)
archive_sha = hashlib.sha256(XDF.read_bytes()).hexdigest()

print(f"known_source_key_sha256: {keys_sha}")
print(f"known_source_content_sha256: {content_sha}")
print(f"tested_archive_sha256: {archive_sha}")

# 4. Update data/supported_versions.json
manifest_path = ROOT / "data" / "supported_versions.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

manifest["translation_version"] = "1.0.3746914.0"
manifest["latest_supported_game_update"] = "3746914"
manifest["tested_game_update"] = "3746914"

if "3746914" not in manifest["supported_game_updates"]:
    manifest["supported_game_updates"].insert(0, "3746914")

revision = "0be02c78f59cc13b8e4cd5d392b5edaf"
if revision not in manifest["supported_game_revisions"]:
    manifest["supported_game_revisions"].insert(0, revision)

manifest["tested_game_revision"] = revision
manifest["tested_archive_sha256"] = archive_sha
manifest["tested_date"] = "2026-10-17"

manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Updated data/supported_versions.json successfully.")
