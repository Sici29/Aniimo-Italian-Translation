import csv
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
XDF = Path(r"D:\SteamLibrary\steamapps\common\Aniimo\Aniimo_Data\StreamingAssets\cvs\res\lua\LuaScripts.xdf")

# 1. Load official English records from 3634150 LuaScripts.xdf
with zipfile.ZipFile(XDF, "r") as zf:
    mapping = json.loads(zf.read("xfs/luascripts/Data/I18N/NewTextMap_en.json").decode("utf-8-sig"))
    bin_data = zf.read("xfs/luascripts/Data/I18N/Compress_en.bin")

official_en = {}
for k, v in mapping.items():
    if not str(k).startswith("_") and isinstance(v, list) and len(v) == 2:
        off, length = int(v[0]), int(v[1])
        text = bin_data[off : off + length].decode("utf-8", errors="replace")
        official_en[str(k)] = text

print(f"Loaded {len(official_en)} official English strings from build 3634150.")

# 2. Translations for new and modified strings
translations = {
    # 1 New key
    "1389687126": "Ho fatto centro nel Tessiluce con un'unica estrazione! Condivido la mia fortuna con te!",

    # 15 Modified keys
    "1217240679": "Gentile Esploratore,\nabbiamo riscontrato che il tuo avatar conteneva contenuti inappropriati e verrà ripristinato a quello predefinito. Se ritieni che si tratti di un errore, puoi contattare l'Assistenza all'interno del gioco per presentare ricorso.\nAniimo è un luogo per tutti, e mantenerlo tale è qualcosa che facciamo insieme. Grazie per aiutarci a prenderci cura di questo mondo.",
    "1389256099": "Un biglietto necessario per accedere a <style=Hint_BgL>Operazione: Furto d'Uova - Modalità Squadra (Caos)</style>.",
    "1413960612": "Gentile Esploratore,\nabbiamo riscontrato che il tuo soprannome conteneva contenuti inappropriati, in violazione del nostro Accordo Utente. Verrà sostituito con uno temporaneo. Se ritieni che si tratti di un errore, puoi contattare l'Assistenza all'interno del gioco per presentare ricorso.\nAniimo è un luogo per tutti, e mantenerlo tale è qualcosa che facciamo insieme. Grazie per aiutarci a prenderci cura di questo mondo.",
    "1517065207": "Gentile Esploratore,\nabbiamo riscontrato che le decorazioni della tua Area Camper contenevano contenuti inappropriati, in violazione del nostro Accordo Utente. Verranno ripristinate allo stato predefinito dal sistema. Se ritieni che si tratti di un errore, puoi contattare l'Assistenza all'interno del gioco per presentare ricorso.\nAniimo è un luogo per tutti, e mantenerlo tale è qualcosa che facciamo insieme. Grazie per aiutarci a prenderci cura di questo mondo.",
    "1535078881": "Apri menu radiale",
    "1555622696": "Tu? Sfidare me? Neanche per sogno. Io voglio sconfiggere un <style=Hint_BgD>Cozite</style>! Torna più tardi e ti metterò in lista d'attesa!",
    "1559853906": "Gentile Esploratore,\nabbiamo riscontrato che la tua biografia conteneva contenuti inappropriati e verrà cancellata. Se ritieni che si tratti di un errore, puoi contattare l'Assistenza all'interno del gioco per presentare ricorso.\nAniimo è un luogo per tutti, e mantenerlo tale è qualcosa che facciamo insieme. Grazie per aiutarci a prenderci cura di questo mondo.",
    "1572123256": "Gentile Esploratore,\nabbiamo riscontrato che la tua Base conteneva contenuti inappropriati e le visite alla tua Base verranno limitate. Se ritieni che si tratti di un errore, puoi contattare l'Assistenza all'interno del gioco per presentare ricorso.\nAniimo è un luogo per tutti, e mantenerlo tale è qualcosa che facciamo insieme. Grazie per aiutarci a prenderci cura di questo mondo.",
    "1634086377": "Gentile Esploratore,\nabbiamo riscontrato che il nome della tua Base conteneva contenuti inappropriati e verrà sostituito con uno temporaneo. In seguito potrai impostarne uno nuovo. Se ritieni che si tratti di un errore, puoi contattare l'Assistenza all'interno del gioco per presentare ricorso.\nAniimo è un luogo per tutti, e mantenerlo tale è qualcosa che facciamo insieme. Grazie per aiutarci a prenderci cura di questo mondo.",
    "1788967467": "Bosco delle Farfalle del Sogno",
    "1955621065": "In seguito alle segnalazioni di altri Esploratori, abbiamo riscontrato che il tuo avatar conteneva contenuti inappropriati e verrà ripristinato a quello predefinito. In seguito potrai caricarne uno nuovo.\nSe ritieni che si tratti di un errore, puoi contattare l'Assistenza all'interno del gioco per presentare ricorso.\nAniimo è un luogo per tutti, e mantenerlo tale è qualcosa che facciamo insieme. Grazie per aiutarci a prenderci cura di questo mondo.",
    "1981873814": "In seguito alle segnalazioni di altri Esploratori, abbiamo riscontrato che il tuo soprannome conteneva contenuti inappropriati e verrà sostituito con uno temporaneo. In seguito potrai impostarne uno nuovo.\nSe ritieni che si tratti di un errore, puoi contattare l'Assistenza all'interno del gioco per presentare ricorso.\nAniimo è un luogo per tutti, e mantenerlo tale è qualcosa che facciamo insieme. Grazie per aiutarci a prenderci cura di questo mondo.",
    "2002478505": "Gentile Esploratore,\nabbiamo riscontrato che il tuo modello per lo studio fotografico conteneva contenuti inappropriati, in violazione del nostro Accordo Utente. Verrà ripristinato allo stato predefinito dal sistema. Se ritieni che si tratti di un errore, puoi contattare l'Assistenza all'interno del gioco per presentare ricorso.\nAniimo è un luogo per tutti, e mantenerlo tale è qualcosa che facciamo insieme. Grazie per aiutarci a prenderci cura di questo mondo.",
    "2047945200": "Gentile Esploratore,\nabbiamo riscontrato che il tuo modello fotografico conteneva contenuti inappropriati e verrà ripristinato a quello predefinito. Se ritieni che si tratti di un errore, puoi contattare l'Assistenza all'interno del gioco per presentare ricorso.\nAniimo è un luogo per tutti, e mantenerlo tale è qualcosa che facciamo insieme. Grazie per aiutarci a prenderci cura di questo mondo.",
    "2104282187": "Gentile Esploratore,\nabbiamo riscontrato che i lotti della tua Base contenevano contenuti inappropriati, in violazione del nostro Accordo Utente. Verranno ripristinati allo stato predefinito dal sistema. Se ritieni che si tratti di un errore, puoi contattare l'Assistenza all'interno del gioco per presentare ricorso.\nAniimo è un luogo per tutti, e mantenerlo tale è qualcosa che facciamo insieme. Grazie per aiutarci a prenderci cura di questo mondo.",
}

# 3. Load existing translation_it.csv
csv_path = ROOT / "data" / "translation_it.csv"
with csv_path.open("r", encoding="utf-8", newline="") as f:
    existing_rows = list(csv.DictReader(f))

catalog = {row["key"]: row for row in existing_rows}

# 4. Update catalog with new/modified entries
for key, en_text in official_en.items():
    source_sha = hashlib.sha256(en_text.encode("utf-8")).hexdigest()
    if key in translations:
        catalog[key] = {
            "key": key,
            "source_sha256": source_sha,
            "it": translations[key],
        }
    elif key in catalog:
        catalog[key]["source_sha256"] = source_sha
    else:
        raise ValueError(f"Missing translation for new key: {key}")

sorted_keys = sorted(catalog.keys(), key=lambda x: int(x) if x.isdigit() else 999999999)
print(f"Total catalog entries after update: {len(sorted_keys)}")

# Write updated translation_it.csv
with csv_path.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["key", "source_sha256", "it"])
    writer.writeheader()
    for k in sorted_keys:
        writer.writerow(catalog[k])

print("Updated data/translation_it.csv successfully.")

# 5. Compute manifest hashes
sys_path = ROOT / "tools"
import sys
sys.path.insert(0, str(sys_path))
import aniimo_it_installer as inst

keys_sha = inst.sha256_keys(sorted_keys)
content_sha = inst.sha256_keyed_text(official_en)
archive_sha = hashlib.sha256(XDF.read_bytes()).hexdigest()

print(f"known_source_key_sha256: {keys_sha}")
print(f"known_source_content_sha256: {content_sha}")
print(f"tested_archive_sha256: {archive_sha}")

# 6. Update data/supported_versions.json
manifest_path = ROOT / "data" / "supported_versions.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

manifest["translation_version"] = "1.0.3634150.0"
manifest["known_source_key_count"] = len(sorted_keys)
manifest["known_source_key_sha256"] = keys_sha
manifest["known_source_content_sha256"] = content_sha
manifest["latest_supported_game_update"] = "3634150"

if "3634150" not in manifest["supported_game_updates"]:
    manifest["supported_game_updates"].insert(0, "3634150")

revision = "0ac01a330f8a64fc13e86bdaf0afdcb2"
if revision not in manifest["supported_game_revisions"]:
    manifest["supported_game_revisions"].insert(0, revision)

manifest["tested_game_revision"] = revision
manifest["tested_archive_sha256"] = archive_sha

manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Updated data/supported_versions.json successfully.")
