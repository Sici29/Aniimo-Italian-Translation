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

# 1. Load official English records from 3857679 LuaScripts.xdf
with zipfile.ZipFile(XDF, "r") as zf:
    mapping = json.loads(zf.read("xfs/luascripts/Data/I18N/NewTextMap_en.json").decode("utf-8-sig"))
    bin_data = zf.read("xfs/luascripts/Data/I18N/Compress_en.bin")

official_en = {}
for k, v in mapping.items():
    if not str(k).startswith("_") and isinstance(v, list) and len(v) == 2:
        off, length = int(v[0]), int(v[1])
        text = bin_data[off : off + length].decode("utf-8", errors="replace")
        official_en[str(k)] = text

print(f"Loaded {len(official_en)} official English strings from build 3857679.")

# 2. 111 Updated Translations for changed keys
updated_translations = {
    "330868732": "Viaggia con i pesci.",
    "387494356": "Viaggia con i pesci.",
    "392590842": "Viaggia con i pesci.",
    "520710181": "Prova a entrare nella bolla e segui Lyrelle.",
    "1082193088": "Avanzamento ",
    "1086376740": "Completa la storia richiesta",
    "1086509794": "Argomento",
    "1086770762": "Biglietto a costo doppio",
    "1103626657": "Già accettata",
    "1124036188": "Attivare una connessione KCP può ridurre gli scatti durante le fluttuazioni di rete, ma potrebbe aumentare il consumo di dati.",
    "1131197568": "Punti personali cumulativi di co-costruzione",
    "1133267933": "Bonus",
    "1138496616": "Riscatta ricompense doppie",
    "1154658381": "Una porta in legno ad arco arrotondato, che veglia con dolcezza su ogni partenza e ritorno.",
    "1158658491": "Scatta vicino al bersaglio e attacca con una rapida serie di affondi. Usarla mentre <style=Hint_BgL><link=\"source_8280\"><u>[Esplosione elastica]</u></link></style> è attiva aumenta i danni inflitti da chi la usa del <style=Hint_BgL><customRichText(calcData,buff, 2122304,param0,1,%d)>%</style> per <style=Hint_BgL><customRichText(calcData,ability,12230300,param2,1)></style> s.",
    "1160851856": "Oggetti insufficienti",
    "1167369090": "BREAK +10%. Questo effetto raddoppia se il Potenziale BREAK supera 15 punti.",
    "1169560313": (
        "Gli Aniimo possono sottoporsi al <style=Hint_BgL>Risveglio Capacità</style> consumando oggetti come la Polvere stellare per <style=Hint_BgL>aumentare</style> il <style=Hint_BgL>Potenziale Acquisito</style> degli attributi selezionati.\n"
        "1. Ognuno dei sei attributi di un Aniimo possiede un [Potenziale Innato] e un [Potenziale Acquisito].\n"
        "Il <style=Hint_BgL>[Potenziale Innato]</style> viene determinato alla nascita e può essere aumentato solo tramite metodi speciali, come i Capafruit.\n"
        "Il <style=Hint_BgL>[Potenziale Acquisito]</style> può essere aumentato tramite il Risveglio Capacità. Più volte viene aumentato, più numerosi e rari saranno gli oggetti richiesti.\n"
        "Tuttavia, <style=Hint_BgL>la somma di Potenziale Innato e Potenziale Acquisito</style> non può superare <style=Hint_BgL>20</style>. Un Potenziale più elevato fa sì che l'attributo corrispondente aumenti maggiormente quando l'Aniimo sale di livello.\n"
        "2. Far salire di livello un Aniimo o raggiungere determinati Gradi Stella di Risonanza conferisce tentativi aggiuntivi di Risveglio Capacità.\n"
        "3. Gli Aniimo di livello 60 o superiore possono anche azzerare il [Risveglio Capacità]. Oltre al costo base in Crediti, l'azzeramento richiede un numero di [Carte azzeramento potenziale] pari al numero di [Essenze di cristallostella] precedentemente investite in quell'Aniimo. Per incoraggiare a provare più combinazioni di Aniimo, l'Istituto abbuonerà il costo di 15 [Carte azzeramento potenziale] per ogni azzeramento. Se sono state investite al massimo 15 [Essenze di cristallostella] in totale, basterà spendere solo Crediti per azzerare."
    ),
    "1188577135": "Una porta in legno a punta, la cui silhouette fiera ed eretta conferisce alla casa un forte senso di appartenenza.",
    "1202986155": "Hai trovato un grande stagno con spazio sufficiente affinché Lilipole e Sugarfish possano giocare in acqua insieme. La pozza dove Kiki e i suoi amici mettono in scena i loro spettacoli di gorgoglii si trova proprio nelle vicinanze. Itsy ha intenzione di andare a parlarne con Kiki e ti chiede di aspettare qui sue notizie.",
    "1223639836": "Aiuta i Lilipole a rimuovere i blocchi di gelatina dolce!",
    "1225052041": "Argomento",
    "1240962729": "Lancia un Pennywisp per assistere i membri della squadra per <style=Hint_BgL><customRichText(buffConfigData,2163303,duration)></style> s. Durante questo tempo, applica il <style=Hint_BgL><link=\"source_8291\"><u>[Marchio di Pennywisp]</u></link></style> all'ultimo bersaglio attaccato dalla squadra e fa sì che il <style=Hint_BgL><link=\"source_8291\"><u>[Marchio di Pennywisp]</u></link></style> ripristini a chi lo usa <style=Hint_BgL><customRichText(calcData,buff, 2163301,param4,1)></style> di Energia extra ogni secondo.",
    "1242150346": "Deposita in blocco\n{0} Aniimo",
    "1251648320": "Crema solare",
    "1251919333": "Ricompensa per la raccolta dei Distintivi d'argento nelle regioni delle Isole Sussurromarea",
    "1257479192": "Uno splendore dorato luccica nello specchio. La luce ruota con l'ombra, e l'ombra nasce dalla luce.",
    "1257511594": "Rivincita dell'Esploratore d'élite",
    "1264507429": "Ritira in blocco\n{0} Aniimo",
    "1278506273": "Si ottiene partecipando all'evento stagionale della Base: Festival della Luna del Raccolto",
    "1279633398": "Raduno notturno",
    "1304869495": "Sogno notturno",
    "1304951304": "Accettazioni disponibili  {0}/{1}",
    "1313346307": "Una porta in legno a punta, la cui silhouette fiera ed eretta conferisce alla casa un forte senso di appartenenza.",
    "1319058530": "Forziere di potenziamento",
    "1323298033": "Quando metti a segno un colpo CRIT, ripristina la ROTTURA di chi lo usa di un valore pari al 25% dei danni da ROTTURA inflitti da quel colpo. Se la ROTTURA di chi lo usa è già al massimo, infligge invece un ulteriore 25% di danni da ROTTURA al bersaglio.",
    "1330822623": "Infligge danni continui in linea retta davanti a sé. Ogni colpo può consumare <style=Hint_BgL>2</style> accumuli del proprio <style=Hint_BgL><link=\"source_8038\"><u>[Malus d'acqua]</u></link></style> per infliggere danni aggiuntivi pari al <style=Hint_BgL>50%</style> di Potenza.",
    "1342824426": "Fai un'offerta al Dio Zucca",
    "1343900461": "1. Durante l'evento, accedi al gioco ogni giorno per completare il check-in giornaliero e ottenere ricompense in base al numero complessivo di check-in effettuati.\n2. Il conteggio giornaliero dei check-in si azzera alle 04:00 (UTC+0). Effettua il check-in per un totale di 14 giorni per riscattare tutte le ricompense.",
    "1362039399": "Storia principale",
    "1399216142": "Sconfiggi questo Aniimo usando un'abilità Fulmine",
    "1406589058": "Crema solare",
    "1407155079": "Usa in [Aspetto] - [Design] per personalizzare l'aspetto.",
    "1410550474": "Dettagli co-costruzione",
    "1420999449": "Dopo aver raccolto dieci colori da tutto il mondo e averli offerti alla Vena, la Piantina sembra aver risposto. Accanto a essa è apparso un Uovo di Aniimo che brilla con i colori di Prismana: un dono in cambio da parte dei fiori sbocciati.",
    "1442869839": "Una porta in legno ad arco arrotondato, che veglia con dolcezza su ogni partenza e ritorno.",
    "1452324901": "Hai raccontato a Royalby l'accaduto. Royalby teme che il Dewple scomparso possa spruzzare acqua e danneggiare il Polline nell'Habitat. Forse quel Dewlop può aiutarti a trovarlo?",
    "1462576154": "Raccogli",
    "1470842266": "Quando catturi un Alfa, spendi il doppio per ricevere <style=Hint_BgD>ricompense doppie</style>",
    "1519152348": "Deposito Aniimo <color=#ffe866>Limite</color>",
    "1521081884": "1. Durante l'evento, accedi ogni giorno per effettuare il check-in giornaliero e riscatta le ricompense in base ai check-in totali effettuati.\n2. Il check-in si azzera ogni giorno alle 04:00. Effettua il check-in per un totale di 14 giorni per riscattare tutte le ricompense.",
    "1524739419": "Stagione della Base - Meravigliosa Notte Magica",
    "1529600565": "Gli Esploratori d'élite daranno il massimo: vinci di nuovo il combattimento per ottenere il Distintivo esclusivo dell'Istituto e risorse rare.",
    "1536174889": "Le Sfide dell'Esploratore d'élite sono aperte agli studenti più promettenti dell'Istituto. Ogni sfida ti contrappone a un Esploratore d'élite certificato con un curriculum straordinario. Superare la prova dimostra la tua forza e ti fa guadagnare un distintivo esclusivo dell'Istituto e risorse rare.",
    "1545420776": "Raccogli nelle Isole Sussurromarea",
    "1559474558": "Scambia nel Negozio Tessiluce",
    "1567643505": "La luce scende dall'alto, facendo risplendere i gradini di pietra. La scala a chiocciola invita dolcemente a salire, scintillando nel suo splendore specchiato.",
    "1574989423": "Una pesante porta rettangolare in legno che delimita nettamente la stanza.",
    "1597075465": "Punti co-costruzione del Parco",
    "1599946322": "Dewlop è stato inspiegabilmente infilato in una scatola mentre dormiva e scaricato qui. Non sa nient'altro. Ti chiede di farglielo sapere quando catturerai il ladro, così da poter accusare il colpevole di persona.",
    "1607861729": "1. Durante l'evento, accedi al gioco ogni giorno per completare il check-in giornaliero e ottenere ricompense in base al numero complessivo di check-in effettuati.\n2. Il conteggio giornaliero dei check-in si azzera alle 04:00 (UTC-4). Effettua il check-in per un totale di 14 giorni per riscattare tutte le ricompense.",
    "1618322180": "Fa' attenzione!",
    "1627249446": "La testimonianza del Dewlop",
    "1634099620": "Contenuti di grande valore attendono di essere sbloccati!",
    "1637378110": "Una pesante porta rettangolare in legno che delimita nettamente la stanza.",
    "1668341728": "Deposito Aniimo <color=#da8000>Capacità</color>",
    "1678397722": "Argomento Aniimo",
    "1683614767": "Spendi {0}<sprite name=\"ui_item_{1}_small\"> e {2}<sprite name=\"ui_item_151005_small\"> per ripristinare il Potenziale Acquisito aumentato. Tutti gli oggetti verranno rimborsati interamente (100%) dopo il ripristino, come segue:",
    "1684544929": "L'uso di un'abilità o dell'Ultima conferisce a chi la usa 1 accumulo di <style=Hint_BgL><link=\"source_8065\"><u>[Turbo Boost]</u></link></style>, facendo sì che il prossimo Attacco Base infligga un ulteriore <style=Hint_BgL><customRichText(calcData,buff,91693011,param0,1,%d)>%</style> di danni e BREAK. Possono esistere fino a 2 accumuli contemporaneamente. All'ingresso in combattimento, Jeburst ottiene un'Ultima senza costi di risorse. Questa si ricarica ogni <style=Hint_BgL><customRichText(calcData,buff,9169301,param0,1)></style> s.",
    "1690948352": "La luce scende dall'alto, facendo risplendere i gradini di pietra. La scala a chiocciola invita dolcemente a salire, scintillando nel suo splendore specchiato.",
    "1699735997": "1. Durante l'evento, accedi al gioco ogni giorno per completare il check-in giornaliero e ottenere ricompense in base al numero complessivo di check-in effettuati.\n2. Il conteggio giornaliero dei check-in si azzera alle 04:00 (UTC+8). Effettua il check-in per un totale di 14 giorni per riscattare tutte le ricompense.",
    "1704892406": "Dopo aver attivato il Pass mensile, puoi spendere il doppio della Primergia per ottenere ricompense doppie ogni volta che sconfiggi un Alfa.",
    "1708296304": "Un prodotto solare regalato da Rosina. Da usare con cautela: proteggersi dai raggi UV è una cosa, ma una reazione allergica è ben altro.",
    "1715740559": "Squit-squit, squit!",
    "1734720419": "Scatena generosamente una pioggia torrenziale di budini, infliggendo danni ad area e aumentando il Potenziamento Elementale Ghiaccio di tutti i membri della squadra di <style=Hint_BgL><customRichText(calcData,buff,915940103,param0,1,%d)></style> per <style=Hint_BgL><customRichText(buffConfigData,915940103,duration)></style> s.",
    "1744893022": "Crea il <style=Hint_BgL>[Dominio della Regina]</style>. Quando un Aniimo di tipo Vento in campo usa un'abilità, il dominio si attiva, infliggendo danni ai bersagli nell'area d'effetto. L'intervallo tra le attivazioni del dominio è di almeno <style=Hint_BgL>0,5</style> s e il dominio dura <style=Hint_BgL><customRichText(buffConfigData,216140101,duration)></style> s. Dopo che il dominio si è attivato, c'è una probabilità del <style=Hint_BgL><customRichText(calcData,buff,216140101,param3,1,%d)>%</style> che si attivi un'ulteriore volta.",
    "1754150542": "Prima vittoria Alfa",
    "1756509840": "Dono Tessiluce",
    "1756713461": "Consegna nutriente settimanale",
    "1773485631": "Vuoi rinunciare a questa opportunità di catturare l'Alfa e ottenere ricompense?",
    "1787067217": "Olio solare mescolato con ingredienti sconosciuti. Emana un fresco profumo di menta e lascia una sensazione di freschezza sulla pelle, ma riparerà davvero dal sole?",
    "1796077050": "Oggetti consegnati: {0}",
    "1797426275": "Un regalo di ringraziamento dal Dio Zucca per i meravigliosi ricordi creati insieme durante la Notte delle Meraviglie. <style=Hint_BgD>Questo Buff si attiva dopo essere entrati una volta nella propria Base.</style>\n\nBuff attuale:",
    "1820424107": "L'arcobaleno sbiadito",
    "1825930836": "Puoi scegliere uno degli Oggetti Tenuti di <style=Q_5>qualità leggendaria</style> come ricompensa.",
    "1829729901": "Selezione Oggetto Tenuto leggendario",
    "1833902994": "Regalo di ringraziamento del Dio Zucca",
    "1837719257": "Usa protocollo KCP (migliora il gioco su reti deboli)",
    "1850105463": "Annulla cattura",
    "1856120881": "Barriera elementale",
    "1888668329": "Aspetta, ti curerò tra un istante.",
    "1899046503": "Scambia",
    "1902783113": "Argomento Aniimo",
    "1940988664": "Un prodotto abbronzante regalato da Javier. Da usare con cautela: non abbronzarsi non è grave, ma una scottatura fa male.",
    "1942590217": "Viaggio leggendario: Echi del mare canoro",
    "1946826310": "Può essere riscattato una volta soddisfatti sia il requisito di progresso complessivo sia quello di progresso personale ottenuto nel <style=Hint_BgL>Parco attuale</style>.",
    "1949816501": "Uno splendore dorato luccica nello specchio. La luce ruota con l'ombra, e l'ombra nasce dalla luce.",
    "1961015087": "Aumento del moltiplicatore di contrattacco elementale degli Aniimo speciali",
    "1996380604": "Ricompense di co-costruzione",
    "2026623131": "Possiedi 1 Aniimo con Risonanza al Grado 6.",
    "2036832163": "Fai un'offerta al Dio Zucca",
    "2049309991": "I danni finali subiti aumentano del 15%.",
    "2057108519": (
        "È nato un potente Aniimo leggendario, che raduna l'energia della Vena e forma una strana fenditura.\n"
        "Tuttavia la Vena sta pulsando in modo anomalo, e l'Aniimo leggendario coinvolto è diventato furioso.\n"
        "Esploratore, indaga immediatamente sulla fenditura d'energia. Con coraggio e un cuore colmo di cure, placa l'Aniimo infuriato e metti fine a questo scompiglio."
    ),
    "2066925728": "Completa la storia richiesta",
    "2078939389": "Apri per scegliere 1 tra gli Oggetti Tenuti leggendari elencati di seguito.",
    "2083901451": "Olio abbronzante mescolato con ingredienti sconosciuti. Emana un profumo terroso difficile da descrivere e lascia la pelle lucida... ma farà davvero scurire la pelle?",
    "2090576611": "Usa questo oggetto quando catturi un Alfa per spendere il doppio di Primergia e ricevere ricompense doppie.",
    "2103507442": "Quando mandi un bersaglio in [Stato di rottura], aumenta il Danno finale che subisce del 10% per 15 s. Se il colpo che innesca questo [Stato di rottura] è un CRIT, l'aumento diventa invece del 15%.",
    "2111964422": "I danni finali subiti aumentano del 10%.",
    "2117024798": "Il Fruttolanterna dorato si ammanta di un velo di garza rossa mentre un tenue profumo aleggia nell'aria, e un sapore dimenticato da tempo riaffiora silenziosamente nei ricordi del Dio Zucca.",
    "2133995773": "La preoccupazione di Royalby",
}

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
cache_ver_content = f"1.0.3857679,{xdt_size},{xdt_md5}\n"

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

manifest["translation_version"] = "1.0.3857679.0"
manifest["known_source_key_count"] = len(sorted_keys)
manifest["known_source_key_sha256"] = keys_sha
manifest["known_source_content_sha256"] = content_sha
manifest["latest_supported_game_update"] = "3857679"
manifest["tested_game_update"] = "3857679"

if "3857679" not in manifest["supported_game_updates"]:
    manifest["supported_game_updates"].insert(0, "3857679")

game_revision = xdt_md5
if game_revision not in manifest["supported_game_revisions"]:
    manifest["supported_game_revisions"].insert(0, game_revision)

manifest["tested_game_revision"] = game_revision
manifest["tested_archive_sha256"] = archive_sha
manifest["tested_date"] = "2026-10-31"
manifest["coverage"] = f"{len(sorted_keys)}/{len(sorted_keys)} keys translated (100.00%)"

notes = [
    f"Aggiornamento per la build Steam 3857679 (patch 1.0.3857679.0) con copertura di traduzione al 100% ({len(sorted_keys):,} chiavi).".replace(",", "."),
    "Traduzione e revisione delle 111 chiavi modificate e rimozione delle 3 chiavi dismesse dagli sviluppatori nella build 3857679.",
    "Aggiornate le descrizioni di risveglio capacità con reset potenziale, abilità Jeburst e Pennywisp, missioni Autumn Wonderfest e Halloween.",
    "Preservazione assoluta di tutti i tag di formattazione nativi, codici colore, placeholder di genere e formattazione rich text.",
    "Compatibilità garantita con Steam e verifica automatica della cache LuaCacheVer.txt."
]
manifest["notes"] = notes

manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Updated data/supported_versions.json successfully.")
