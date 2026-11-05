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

# 1. Load official English records from 3880756 LuaScripts.xdf
with zipfile.ZipFile(XDF, "r") as zf:
    mapping = json.loads(zf.read("xfs/luascripts/Data/I18N/NewTextMap_en.json").decode("utf-8-sig"))
    bin_data = zf.read("xfs/luascripts/Data/I18N/Compress_en.bin")

official_en = {}
for k, v in mapping.items():
    if not str(k).startswith("_") and isinstance(v, list) and len(v) == 2:
        off, length = int(v[0]), int(v[1])
        text = bin_data[off : off + length].decode("utf-8", errors="replace")
        official_en[str(k)] = text

print(f"Loaded {len(official_en)} official English strings from build 3880756.")

# 2. 98 Updated Translations (27 Added + 71 Changed)
updated_translations = {
    # 27 Added keys in build 3880756
    "1113977829": "Dopo lo scollegamento, il tuo account Steam verrà considerato come un nuovo account e tornerai alla schermata di accesso. Potrai collegare nuovamente un indirizzo email. Accedi con l'indirizzo email precedentemente collegato per ritrovare il tuo personaggio originale.",
    "1125344566": "Un fiore che cresce dove si raduna l'energia della Vena. Quando sboccia, attira un gran numero di Aniimo.",
    "1127075140": "Account Epic Games",
    "1206914247": "Account WeGame",
    "1322724649": "Ambra infusa del potere Lumin. I Rami possono assorbirne l'energia per crescere.",
    "1381523871": "Le Sfide dell'Esploratore d'élite sono aperte agli studenti più promettenti dell'Istituto. Ogni sfida ti contrappone a un Esploratore d'élite certificato dall'Istituto con un curriculum straordinario. Superare la prova dimostra la tua forza e ti fa guadagnare un distintivo esclusivo dell'Istituto e risorse rare.",
    "1496395221": "Misteriosi forzieri sono sparsi per Idyll. Potrebbero essere bagagli smarriti da viaggiatori, scorte lasciate da Avventurieri o tesori sigillati da un'antica civiltà... Ognuno di essi attende solo di essere scoperto e aperto.",
    "1522631013": "Dopo lo scollegamento, il tuo account WeGame verrà considerato come un nuovo account e tornerai alla schermata di accesso. Potrai collegare nuovamente un numero di telefono. Accedi con il numero di telefono precedentemente collegato per ritrovare il tuo personaggio originale.",
    "1586371045": "Ambra fuggiasca",
    "1618081308": "Dopo lo scollegamento, il tuo account Epic Games verrà considerato come un nuovo account e tornerai alla schermata di accesso. Potrai collegare nuovamente un indirizzo email. Accedi con l'indirizzo email precedentemente collegato per ritrovare il tuo personaggio originale.",
    "1627580569": "Dopo lo scollegamento, il tuo account Heybox verrà considerato come un nuovo account e tornerai alla schermata di accesso. Potrai collegare nuovamente un numero di telefono. Accedi con il numero di telefono precedentemente collegato per ritrovare il tuo personaggio originale.",
    "1630161481": "Nuovo aspetto",
    "1661267208": "Account Heybox",
    "1815667443": "Raccolta Lumin",
    "1833335534": "Sogno di Fentuft",
    "1865671039": "Misteriosi forzieri sono sparsi per Idyll. Potrebbero essere bagagli smarriti da viaggiatori, scorte lasciate da Avventurieri o tesori sigillati da un'antica civiltà... Ognuno di essi attende solo di essere scoperto e aperto.",
    "1883586541": "Sfida gli Esploratori sparsi per il mondo per ottenere ricompense.",
    "1883800443": "Account Steam",
    "1889403421": "Nuovo",
    "1929421807": "Le antiche statue sembrano nascondere un segreto.",
    "1968330484": "Aiuta l'Aniimo",
    "1976539297": "L'energia di Prismana si è radunata qui, attirando un Aniimo di Prismana.",
    "2015413285": "Attiva il Ramo prima di nutrire il Fiore della Vena.",
    "2017482451": "Account TapTap",
    "2019689745": "Dopo lo scollegamento, il tuo account TapTap verrà considerato come un nuovo account e tornerai alla schermata di accesso. Potrai collegare nuovamente un numero di telefono. Accedi con il numero di telefono precedentemente collegato per ritrovare il tuo personaggio originale.",
    "2043141305": "Avventurati nelle profondità delle antiche rovine alla ricerca del Respiro delle Vene",
    "2111557614": "Le Sfide dell'Esploratore d'élite sono aperte agli studenti più promettenti dell'Istituto. Ogni sfida ti contrappone a un Esploratore d'élite certificato dall'Istituto con un curriculum straordinario. Superare la prova dimostra la tua forza e ti fa guadagnare un distintivo esclusivo dell'Istituto e risorse rare.",

    # 71 Changed keys in build 3880756
    "289172187": "Posiziona il Barattolo delle Stelle dei Desideri nell'Area Residenziale.",
    "303065263": "Possiedi 1 Aniimo con Risonanza al Grado 6.",
    "1086307397": "Raccogline abbastanza e si cristallizzerà in una Stella dei Desideri.\nPoi potrai scambiarla con dei mobili. Tutto qui.",
    "1099715302": "Dr. Lewis",
    "1111050882": "Dr. Lewis",
    "1163034730": "L'ultimo colpo di un attacco base marchia il lato del bersaglio più lontano da chi lo sferra con <style=Hint_BgL>[Fango]</style>. Quando un'abilità colpisce il lato con <style=Hint_BgL>[Fango]</style>, rimuove <style=Hint_BgL>[Fango]</style>, infligge danni pari a <style=Hint_BgL><customRichText(calcData,buff,9154302,param0,1)></style> di Potenza e applica <style=Hint_BgL><customRichText(calcData,buff,9154302,param1,1)></style> accumuli di <style=Hint_BgL><link=\"source_8038\"><u>[Malus d'acqua]</u></link></style>.",
    "1181842532": "Dr. Lewis",
    "1195396486": "Dr. Lewis",
    "1199933360": "Stelle dei Desideri insufficienti per l'acquisto.",
    "1202040496": "Dr. Lewis",
    "1238136739": "Dr. Lewis",
    "1253717733": "Fascino Ombrenato",
    "1279523797": "Gli Aniimo collocati nell'<style=Hint_BgL>Area Residenziale</style> producono continuamente Stelle dei Desideri.",
    "1280598002": "Un'Abilità da Esploratore che ti permette di scalare le pareti.",
    "1302619022": "Il tuo Barattolo delle Stelle dei Desideri è pieno! Vai a raccogliere le Stelle dei Desideri!",
    "1309983569": "Velocità di produzione Stelle dei Desideri:",
    "1310319468": "Barattolo delle Stelle dei Desideri",
    "1342958797": "Produzione Stelle dei Desideri",
    "1345850271": "Anche l'energia psichica occupa spazio: quando il barattolo è pieno, smette di raccoglierne altra.\nRicordati di <style=Hint_BgD>passare regolarmente a ritirare le Stelle dei Desideri al suo interno</style>.",
    "1368110962": "Barattolo delle Stelle dei Desideri",
    "1370295603": "Un'Abilità da Esploratore che ti permette di nuotare in acqua.",
    "1378036681": "Dr. Lewis",
    "1386820989": "Spendere {0}<sprite name=\"ui_item_{1}_small\"> per sbloccare una pagina del Magazzino?",
    "1393710899": "Dr. Lewis",
    "1403623762": "La Zona di Produzione è un po' lontana dall'Area Residenziale per gli Aniimo, quindi è improbabile che ci vadano.\nMa mentre trascorrono il tempo nell'<style=Hint_BgD>Area Residenziale</style>, produrranno \"<style=Hint_BgD>Stelle dei Desideri</style>\"!",
    "1412606792": "E allora con cosa raccolgo le Stelle dei Desideri?",
    "1439005914": "Scambio Stelle dei Desideri",
    "1447507625": "Completa l'Allenamento Ombra di questa stagione a Difficile nel Simulatore Holo-Battle",
    "1464299319": "Non ci sono ancora Stelle dei Desideri da ritirare!",
    "1483438634": "Dr. Lewis",
    "1484487296": "D'accordo, d'accordo, Veep, pensiamo agli affari! Dora ci chiede di verificare se le foglie di alghe fresche che ha ordinato sono arrivate. Dobbiamo portare con noi una cassa.",
    "1501006697": "Posizionalo nell'Area Residenziale della tua Base per raccogliere automaticamente le Stelle dei Desideri prodotte dagli Aniimo presenti.",
    "1509827336": "Posizionalo nell'Area Residenziale della tua Base per raccogliere automaticamente le Stelle dei Desideri prodotte dagli Aniimo presenti.",
    "1518450849": "Stelle dei Desideri insufficienti per sbloccare.",
    "1552270364": "Dr. Lewis",
    "1587302921": "Barattolo delle Stelle dei Desideri",
    "1614063144": "Stella dei Desideri",
    "1654579391": "Completa l'Allenamento Terra di questa stagione a Difficile nel Simulatore Holo-Battle",
    "1668806970": "Dr. Lewis",
    "1682363256": "Dr. Lewis",
    "1695920311": (
        "L'Area Residenziale è ora aperta! Gli Aniimo in quest'area possono produrre <link=\"item_1011\"><color=#5090df><u>Stelle dei Desideri</u></color></link>!\n"
        "Ora puoi collocare <style=Hint_BgL>24</style> Aniimo nella tua Base.\n"
        "<style=Hint_BgL>Nuovi oggetti</style> sono disponibili nel Negozio Base e nel Negozio di Mobili, e <style=Hint_BgL>sono ora disponibili strutture di produzione più avanzate!</style>\n"
        "Il <style=Hint_BgL>limite sul numero di strutture funzionali</style> che puoi collocare nella tua Base è aumentato.\n"
        "<link=\"item_4040013\"><color=#5090df><u>Rilevatore di Risorse</u></color></link> può essere potenziato al <style=Hint_BgL>Liv. 2</style>.\n"
        "<link=\"item_4040012\"><color=#5090df><u>Modulo Cucina</u></color></link> può essere potenziato al <style=Hint_BgL>Liv. 3</style>.\n"
        "<link=\"item_4040011\"><color=#5090df><u>Modulo Ecologico</u></color></link> può essere potenziato al <style=Hint_BgL>Liv. 3</style>."
    ),
    "1703496949": "Dr. Lewis",
    "1722416359": "Dr. Lewis",
    "1762858799": (
        "Caro Esploratore,\n\n"
        "Dai tuoi primi passi sul Continente di Idyll all'esplorare in solitaria e avventurarti al fianco dei tuoi alleati, hai fatto molta strada. Non sei più un principiante: sei diventato uno splendido Esploratore! Anche se il periodo con il tuo Compagno appena schiuso è giunto al termine, la tua avventura è solo all'inizio.\n\n"
        "Abbiamo allegato a questo messaggio alcuni doni di Affinità. Dopo averli riscattati, perché non donarli agli Alleati che ti hanno aiutato lungo il cammino, rafforzando i legami che condividete? Mentre il tuo viaggio prosegue, speriamo che trasmetterai questa gentilezza ai nuovi arrivati che incontrerai!\n\n"
        "Il Continente di Idyll ha ancora molte sorprese in serbo. Continua a esplorare!"
    ),
    "1765864035": "Stelle dei Desideri?",
    "1776989851": (
        "Proprio con questo: il <style=Hint_BgD>Barattolo delle Stelle dei Desideri</style>! Raccoglie automaticamente l'energia psichica dei tuoi Aniimo.\n"
        "Di notte si illumina persino, come un sogno di mezza estate in una bottiglia."
    ),
    "1808928015": "Dr. Lewis",
    "1822764180": "Dr. Lewis",
    "1832802304": "Raccogli Stelle dei Desideri",
    "1833298325": "Fascino Ombrenato",
    "1835642618": "Un'Abilità da Esploratore che ti permette di volare.",
    "1841197835": "Dr. Lewis",
    "1850372239": "Dr. Lewis",
    "1859476209": "Dr. Lewis",
    "1884531117": "Dr. Lewis",
    "1924646037": "Dr. Lewis",
    "1936139138": "Dr. Lewis",
    "1947489063": "Dr. Lewis",
    "1952540324": "Dr. Lewis",
    "1967864276": "Dr. Lewis",
    "1979595701": "Dr. Lewis",
    "1987815834": "Dr. Lewis",
    "1993112003": "Nella mente degli Aniimo nascono sempre desideri fantastici e meravigliosi. Raccogli quei pensieri scintillanti in questo barattolo: una di queste splendenti Stelle dei Desideri potrebbe racchiudere la loro prossima brillante idea.",
    "1999534500": "Qui puoi vedere la distribuzione dei tag aspetto tra gli Aniimo della tua Base <style=Hint_BgL>che ricevono un bonus alla velocità di produzione delle Stelle dei Desideri</style>.",
    "2002290835": "Dr. Lewis",
    "2044306657": "Completa l'Allenamento Fulmine di questa stagione a Difficile nel Simulatore Holo-Battle",
    "2064177431": "Gli Aniimo collocati nell'<style=Hint_BgL>Area Residenziale</style> produrranno continuamente Stelle dei Desideri. La velocità di produzione dipende dalla velocità di produzione base di ciascun Aniimo e dai suoi <style=Hint_BgL>tag aspetto</style>. Gli effetti dei tag sono i seguenti:",
    "2104564814": "Puoi spendere {0}<sprite name=\"ui_item_{1}_small\"> per azzerare il Potenziale Acquisito aumentato. Dopo l'azzeramento, il 100% degli oggetti utilizzati verrà restituito come segue:",
    "2122989478": "Nella mente degli Aniimo nascono sempre desideri fantastici e meravigliosi. Raccogli quei pensieri scintillanti in questo barattolo: una di queste splendenti Stelle dei Desideri potrebbe racchiudere la loro prossima brillante idea.",
    "2129525430": "Nella mente degli Aniimo nascono sempre desideri fantastici e meravigliosi. Raccogli quei pensieri scintillanti in questo barattolo: una di queste splendenti Stelle dei Desideri potrebbe racchiudere la loro prossima brillante idea.",
    "2133741095": "Dr. Lewis",
}

print(f"Total defined translations in dictionary: {len(updated_translations)}")
assert len(updated_translations) == 98, f"Expected 98 translations, got {len(updated_translations)}"

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
cache_ver_content = f"1.0.3880756,{xdt_size},{xdt_md5}\n"

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

manifest["translation_version"] = "1.0.3880756.0"
manifest["known_source_key_count"] = len(sorted_keys)
manifest["known_source_key_sha256"] = keys_sha
manifest["known_source_content_sha256"] = content_sha
manifest["latest_supported_game_update"] = "3880756"
manifest["tested_game_update"] = "3880756"

if "3880756" not in manifest["supported_game_updates"]:
    manifest["supported_game_updates"].insert(0, "3880756")

game_revision = xdt_md5
if game_revision not in manifest["supported_game_revisions"]:
    manifest["supported_game_revisions"].insert(0, game_revision)

manifest["tested_game_revision"] = game_revision
manifest["tested_archive_sha256"] = archive_sha
manifest["tested_date"] = "2026-11-05"
manifest["coverage"] = f"{len(sorted_keys)}/{len(sorted_keys)} keys translated (100.00%)"

notes = [
    f"Aggiornamento per la build Steam 3880756 (patch 1.0.3880756.0) con copertura di traduzione al 100% ({len(sorted_keys):,} chiavi).".replace(",", "."),
    "Traduzione delle 27 nuove chiavi (disconnessione account Steam/Epic/WeGame/TapTap/Heybox, forzieri misteriosi, Ambra Lumin, abilità Esploratore d'élite) e 71 chiavi aggiornate.",
    "Rinominazione completa della valuta abitativa: da 'Biglietti Germoglio' a 'Stelle dei Desideri' e 'Barattolo delle Stelle dei Desideri'.",
    "Allineamento del nome del PNG Dr. Lewis nei dialoghi narrativi e correzione sintattica nei messaggi di sblocco magazzino e reset potenziale.",
    "Preservazione assoluta di tutti i tag di formattazione nativi, codici colore, placeholder di genere e formattazione rich text.",
    "Compatibilità garantita con Steam e verifica automatica della cache LuaCacheVer.txt."
]
manifest["notes"] = notes

manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Updated data/supported_versions.json successfully.")
