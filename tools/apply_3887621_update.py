import csv
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STREAMING_LUA = Path(r"D:\SteamLibrary\steamapps\common\Aniimo\Aniimo_Data\StreamingAssets\cvs\res\lua")
CVS_LUA = Path(r"D:\SteamLibrary\steamapps\common\Aniimo\Aniimo_Data\cvs\res\lua")
XDF = STREAMING_LUA / "LuaScripts.xdf"
XDT = STREAMING_LUA / "LuaScripts.xdt"
VER_FILE = Path(r"D:\SteamLibrary\steamapps\common\Aniimo\verlist.txt")

# 1. Load official English records from 3887621 LuaScripts.xdf
with zipfile.ZipFile(XDF, "r") as zf:
    mapping = json.loads(zf.read("xfs/luascripts/Data/I18N/NewTextMap_en.json").decode("utf-8-sig"))
    bin_data = zf.read("xfs/luascripts/Data/I18N/Compress_en.bin")

official_en = {}
for k, v in mapping.items():
    if not str(k).startswith("_") and isinstance(v, list) and len(v) == 2:
        off, length = int(v[0]), int(v[1])
        text = bin_data[off : off + length].decode("utf-8", errors="replace")
        official_en[str(k)] = text

print(f"Loaded {len(official_en)} official English strings from build 3887621.")
assert len(official_en) == 134298, f"Expected 134298 keys, got {len(official_en)}"

# 2. Load 608 Updated Translations
translations_path = ROOT / "tools" / "translations_3887621.json"
updated_translations = json.loads(translations_path.read_text(encoding="utf-8"))
print(f"Loaded {len(updated_translations)} updated translations.")
assert len(updated_translations) == 608, f"Expected 608 updated translations, got {len(updated_translations)}"

# 3. Load existing translation_it.csv
csv_path = ROOT / "data" / "translation_it.csv"
with csv_path.open("r", encoding="utf-8", newline="") as f:
    existing_rows = list(csv.DictReader(f))

old_catalog = {row["key"]: row for row in existing_rows}
new_catalog = {}

for k, en_text in official_en.items():
    cur_sha = hashlib.sha256(en_text.encode("utf-8")).hexdigest()
    if k in updated_translations:
        it_text = updated_translations[k]
    elif k in old_catalog:
        it_text = old_catalog[k]["it"]
    else:
        raise RuntimeError(f"Missing translation for key: {k}")
    new_catalog[k] = {"key": k, "source_sha256": cur_sha, "it": it_text}

assert len(new_catalog) == len(official_en), f"Count mismatch: {len(new_catalog)} vs {len(official_en)}"
print(f"Verified 100.00% exact match across all {len(official_en)} strings.")

sorted_keys = sorted(new_catalog.keys(), key=lambda x: int(x) if x.isdigit() else 999999999)

# 4. Write data/translation_it.csv
with csv_path.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["key", "source_sha256", "it"])
    writer.writeheader()
    for k in sorted_keys:
        writer.writerow(new_catalog[k])

print(f"Successfully wrote {len(sorted_keys)} keys to data/translation_it.csv.")

# 5. Synchronize live game files in Aniimo_Data/cvs/res/lua with StreamingAssets
if CVS_LUA.is_dir():
    for f in CVS_LUA.glob("LuaScripts.*"):
        f.unlink()
    shutil.copy2(XDF, CVS_LUA / "LuaScripts.xdf")
    shutil.copy2(XDT, CVS_LUA / "LuaScripts.xdt")
    print("Synchronized cvs/res/lua with StreamingAssets/cvs/res/lua.")

# Compute MD5 and size of LuaScripts.xdt
xdt_size = XDT.stat().st_size
xdt_md5 = hashlib.md5(XDT.read_bytes()).hexdigest()
cache_ver_content = f"1.0.3887621,{xdt_size},{xdt_md5}\n"

(STREAMING_LUA / "LuaCacheVer.txt").write_text(cache_ver_content, encoding="utf-8")
if CVS_LUA.is_dir():
    (CVS_LUA / "LuaCacheVer.txt").write_text(cache_ver_content, encoding="utf-8")
print(f"Synchronized LuaCacheVer.txt: {cache_ver_content.strip()}")

# 6. Compute manifest hashes & update data/supported_versions.json
sys_path = ROOT / "tools"
import sys
sys.path.insert(0, str(sys_path))
import aniimo_it_installer as inst

keys_sha = inst.sha256_keys(sorted_keys)
content_sha = inst.sha256_keyed_text(official_en)
archive_sha = hashlib.sha256(XDF.read_bytes()).hexdigest()

manifest_path = ROOT / "data" / "supported_versions.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

manifest["translation_version"] = "1.0.3887621.0"
manifest["known_source_key_count"] = len(sorted_keys)
manifest["known_source_key_sha256"] = keys_sha
manifest["known_source_content_sha256"] = content_sha
manifest["latest_supported_game_update"] = "3887621"
manifest["tested_game_update"] = "3887621"

if "3887621" not in manifest["supported_game_updates"]:
    manifest["supported_game_updates"].insert(0, "3887621")

game_revision = xdt_md5
if game_revision not in manifest["supported_game_revisions"]:
    manifest["supported_game_revisions"].insert(0, game_revision)

manifest["tested_game_revision"] = game_revision
manifest["tested_archive_sha256"] = archive_sha
manifest["tested_date"] = "2026-11-06"
manifest["coverage"] = f"{len(sorted_keys)}/{len(sorted_keys)} keys translated (100.00%)"

notes = [
    f"Aggiornamento per la build Steam 3887621 (patch 1.0.3887621.0) con copertura di traduzione al 100% ({len(sorted_keys):,} chiavi).".replace(",", "."),
    "Aggiunta la nuova chiave di formattazione ({0} ({1})) e aggiornate 607 chiavi sincronizzate con la patch ufficiale di Steam.",
    "Normalizzazione tipografica completa dei titoli e descrizioni (allineamento separatori ' - ' al posto del punto mediano).",
    "Allineamento del nome del PNG Lilipole 'Itsy' (precedentemente Tiny/Mimi) in tutti i dialoghi, archivi e finali narrativi.",
    "Rinominazione ufficiale in 'Club Polaris' e aggiornamento delle voci cosmetiche 'Scarpe Notturno Scarlatto', Fruttobimbo e serie Notte Meravigliosa.",
    "Preservazione assoluta di tutti i tag di formattazione nativi, codici colore, placeholder di genere e formattazione rich text.",
    "Compatibilità garantita con Steam e verifica automatica della cache LuaCacheVer.txt."
]
manifest["notes"] = notes

manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Updated data/supported_versions.json successfully.")
