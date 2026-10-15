import csv
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
XDF = Path(r"D:\SteamLibrary\steamapps\common\Aniimo\Aniimo_Data\StreamingAssets\cvs\res\lua\LuaScripts.xdf")

# 1. Load official English records from 3732728 LuaScripts.xdf
with zipfile.ZipFile(XDF, "r") as zf:
    mapping = json.loads(zf.read("xfs/luascripts/Data/I18N/NewTextMap_en.json").decode("utf-8-sig"))
    bin_data = zf.read("xfs/luascripts/Data/I18N/Compress_en.bin")

official_en = {}
for k, v in mapping.items():
    if not str(k).startswith("_") and isinstance(v, list) and len(v) == 2:
        off, length = int(v[0]), int(v[1])
        text = bin_data[off : off + length].decode("utf-8", errors="replace")
        official_en[str(k)] = text

print(f"Loaded {len(official_en)} official English strings from build 3732728.")

# 2. Translations for new and modified strings
translations = {
    # --- 59 New Keys ---
    "1089256227": "Asso delle Indagini",
    "1101141400": "Accessorio Personaggio",
    "1114413425": "Ascolta attentamente ogni eco e cogli le tracce più deboli nel minimo movimento.",
    "1152662903": "Seleziona la Combo Uno",
    "1177876508": "Valutaci",
    "1186452011": "Deduzione Brillante",
    "1216823337": "Parte Superiore",
    "1229116354": "Premi per vedere tutti gli arredi richiesti per la combo attuale",
    "1233057965": "Orecchie da Pipistrello Spione",
    "1242312851": "Tuckin Omega",
    "1255862541": "Premi un arredo per aprire direttamente il Negozio di Arredamento e acquistarlo",
    "1283346504": "Vestito per la caccia con ali di pipistrello, pronto a svelare i misteri della notte.",
    "1291654185": "Treccia della Lucidità",
    "1304666202": "Nuovo Aspetto",
    "1334454703": "Accessorio Personaggio",
    "1344308465": "Acconciatura",
    "1346488118": "Sconfiggi Glynsera Omega",
    "1351708255": "Sguardo del Detective",
    "1360171542": "Scarpe",
    "1361790482": "Gentile Esploratore, congratulazioni per aver ottenuto un Aniimo raro! Lascia la tua recensione~",
    "1362055313": "Deduzione Elementare",
    "1367754137": "Batlock Holmes",
    "1379255808": "Acconciatura",
    "1397659451": "Guanti",
    "1409174186": "Infergon Omega",
    "1416996360": "Seleziona la combo [<style=Hint_BgL>Raduno della Luna del Raccolto - Insieme</style>]",
    "1466795842": "Batteria ad Alta Capacità",
    "1494631509": "Gentile Esploratore, ehm... se pensi che non siamo male, potresti... magari lasciare una recensione?",
    "1573112683": "Magnifico Gufo Notturno",
    "1579772684": "Esci dalla schermata di gestione e vedrai che l'Aniimo è stato collocato nella tua Base.",
    "1594762494": "Deduzione Brillante",
    "1604604561": "Dissipa la nebbia e guarda oltre ogni falsa apparenza.",
    "1612259046": "Tutto in ordine, idee ben chiare.",
    "1616183857": "Nuovo",
    "1668211018": "Acconciatura",
    "1723622319": "Infergon Omega",
    "1727841686": "Esci dal posizionamento.",
    "1754780104": "Dopo aver usato una Suprema, aumenta l'efficienza di guadagno dei Punti Suprema del 30% per 10s.",
    "1819329071": "Un lampo d'intuizione, e la soluzione si rivela all'improvviso.",
    "1835835687": "Nuovo Aspetto",
    "1839578158": "Premi la categoria [<style=Hint_BgL>Combo di Sistema</style>]",
    "1873802669": "Ogni passo fa parte del piano.",
    "1886944877": "Vai agli Arredi",
    "1891473383": "Visualizza Dettagli",
    "1898043644": "Traccia di Mistero",
    "1905052105": "BOSS Infergon",
    "1924385647": "Infergon Omega",
    "1951636312": "Sherro Omega",
    "1965233514": "Parte Inferiore",
    "1974177711": "Set",
    "1984219768": "Un lampo d'intuizione, e la soluzione si rivela all'improvviso.",
    "2020038009": "Elimina l'impossibile, e la verità si rivelerà da sé.",
    "2053668453": "Astra - Messaggio inviato dopo aver speso 1.000 Monete Voxel",
    "2059163769": "Batlock Holmes",
    "2075432062": "Nuovo",
    "2105202329": "Categoria Combo di Sistema",
    "2116283630": "Non lasciarti mai sfuggire neppure il minimo indizio.",
    "2131489598": "Stile da Detective",
    "2147361329": "Svela ogni strato di finzione e raggiungi la verità nascosta.",

    # --- Modified Keys with Targeted Updates ---
    "1272340979": "Teletrasporto Pebbling",
    "1341319319": "Teletrasporto Pebbling",
    "1343470307": "Teletrasporto Pebbling",
    "1456972409": "Teletrasporto Pebbling",
    "1115523963": "Premi la scheda [<style=Hint_BgL>Combo</style>]",
    "1338607093": "Premi la scheda [<style=Hint_BgL>Combo</style>]",
    "1278602113": "Scheda Combo",
    "1573303586": "Scheda Combo",
    "1589717268": "L'energia della Vena a Breezy Plains è più intensa che mai! Tutti e quattro gli Aniimo Prismana esclusivi della stagione appariranno contemporaneamente nelle rispettive aree. Partecipa al Carnevale Prismana!",
    "1879362901": "L'energia della Vena a Breezy Plains è più intensa che mai! Tutti e quattro gli Aniimo Prismana esclusivi della stagione appariranno contemporaneamente nelle rispettive aree. Partecipa al Carnevale Prismana!",
    "1112729150": "Premi #kRaw/GamepadButtonNorth#z per posizionare nella Base un Aniimo dal Deposito Aniimo.",
    "1113979452": "Forma Prismana",
    "1144549965": "Categoria Combo di Sistema",
    "1206283316": "Valuta insufficiente.",
    "1251654036": "Premi X.",
    "1252420127": "Infergon Omega",
    "1256259436": "Usa #kRaw/GamepadLeftStickMove#z per selezionare un Aniimo, poi premi #kRaw/GamepadButtonSouth#z per confermare.",
    "1280384982": "Seleziona un Aniimo dal Deposito Aniimo e premi #kRaw/GamepadButtonNorth#z per posizionarlo nella Base.",
    "1287905195": "Posiziona Aniimo.",
    "1389133708": "Rookey Alpha",
    "1456185337": "Forma Regionale",
    "1564582836": "Premi #kRaw/GamepadButtonWest#z per aprire la Selezione Aniimo.",
    "1626616525": "Tuckin Omega",
    "1719548120": "Seleziona [<style=Hint_BgL>Zona di Costruzione della Base</style>]",
    "1728154020": "Sherro Omega",
    "1814306880": "Premi #kRaw/GamepadButtonWest#z per aprire l'Elenco Arredi.",
    "1836146096": "Sblocca l'avatar di Hexxin in Forma Prismana",
    "1866189359": "Premi la categoria [<style=Hint_BgL>Combo di Sistema</style>]",
    "1875608920": "Apri Costruisci.",
    "1897787096": "Equipaggia",
    "1965613211": "Aniimo",
    "1968302307": "<style=Hint_BgL>Trascina</style> un Aniimo dal Deposito Aniimo alla tua Base.",
    "1999534500": "Qui puoi vedere la distribuzione dei tag aspetto degli Aniimo della Base <style=Hint_BgL>che ricevono un bonus alla velocità di produzione dei Biglietti Germoglio</style>.",
    "2067440248": "Seleziona Zona di Costruzione della Base",
    "2127733083": "Premi [<style=Hint_BgL>Costruisci</style>] per aprire Costruzione della Base",
    "522470726": "Jiff di Super Artiglio sembra cercare aiuto...",
}

# 3. Load existing translation_it.csv
csv_path = ROOT / "data" / "translation_it.csv"
with csv_path.open("r", encoding="utf-8", newline="") as f:
    existing_rows = list(csv.DictReader(f))

old_catalog = {row["key"]: row for row in existing_rows}
new_catalog = {}

# 4. Populate new catalog with official keys from build 3732728
for key, en_text in official_en.items():
    source_sha = hashlib.sha256(en_text.encode("utf-8")).hexdigest()
    if key in translations:
        new_catalog[key] = {
            "key": key,
            "source_sha256": source_sha,
            "it": translations[key],
        }
    elif en_text == "Character Accessory":
        new_catalog[key] = {
            "key": key,
            "source_sha256": source_sha,
            "it": "Accessorio Personaggio",
        }
    elif key in old_catalog:
        new_catalog[key] = {
            "key": key,
            "source_sha256": source_sha,
            "it": old_catalog[key]["it"],
        }
    else:
        raise ValueError(f"Missing translation for new key: {key}")

sorted_keys = sorted(new_catalog.keys(), key=lambda x: int(x) if x.isdigit() else 999999999)
print(f"Total catalog entries after update: {len(sorted_keys)}")

# Write updated translation_it.csv
with csv_path.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["key", "source_sha256", "it"])
    writer.writeheader()
    for k in sorted_keys:
        writer.writerow(new_catalog[k])

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

manifest["translation_version"] = "1.0.3732728.0"
manifest["known_source_key_count"] = len(sorted_keys)
manifest["known_source_key_sha256"] = keys_sha
manifest["known_source_content_sha256"] = content_sha
manifest["latest_supported_game_update"] = "3732728"
manifest["tested_game_update"] = "3732728"

if "3732728" not in manifest["supported_game_updates"]:
    manifest["supported_game_updates"].insert(0, "3732728")

revision = "56fd90cbd9dee22164aa1c7912e4adda"
if revision not in manifest["supported_game_revisions"]:
    manifest["supported_game_revisions"].insert(0, revision)

manifest["tested_game_revision"] = revision
manifest["tested_archive_sha256"] = archive_sha
manifest["coverage"] = f"{len(sorted_keys)}/{len(sorted_keys)} keys translated (100.00%)"

manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Updated data/supported_versions.json successfully.")
