"""Apply translation updates for Aniimo Steam build 3603741 (1.0.3603741.0)."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "translation_it.csv"
DIFF_PATH = Path(r"E:\TRADUZIONI\ANIIMO\diff_3603741.json")

# Detailed high-quality Italian translations curated for all 122 keys
HATCHINATOR_4_SHARDS = (
    "Può essere usato nell'<style=Hint_BgL>Hatchinator dell'Avamposto</style> e nell'<style=Hint_BgL>Hatchinator della Base</style>. "
    "L'energia Prismana residua durante la schiusa si condenserà anche in <style=Hint_BgL>4 Frammenti Guscio Prismana</style>."
)

HATCHINATOR_2_SHARDS = (
    "Può essere usato nell'<style=Hint_BgL>Hatchinator dell'Avamposto</style> e nell'<style=Hint_BgL>Hatchinator della Base</style>. "
    "L'energia Prismana residua durante la schiusa si condenserà anche in <style=Hint_BgL>2 Frammenti Guscio Prismana</style>."
)

GATHERING_LIMIT = "Hai raggiunto il limite di raccolta odierno. Lasciali crescere ancora un po'."

POLARIS_FAQ_2_QUESTIONS = (
    "1. Cos'è il Club Polaris?\n"
    "Il Club Polaris è la piattaforma di servizi per i giocatori di Aniimo. Qui puoi controllare novità del gioco, eventi e guide, "
    "consultare informazioni sugli Aniimo, partecipare a eventi con ricompense, ottenere punti (Punti Polaris) e riscattare premi.\n"
    "2. A cosa servono i Punti Polaris?\n"
    "I Punti Polaris possono essere usati per riscattare oggetti nel Negozio Punti."
)

POLARIS_FAQ_3_QUESTIONS = (
    "1. Cos'è il Club Polaris?\n"
    "Il Club Polaris è la piattaforma di servizi per i giocatori di Aniimo. Qui puoi controllare novità del gioco, eventi e guide, "
    "consultare informazioni sugli Aniimo, partecipare a eventi con ricompense, ottenere punti (Punti Polaris) e riscattare premi.\n"
    "2. A cosa servono i Punti Polaris?\n"
    "I Punti Polaris possono essere usati per riscattare oggetti nel Negozio Punti.\n"
    "3. In che modo il Club Polaris è collegato al Mini-programma Aniimo Land?\n"
    "Il Club Polaris e il Mini-programma Aniimo Land condividono gli stessi dati: l'unica differenza è la piattaforma."
)

RECORD_PLAYER_DESC = (
    "Un giradischi per la tua Base, custode di ricordi che rivivono nella musica. "
    "Usalo nella tua Area Residenziale per cambiare la musica di sottofondo della tua casa. "
    "Quando i fiori sbocciano e la luna è piena, riunisciti con qualche amico per condividere una canzone sotto la loro dolce luce."
)

TRANSLATIONS_3603741: dict[str, str] = {
    # 1. Homebuilding Zone & quests
    "289172187": "Posiziona il Barattolo dei Biglietti Germoglio nell'Area Residenziale.",
    "296237158": "Trova l'Hummin che ama i rompicapi.",
    "379215567": "Rintraccia l'Hummin buongustaio.",
    "396103414": "Completa 4 missioni richieste nel Capitolo 7.",
    "421609975": "Decora una volta la tua piattaforma personale in un Parco.",
    "454093083": "Cattura 1 Aniimo Leggendario.",
    "489739520": "Recupera l'Hummin introverso.",
    "495870995": "Trova l'Hummin irascibile.",
    "526441920": "Trova l'Hummin che adora raccogliere oggetti.",

    # 2. Gathering limits
    "1077478733": GATHERING_LIMIT,
    "1107387973": GATHERING_LIMIT,
    "1387985170": GATHERING_LIMIT,
    "1538967381": GATHERING_LIMIT,
    "1888011014": GATHERING_LIMIT,

    # 3. Season stamp & currency quotas
    "1087679361": "Hai raggiunto il limite settimanale di Timbri stagionali ottenibili dal Simulatore di Olo-battaglie.",
    "1139318123": "Hai raggiunto il limite settimanale di Timbri stagionali ottenibili dall'Interconnessione Olo-battaglie.",
    "1366314665": "Hai raggiunto il limite settimanale di Timbri stagionali ottenibili dalle Ordinazioni della Base.",
    "1575742053": "Hai raggiunto il limite settimanale di Timbri stagionali ottenibili nel Tè Sotto le Stelle.",
    "1683117805": "Hai raggiunto il limite settimanale di Timbri stagionali ottenibili in Operazione: Furto d'Uova.",
    "1793832553": "Hai raggiunto il limite settimanale di Timbri stagionali ottenibili dagli Impeti Selvaggi.",
    "1855549821": "Hai raggiunto il limite settimanale di Timbri stagionali ottenibili sconfiggendo gli Alpha.",
    "1978671355": "Hai raggiunto il limite settimanale di Timbri stagionali.",
    "1505151352": "Hai raggiunto il limite settimanale di Monete Voxel.",

    # 4. UI labels & limits
    "1104856835": "Anteprima premi",
    "1125474181": "Limite settimanale",
    "1488129001": "Limite giornaliero",
    "1941631051": "Ordina per qualità",
    "1986707430": "Premi in un punto qualsiasi per chiudere",
    "1993245032": "Costo",
    "1936396154": "Non comune",
    "1757508011": "Buono di Rinnovo",
    "1844345569": "Tabella Abilità della Famiglia",
    "1521443218": "Acquista Lettera d'Incarico",
    "2101607614": "Negozio Punti",
    "2094725741": "Riscatto Punti (Prossimamente)",
    "1617952627": "Avatar Esclusivo del Negozio Punti",
    "2028410309": "Si ottiene dal Negozio Punti.",

    # 5. Dialogues, exploration & quizzes
    "1107166181": "Catturare ripetutamente Aniimo in quest'area non farà apparire un grande gruppo tutti insieme.\nAnche l'osservazione conta durante l'esplorazione: ripensaci.",
    "1107423120": "...Non ce la faccio più. Puoi muoverti un po' con me? Devo svegliarmi...\nQuesto breve momento dopo il lavoro e prima di andare a dormire è l'unico che ho con i miei amici Aniimo. Non riesco a dormire...",
    "1111410250": "La tua figura ondeggia dolcemente tra increspature scintillanti.",
    "1116630769": "Oh, certo. È ora che me ne torni a casa... *sbadiglio*...",
    "1180516783": "Segui il luccichio delle onde e parti per un lungo viaggio.",
    "1268494819": "Con una lama affilata in pugno, perché temere il filo altrui?",
    "1272161265": "Bene, basta chiacchiere. Vieni con me all'<style=Hint_BgD>impianto di trasporto</style>. Si va a Idyll.",
    "1495711670": "Le condizioni meteo speciali fanno apparire solo Aniimo con forme speciali: non attiveranno la comparsa di un grande gruppo di Aniimo insieme.",
    "1682484400": "Questa foto serve come prova di ricerca ed è stata salvata automaticamente.",
    "1721413936": "Continua a catturare Aniimo in quest'area",
    "1745729389": "Condividi la tua buona sorte con gli amici!",
    "1772684179": "Esatto! Nutrire l'ecosistema tramite il Ramo è davvero il modo più diretto per innescare un Impeto Selvaggio.",
    "1936447446": "Gli <style=Hint_BgD>Impeti Selvaggi</style> possono far apparire grandi gruppi di Aniimo contemporaneamente. Quale delle seguenti azioni può innescarlo?",
    "2017352898": "Un'essenza concentrata estratta dalla rugiada con proprietà trasformative. Raccogline abbastanza e potrebbe valere un buon prezzo.",
    "2088390752": "Intrecciarsi con un Aniimo Amico conferisce effetti speciali.",
    "2106947923": "I bordi della gonna rimbalzano di gioia, scintillando di vibrante energia.",

    # 6. NPC Names & Places
    "1589153568": "Cloud",
    "1638575909": "Somna",
    "1763251487": "Aven",
    "1962736755": "Bosco dei Sogni di Farfalla",
    "2114420982": "Cronologia del Bosco dei Sogni di Farfalla",
    "1870845922": "Pelliccia morbida come nebbia ghiacciata, con cristalli di ghiaccio che brillano sulla punta della coda.",

    # 7. Illusory & Party mechanics
    "1142870367": "Hai raggiunto il limite di Aniimo Illusori: <style=Hint_BgL>{0}/{1}</style>. Se scegli di rendere Illusorio questo Aniimo, il tuo Aniimo <style=Hint_BgL>{2}</style> tornerà alla sua forma originale. Continuare?",
    "1185478046": "Dopo aver completato la squadra, premi #kCommon/Cancel#z per uscire dalla schermata.",
    "1194976951": "Cattura 1 Aniimo Leggendario.",
    "1203309896": "Tieni premuto per stringere un'alleanza",
    "1208053902": "La funzione Sblocca posizione è in ricarica.",
    "1217513573": "Ottieni 3 slot per Forzieri della Fortuna. Si possono ottenere fino a 5 Forzieri al giorno.",
    "1236882038": "Usa Nutri tramite il Ramo",
    "1258612437": "Premi un nome per visualizzare i dettagli dell'Illusorio",
    "1297105769": "Il teletrasporto di sblocco inizierà tra [%s].",
    "1717504663": "Il teletrasporto di sblocco inizierà tra {0}s.",
    "1301213923": "Attendi condizioni meteo speciali",
    "1359075658": "Premi #kCommon/GamepadConfirm#z per <style=Hint_BgL>impostare la squadra prima della battaglia</style>.",
    "1388427975": "Amico Illusificatore: {0}\nData di Illusificazione: {1}",
    "1928361015": "Aniimo Illusificati: {0}/{1}",
    "1180667776": "Il numero di arredi supera il limite di combinazione.",
    "1410671181": "Questo Aspetto è incompatibile con quello equipaggiato. Continuando, l'Aspetto equipaggiato verrà rimosso automaticamente. Continuare?",
    "1172906815": "Equipaggia un oggetto [Moda] - [Tiro con l'arco] prima di usare questa Emote.",
    "1863335452": "Tiro con l'arco",

    # 8. Transmog / Glimmering Driftshadow / Radiant Dreamshadow
    "1229856692": "L'<color=#b767e1>Ombra Fluttuante Scintillante</color> può essere usata solo per i primi {0} slot.",
    "1243644204": "Gli slot bloccati possono usare solo l'<color=#e49b43>Ombra di Sogno Radiosa</color>. Deselezionare e usare solo l'<color=#b767e1>Ombra Fluttuante Scintillante</color>?",
    "1881684781": "<color=#b767e1>Ombra Fluttuante Scintillante</color> insufficiente per la trasmogrificazione.",
    "1928213059": "L'<color=#b767e1>Ombra Fluttuante Scintillante</color> non può essere usata esclusivamente se ci sono slot bloccati.",
    "1938426332": "Usare l'<color=#b767e1>Ombra Fluttuante Scintillante</color> per la trasmogrificazione? Una volta attivata, non potrai bloccare gli slot e potrà essere usata solo sui primi {0} slot.",

    # 9. Combat abilities & buffs
    "1284429914": "Si accumula fino a <style=Hint_BgL>4</style> volte e dura <style=Hint_BgL><customRichText(buffConfigData,91323020,duration)></style>s. Ogni colpo di attacco base andato a segno consuma <style=Hint_BgL>1</style> accumulo di <style=Hint_BgL>[Danza della Spada]</style>, infliggendo un <style=Hint_BgL><customRichText(calcData,buff, 91323022,param0,1,%d)>%</style> di danni extra.",
    "1483754499": "Ottieni l'8% di Amplificazione Danno e l'8% di Tasso Critico, cumulabile fino a 3 volte.",
    "1506239390": "Ottieni l'8% di Amplificazione Danno e l'8% di Tasso Critico per ogni clone sul campo di battaglia, cumulabile fino a 3 volte.",
    "1568607962": "I cloni evocati infliggono il 30% di danno aggiuntivo.",
    "1775167656": "Ottieni immediatamente 5 Energia e 5 Punti Suprema per ogni clone evocato.",
    "2066000110": "Fornisce una probabilità del 20% di ripristinare 10 PE quando si attiva il recupero PV. Raddoppia la probabilità se il Potenziale RIGEN è superiore a 15.",

    # 10. Record player
    "1313990903": RECORD_PLAYER_DESC,
    "2111652548": RECORD_PLAYER_DESC,

    # 11. Club Polaris FAQs
    "1349528611": POLARIS_FAQ_2_QUESTIONS,
    "1387375580": POLARIS_FAQ_2_QUESTIONS,
    "1830443360": POLARIS_FAQ_2_QUESTIONS,
    "2033306520": POLARIS_FAQ_3_QUESTIONS,
    "1399930021": "Benvenuto nel Club Polaris, Esploratore: il tuo punto di riferimento unico per l'avventura! Con le ultime notizie, i dati sugli Aniimo e vantaggi a sorpresa, il tuo assistente per esplorare Idyll è pronto e ti aspetta!",

    # 12. Season / Irisalis pods
    "1349753641": (
        "1. Dopo aver creato l'Aniipod Leggendario: Irisalis, gli Esploratori possono spendere 49 Petali di Irisalis per creare 1 Aniipod Leggendario: Partenza col Vento.\n"
        "2. Puoi creare fino a 10 Aniipod Leggendari: Partenza col Vento.\n"
        "3. L'uso dell'Aniipod Leggendario: Partenza col Vento garantisce una cattura riuscita. Il Potenziale dell'Aniimo sarà almeno Perfetto ed è garantito che sia Scintillante. "
        "Ottiene inoltre un effetto esclusivo della stagione Partenza col Vento."
    ),
    "1377516075": (
        "1. È stata sbloccata una nuova fonte settimanale limitata per ottenere Petali di Irisalis.\n"
        "2. Gli Esploratori possono spendere 99 Petali di Irisalis per creare l'Aniipod Leggendario: Irisalis.\n"
        "3. Una volta creato e riscattato l'Aniipod Leggendario: Irisalis, si aprirà una faglia che conduce all'Aniimo Leggendario: Irisalis. "
        "Sbloccherai quindi l'idoneità alla creazione per l'oggetto della fase successiva: Aniipod Leggendario: Partenza col Vento."
    ),
    "1385647580": "Punti ottenibili durante l'evento Caccia al Sogno Radioso.",
    "1600866695": "Invia qualcun altro a perlustrare le Pianure Ventose in cerca di un Fiore di Irisalis. Garantisce il recupero di 1 Fiore di Irisalis più un numero casuale di Forzieri Leggendari. Usa un Fiore di Irisalis nel tuo inventario per ottenere 5 [Petali di Irisalis].",
    "2065138192": (
        "Esclusivo della stagione Partenza col Vento. L'uso garantisce una cattura riuscita con Potenziale <style=Hint_BgL>Perfetto</style>, "
        "oltre all'effetto <style=Hint_BgL>Scintillante</style> esclusivo della stagione. Nella versione 1.1, potrà essere usato su un Aniimo <style=Hint_BgL>Scintillante</style> "
        "per sostituire il suo Aniipod originale con l'attuale Aniipod Leggendario, conferendogli il corrispondente effetto <style=Hint_BgL>Scintillante</style> esclusivo."
    ),

    # 13. Lumin Crystal official payment discounts
    "1547120291": "Usa il servizio di pagamento ufficiale per ottenere uno sconto del <style=Hint_BgL>5%</style> sugli acquisti di <style=Hint_BgL>Cristalli Lumin</style>.",
    "1625373652": "Ti stai perdendo uno sconto del <style=Hint_BgL>5%</style> ogni volta che acquisti <style=Hint_BgL>Cristalli Lumin</style>! Richiedi subito il tuo!",
    "1757773855": "<style=Hint_BgL>5% di sconto</style> sugli acquisti di Cristalli Lumin!",
    "1763349619": "Il pagamento ufficiale è attivo: approfitta di uno sconto del <style=Hint_BgL>5%</style> quando acquisti <style=Hint_BgL>Cristalli Lumin</style>!",

    # 14. Hatchinators
    "1177131590": HATCHINATOR_4_SHARDS,
    "1197019848": HATCHINATOR_4_SHARDS,
    "1256580105": HATCHINATOR_4_SHARDS,
    "1276034318": HATCHINATOR_4_SHARDS,
    "1315886863": HATCHINATOR_4_SHARDS,
    "1408756870": HATCHINATOR_4_SHARDS,
    "1421887919": HATCHINATOR_4_SHARDS,
    "1448597320": HATCHINATOR_4_SHARDS,
    "1554921724": HATCHINATOR_2_SHARDS,
    "1614618516": HATCHINATOR_4_SHARDS,
    "1716602967": HATCHINATOR_4_SHARDS,
    "1890880978": HATCHINATOR_2_SHARDS,
    "1894757116": HATCHINATOR_4_SHARDS,
    "1898970090": HATCHINATOR_4_SHARDS,
    "1927069695": HATCHINATOR_4_SHARDS,
    "1947643806": HATCHINATOR_4_SHARDS,
    "2037627865": HATCHINATOR_4_SHARDS,
    "2103639669": HATCHINATOR_4_SHARDS,
}


def main() -> None:
    with open(DIFF_PATH, "r", encoding="utf-8") as f:
        diffs = json.load(f)

    diff_map = {d["key"]: d for d in diffs}
    print(f"Loaded {len(diff_map)} diff keys from diff_3603741.json")

    missing_in_translations = [k for k in diff_map if k not in TRANSLATIONS_3603741]
    if missing_in_translations:
        raise ValueError(f"Missing translations for {len(missing_in_translations)} keys: {missing_in_translations}")

    print(f"All {len(diff_map)} keys have translations defined!")

    # Read current translation_it.csv
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Read {len(rows)} rows from {CSV_PATH.name}")

    updated_count = 0
    for row in rows:
        k = row["key"]
        if k in diff_map:
            new_sha = diff_map[k]["sha256"]
            new_it = TRANSLATIONS_3603741[k]
            row["source_sha256"] = new_sha
            row["it"] = new_it
            updated_count += 1

    print(f"Updated {updated_count} rows in catalog")

    # Write back translation_it.csv
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["key", "source_sha256", "it"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {CSV_PATH.name} successfully!")


if __name__ == "__main__":
    main()
