import csv
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
XDF = Path(r"D:\SteamLibrary\steamapps\common\Aniimo\Aniimo_Data\StreamingAssets\cvs\res\lua\LuaScripts.xdf")

# 1. Load official English records from 3743667 LuaScripts.xdf
with zipfile.ZipFile(XDF, "r") as zf:
    mapping = json.loads(zf.read("xfs/luascripts/Data/I18N/NewTextMap_en.json").decode("utf-8-sig"))
    bin_data = zf.read("xfs/luascripts/Data/I18N/Compress_en.bin")

official_en = {}
for k, v in mapping.items():
    if not str(k).startswith("_") and isinstance(v, list) and len(v) == 2:
        off, length = int(v[0]), int(v[1])
        text = bin_data[off : off + length].decode("utf-8", errors="replace")
        official_en[str(k)] = text

print(f"Loaded {len(official_en)} official English strings from build 3743667.")

# 2. Translations for new and modified strings
translations = {
    # --- 53 New Keys ---
    "1120746848": "12",
    "1122265592": "Può essere usato per personalizzare il tuo personaggio e i tuoi Aniimo.",
    "1137237960": "11",
    "1190430899": "Accessorio Aniimo",
    "1213998986": "La domanda è profonda, ma la risposta è vaga.",
    "1255600189": "BINI #2333",
    "1265985987": "Dopo aver ottenuto il pacchetto precedente, sblocca il successivo in ordine!",
    "1269861010": "Acquistato",
    "1284329308": "Più grande è la goccia di sudore, più imbarazzante è la situazione.",
    "1298091851": "Sudore Tattico",
    "1311041047": "A Scaglioni",
    "1320154556": "La domanda è profonda, ma la risposta è vaga.",
    "1321943020": "Tempo Rimanente",
    "1422274780": "Grandi Doni a Scaglioni",
    "1435983298": "6",
    "1481632768": "3",
    "1526018201": "La rabbia sale, ma non ha ancora raggiunto il punto di ebollizione.",
    "1581206194": "Stizzito",
    "1589968924": "1",
    "1590557182": "Sudore Tattico",
    "1600334700": "Può essere usato per personalizzare il tuo personaggio e i tuoi Aniimo.",
    "1605039397": "Accessorio Personaggio",
    "1606930419": "Domanda Profonda",
    "1614357308": "Più grande è la goccia di sudore, più imbarazzante è la situazione.",
    "1630725074": "Accessorio Personaggio",
    "1670884947": "Accessorio Aniimo",
    "1686679726": "10",
    "1705542431": "Accessorio Aniimo",
    "1748320706": "7",
    "1771918047": "Questo Forziere è già stato aperto da qualcun altro.",
    "1773552001": "La rabbia sale, ma non ha ancora raggiunto il punto di ebollizione.",
    "1804508765": "Puoi scegliere come ricompensa uno degli Oggetti Tenuti di <style=Q_5>qualità Leggendaria</style>.",
    "1809824516": "2",
    "1817530490": "Sudore Tattico",
    "1830902283": "Stizzito",
    "1874288694": "L'elenco degli Oggetti Tenuti Leggendari è il seguente. Dopo l'apertura, puoi sceglierne 1.",
    "1912374974": "Domanda Profonda",
    "1916663079": "13",
    "1921287871": "9",
    "1948201211": "Più grande è la goccia di sudore, più imbarazzante è la situazione.",
    "1949848847": "Ricompense evento [Raduno del Raccolto]",
    "1956512465": "8",
    "1968913411": "Stizzito",
    "1977578303": "Può essere usato per personalizzare il tuo personaggio e i tuoi Aniimo.",
    "1987891497": "Domanda Profonda",
    "2008078191": "Bonus attivo: la quota di ESP ottenuta al di sotto del livello 70 è raddoppiata.",
    "2017747455": "La rabbia sale, ma non ha ancora raggiunto il punto di ebollizione.",
    "2033928783": "Selezione Oggetto Tenuto Leggendario",
    "2042984747": "5",
    "2075736765": "4",
    "2096806606": "Accessorio Personaggio",
    "2117702185": "La domanda è profonda, ma la risposta è vaga.",
    "2118802929": "Gentile Esploratore, grazie per aver ospitato con entusiasmo il Raduno del Raccolto. Le ricompense per aver ospitato il Raduno del Raccolto ti sono state consegnate.",

    # --- Modified Keys ---
    "1106614039": "I turni preliminari di Glamour Star sono ora aperti! In base al tema attuale, scegli l'outfit perfetto per il tuo Aniimo e punta a un punteggio elevato con la valutazione della tua Onda d'Urto per diventare la stella più brillante!",
    "1260998194": "I turni preliminari di Glamour Star sono ora aperti! In base al tema attuale, scegli l'outfit perfetto per il tuo Aniimo e punta a un punteggio elevato con la valutazione della tua Onda d'Urto per diventare la stella più brillante!",
    "1926564502": "I turni preliminari di Glamour Star sono ora aperti! In base al tema attuale, scegli l'outfit perfetto per il tuo Aniimo e punta a un punteggio elevato con la valutazione della tua Onda d'Urto per diventare la stella più brillante!",
    "1144698079": "Un dispositivo per <style=Hint_BgD>catturare</style>, <style=Hint_BgD>portare con sé</style> e <style=Hint_BgD>allenare</style> gli <style=Hint_BgD>Aniimo</style>.\nAl suo interno, la tecnologia di ripiegamento spaziale offre agli Aniimo un comodo spazio in cui riposare.",
    "1713412633": "Un dispositivo per <style=Hint_BgD>catturare</style>, <style=Hint_BgD>portare con sé</style> e <style=Hint_BgD>allenare</style> gli <style=Hint_BgD>Aniimo</style>.\nAl suo interno, la tecnologia di ripiegamento spaziale offre agli Aniimo un comodo spazio in cui riposare.",
    "1581724593": "Stadio Lumin",
    "1725249255": "Ambra del Sogno di Farfalla",
    "1788967467": "Ambra del Sogno di Farfalla",
    "1238937410": "Voce Esploratore",
    "1198162648": "1. Una volta iniziato l'evento, il Polaris Institute annuncerà il tema dell'audizione per Glamour Star.\n2. Gli Esploratori possono scegliere Aniimo adatti e abbinarli ad Accessori in base al tema attuale per completare la registrazione all'evento.\n3. L'Istituto assegnerà un punteggio agli Aniimo partecipanti in base a quanto gli Aniimo e gli Accessori si adattano al tema.\n4. Quando il punteggio di un Esploratore raggiunge il traguardo richiesto, può riscattare la ricompensa corrispondente.\n5. È possibile partecipare a ciascun turno di Glamour Star più volte, ma ogni ricompensa può essere riscattata una sola volta e non può essere ottenuta ripetutamente.",
    "1397639221": "1. Una volta iniziato l'evento, il Polaris Institute annuncerà il tema dell'audizione per Glamour Star.\n2. Gli Esploratori possono scegliere Aniimo adatti e abbinarli ad Accessori in base al tema attuale per completare la registrazione all'evento.\n3. L'Istituto assegnerà un punteggio agli Aniimo partecipanti in base a quanto gli Aniimo e gli Accessori si adattano al tema.\n4. Quando il punteggio di un Esploratore raggiunge il traguardo richiesto, può riscattare la ricompensa corrispondente.\n5. È possibile partecipare a ciascun turno di Glamour Star più volte, ma ogni ricompensa può essere riscattata una sola volta e non può essere ottenuta ripetutamente.",
    "1399285160": "1. Una volta iniziato l'evento, il Polaris Institute annuncerà il tema dell'audizione per Glamour Star.\n2. Gli Esploratori possono scegliere Aniimo adatti e abbinarli ad Accessori in base al tema attuale per completare la registrazione all'evento.\n3. L'Istituto assegnerà un punteggio agli Aniimo partecipanti in base a quanto gli Aniimo e gli Accessori si adattano al tema.\n4. Quando il punteggio di un Esploratore raggiunge il traguardo richiesto, può riscattare la ricompensa corrispondente.\n5. È possibile partecipare a ciascun turno di Glamour Star più volte, ma ogni ricompensa può essere riscattata una sola volta e non può essere ottenuta ripetutamente.",
    "1630468949": "1. Una volta iniziato l'evento, il Polaris Institute annuncerà il tema dell'audizione per Glamour Star.\n2. Gli Esploratori possono scegliere Aniimo adatti e abbinarli ad Accessori in base al tema attuale per completare la registrazione all'evento.\n3. L'Istituto assegnerà un punteggio agli Aniimo partecipanti in base a quanto gli Aniimo e gli Accessori si adattano al tema.\n4. Quando il punteggio di un Esploratore raggiunge il traguardo richiesto, può riscattare la ricompensa corrispondente.\n5. È possibile partecipare a ciascun turno di Glamour Star più volte, ma ogni ricompensa può essere riscattata una sola volta e non può essere ottenuta ripetutamente.",
    "1725451892": "1. Una volta iniziato l'evento, il Polaris Institute annuncerà il tema dell'audizione per Glamour Star.\n2. Gli Esploratori possono scegliere Aniimo adatti e abbinarli ad Accessori in base al tema attuale per completare la registrazione all'evento.\n3. L'Istituto assegnerà un punteggio agli Aniimo partecipanti in base a quanto gli Aniimo e gli Accessori si adattano al tema.\n4. Quando il punteggio di un Esploratore raggiunge il traguardo richiesto, può riscattare la ricompensa corrispondente.\n5. È possibile partecipare a ciascun turno di Glamour Star più volte, ma ogni ricompensa può essere riscattata una sola volta e non può essere ottenuta ripetutamente.",
    "1728989437": "1. Una volta iniziato l'evento, il Polaris Institute annuncerà il tema dell'audizione per Glamour Star.\n2. Gli Esploratori possono scegliere Aniimo adatti e abbinarli ad Accessori in base al tema attuale per completare la registrazione all'evento.\n3. L'Istituto assegnerà un punteggio agli Aniimo partecipanti in base a quanto gli Aniimo e gli Accessori si adattano al tema.\n4. Quando il punteggio di un Esploratore raggiunge il traguardo richiesto, può riscattare la ricompensa corrispondente.\n5. È possibile partecipare a ciascun turno di Glamour Star più volte, ma ogni ricompensa può essere riscattata una sola volta e non può essere ottenuta ripetutamente.",
    "1808089158": "1. Una volta iniziato l'evento, il Polaris Institute annuncerà il tema dell'audizione per Glamour Star.\n2. Gli Esploratori possono scegliere Aniimo adatti e abbinarli ad Accessori in base al tema attuale per completare la registrazione all'evento.\n3. L'Istituto assegnerà un punteggio agli Aniimo partecipanti in base a quanto gli Aniimo e gli Accessori si adattano al tema.\n4. Quando il punteggio di un Esploratore raggiunge il traguardo richiesto, può riscattare la ricompensa corrispondente.\n5. È possibile partecipare a ciascun turno di Glamour Star più volte, ma ogni ricompensa può essere riscattata una sola volta e non può essere ottenuta ripetutamente.",
    "1820237724": "1. Una volta iniziato l'evento, il Polaris Institute annuncerà il tema dell'audizione per Glamour Star.\n2. Gli Esploratori possono scegliere Aniimo adatti e abbinarli ad Accessori in base al tema attuale per completare la registrazione all'evento.\n3. L'Istituto assegnerà un punteggio agli Aniimo partecipanti in base a quanto gli Aniimo e gli Accessori si adattano al tema.\n4. Quando il punteggio di un Esploratore raggiunge il traguardo richiesto, può riscattare la ricompensa corrispondente.\n5. È possibile partecipare a ciascun turno di Glamour Star più volte, ma ogni ricompensa può essere riscattata una sola volta e non può essere ottenuta ripetutamente.",
    "1831638158": "1. Una volta iniziato l'evento, il Polaris Institute annuncerà il tema dell'audizione per Glamour Star.\n2. Gli Esploratori possono scegliere Aniimo adatti e abbinarli ad Accessori in base al tema attuale per completare la registrazione all'evento.\n3. L'Istituto assegnerà un punteggio agli Aniimo partecipanti in base a quanto gli Aniimo e gli Accessori si adattano al tema.\n4. Quando il punteggio di un Esploratore raggiunge il traguardo richiesto, può riscattare la ricompensa corrispondente.\n5. È possibile partecipare a ciascun turno di Glamour Star più volte, ma ogni ricompensa può essere riscattata una sola volta e non può essere ottenuta ripetutamente.",
    "1852029162": "1. Una volta iniziato l'evento, il Polaris Institute annuncerà il tema dell'audizione per Glamour Star.\n2. Gli Esploratori possono scegliere Aniimo adatti e abbinarli ad Accessori in base al tema attuale per completare la registrazione all'evento.\n3. L'Istituto assegnerà un punteggio agli Aniimo partecipanti in base a quanto gli Aniimo e gli Accessori si adattano al tema.\n4. Quando il punteggio di un Esploratore raggiunge il traguardo richiesto, può riscattare la ricompensa corrispondente.\n5. È possibile partecipare a ciascun turno di Glamour Star più volte, ma ogni ricompensa può essere riscattata una sola volta e non può essere ottenuta ripetutamente.",
    "1992340295": "1. Una volta iniziato l'evento, il Polaris Institute annuncerà il tema dell'audizione per Glamour Star.\n2. Gli Esploratori possono scegliere Aniimo adatti e abbinarli ad Accessori in base al tema attuale per completare la registrazione all'evento.\n3. L'Istituto assegnerà un punteggio agli Aniimo partecipanti in base a quanto gli Aniimo e gli Accessori si adattano al tema.\n4. Quando il punteggio di un Esploratore raggiunge il traguardo richiesto, può riscattare la ricompensa corrispondente.\n5. È possibile partecipare a ciascun turno di Glamour Star più volte, ma ogni ricompensa può essere riscattata una sola volta e non può essere ottenuta ripetutamente.",
    "2079298497": "1. Una volta iniziato l'evento, il Polaris Institute annuncerà il tema dell'audizione per Glamour Star.\n2. Gli Esploratori possono scegliere Aniimo adatti e abbinarli ad Accessori in base al tema attuale per completare la registrazione all'evento.\n3. L'Istituto assegnerà un punteggio agli Aniimo partecipanti in base a quanto gli Aniimo e gli Accessori si adattano al tema.\n4. Quando il punteggio di un Esploratore raggiunge il traguardo richiesto, può riscattare la ricompensa corrispondente.\n5. È possibile partecipare a ciascun turno di Glamour Star più volte, ma ogni ricompensa può essere riscattata una sola volta e non può essere ottenuta ripetutamente.",
}

# 3. Load existing translation_it.csv
csv_path = ROOT / "data" / "translation_it.csv"
with csv_path.open("r", encoding="utf-8", newline="") as f:
    existing_rows = list(csv.DictReader(f))

old_catalog = {row["key"]: row for row in existing_rows}
new_catalog = {}

# 4. Populate new catalog with official keys from build 3743667
for key, en_text in official_en.items():
    source_sha = hashlib.sha256(en_text.encode("utf-8")).hexdigest()
    if key in translations:
        new_catalog[key] = {
            "key": key,
            "source_sha256": source_sha,
            "it": translations[key],
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

manifest["translation_version"] = "1.0.3743667.0"
manifest["known_source_key_count"] = len(sorted_keys)
manifest["known_source_key_sha256"] = keys_sha
manifest["known_source_content_sha256"] = content_sha
manifest["latest_supported_game_update"] = "3743667"
manifest["tested_game_update"] = "3743667"

if "3743667" not in manifest["supported_game_updates"]:
    manifest["supported_game_updates"].insert(0, "3743667")

# Game revision from verlist.txt: 3743667,a482c47cf649a6c1053854cfc09fde42,2615345
revision = "a482c47cf649a6c1053854cfc09fde42"
if revision not in manifest["supported_game_revisions"]:
    manifest["supported_game_revisions"].insert(0, revision)

manifest["tested_game_revision"] = revision
manifest["tested_archive_sha256"] = archive_sha
manifest["coverage"] = f"{len(sorted_keys)}/{len(sorted_keys)} keys translated (100.00%)"

manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Updated data/supported_versions.json successfully.")
