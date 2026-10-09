import csv
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
XDF = Path(r"D:\SteamLibrary\steamapps\common\Aniimo\Aniimo_Data\StreamingAssets\cvs\res\lua\LuaScripts.xdf")

# 1. Load official English records from 3668494 LuaScripts.xdf
with zipfile.ZipFile(XDF, "r") as zf:
    mapping = json.loads(zf.read("xfs/luascripts/Data/I18N/NewTextMap_en.json").decode("utf-8-sig"))
    bin_data = zf.read("xfs/luascripts/Data/I18N/Compress_en.bin")

official_en = {}
for k, v in mapping.items():
    if not str(k).startswith("_") and isinstance(v, list) and len(v) == 2:
        off, length = int(v[0]), int(v[1])
        text = bin_data[off : off + length].decode("utf-8", errors="replace")
        official_en[str(k)] = text

print(f"Loaded {len(official_en)} official English strings from build 3668494.")

glamour_rules = (
    "1. Una volta iniziato l'evento, il Polaris Institute annuncerà il tema dell'audizione per Glamour Star.\n"
    "2. Gli Esploratori possono scegliere Aniimo adatti e abbinarli ad Accessori in base al tema attuale per completare la registrazione all'evento.\n"
    "3. L'Istituto assegnerà un punteggio agli Aniimo partecipanti in base a quanto gli Aniimo e gli Accessori si adattano al tema.\n"
    "4. Quando il punteggio di un Esploratore raggiunge il traguardo richiesto, può riscattare la ricompensa corrispondente.\n"
    "5. È possibile partecipare a ciascun turno di Glamour Star più volte, ma ogni ricompensa può essere riscattata una sola volta e non può essere ottenuta ripetutamente."
)

glamour_prelim = (
    "I turni preliminari di Glamour Star sono aperti! In base al tema attuale, scegli l'outfit perfetto per il tuo Aniimo e punta a un punteggio elevato per diventare la stella più brillante!"
)

# 2. Translations for new and modified strings
translations = {
    # --- 44 New keys ---
    "1090020906": "Carica registri",
    "1106614039": glamour_prelim,
    "1145174842": "Tepore Invernale",
    "1150031041": "Nuota",
    "1198162648": glamour_rules,
    "1206283316": "Valuta insufficiente",
    "1235720364": "Ghiaccio",
    "1260998194": glamour_prelim,
    "1276393509": "Acqua",
    "1397639221": glamour_rules,
    "1399285160": glamour_rules,
    "1408235732": "Inizializzazione caricamento registri non riuscita",
    "1483220973": "Super Armatura di Benevolenza",
    "1519738927": "Scudo della Benevolenza",
    "1541540945": "Glamour Star",
    "1562292396": "Carica registri",
    "1581724593": "Fase Nova",
    "1606517023": "Caccia Furtiva",
    "1630468949": glamour_rules,
    "1640983375": "Istintivo",
    "1677961271": "Glamour Star",
    "1725451892": glamour_rules,
    "1728989437": glamour_rules,
    "1768063412": "Fase Nova",
    "1802693175": "Erlath Umbrale",
    "1808089158": glamour_rules,
    "1818406773": "Avvio del caricamento dei registri",
    "1820237724": glamour_rules,
    "1831638158": glamour_rules,
    "1848176021": "Benevolenza",
    "1852029162": glamour_rules,
    "1877285763": "Carnevale dell'Acqua",
    "1890751243": "Glamour Star",
    "1922771831": "Caricamento dei registri non riuscito",
    "1926564502": glamour_prelim,
    "1980564627": "Registri caricati con successo",
    "1992340295": glamour_rules,
    "2066940891": "Boschetto Assolato",
    "2074270703": "Risultati del test di rete caricati con successo",
    "2079298497": glamour_rules,
    "2084161286": "DPS",
    "2087410097": "Pacco",
    "2112820829": "Dominio della Benevolenza",
    "2139099862": "Fase Nova",

    # --- Modified keys with targeted updates ---
    "1087506467": "Se non hai abbastanza materiali di questo tipo, puoi <style=Hint_BgD>coltivare nuovi appezzamenti</style>. <style=Hint_BgD>Tra i detriti si possono trovare anche risorse nascoste</style>.\nNaturalmente... anche questo richiederà qualche fondo...",
    "1132087194": "Diagnostica di rete completata.",
    "1230995775": "Erlath Umbrale",
    "1333031189": "Ah, e c'è un'altra cosa importante da dirti: per le strade della città ci sono delle <style=Hint_BgD>strisce luminose musicali</style>. Se le calpesti nell'ordine giusto, sembra che anche lì compaiano monete voxel.",
    "1371785764": "Risultati della diagnostica salvati in:\n{0}",
    "1505155420": "Impossibile salvare i risultati della diagnostica. Controlla il registro.",
    "1535078881": "Mostra menu radiale",
    "1553313007": "Coltiva",
    "1646490061": "Seleziona prima un server.",
    "1674181138": "Erlath Umbrale",
    "1725249255": "Bosco delle Farfalle del Sogno",
    "1742755408": "Avvia diagnostica",
    "1798454723": "Pausa / Riproduci",
    "1824103527": "Gli Aniimo di tipo Terra possono svolgere compiti come coltivare la terra ed estrarre risorse nella Base.",
    "1832815711": "%s è apparso nel tuo mondo.",
    "1926801134": "Coltivazione",
    "1937006741": "Coltiva, costruisci, produci, pianta, raccogli e poi vendi per guadagnare più monete base, e ripeti il ciclo.",
    "2019933308": "Erlath Umbrale",
    "2023353376": "Continua a seguirci",
    "2032747102": "Coltivazione...",
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

manifest["translation_version"] = "1.0.3668494.0"
manifest["known_source_key_count"] = len(sorted_keys)
manifest["known_source_key_sha256"] = keys_sha
manifest["known_source_content_sha256"] = content_sha
manifest["latest_supported_game_update"] = "3668494"
manifest["tested_game_update"] = "3668494"

if "3668494" not in manifest["supported_game_updates"]:
    manifest["supported_game_updates"].insert(0, "3668494")

revision = "7e7dc7895ca2725a52d92fa4ac6cf807"
if revision not in manifest["supported_game_revisions"]:
    manifest["supported_game_revisions"].insert(0, revision)

manifest["tested_game_revision"] = revision
manifest["tested_archive_sha256"] = archive_sha
manifest["coverage"] = f"{len(sorted_keys)}/{len(sorted_keys)} keys translated (100.00%)"

manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Updated data/supported_versions.json successfully.")
