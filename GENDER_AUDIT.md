# Audit delle concordanze di genere

La versione 0.3.6 introduce una verifica dedicata a genere, referente e naturalezza dei dialoghi italiani. La versione 0.3.10 estende il metodo all'intero cast usando l'attribuzione reale delle battute contenuta in `pmdata.bin`.

La versione 0.3.11 ripete il controllo sull'intero master e aggiunge i testi non attribuiti a un parlante, come tutorial, notifiche, saluti e descrizioni rivolte direttamente al protagonista selezionabile.

## Ordine delle fonti

Per ogni stringa dubbia vengono confrontate le localizzazioni ufficiali disponibili, con questo criterio:

1. identità certa del personaggio e contesto della scena;
2. giapponese, quando usa pronomi o particelle che dichiarano chiaramente il genere;
3. inglese e cinese per verificare che il significato e il referente coincidano;
4. russo soltanto se la sua frase è semanticamente allineata alle altre lingue;
5. formulazione italiana neutra quando le fonti non permettono una conclusione sicura.

Il giapponese non dichiara sempre il genere: pronomi come `私` possono essere neutri. In questi casi non viene forzata una concordanza. Marcatori espliciti come `僕`, `俺`, `だわ` o il finale `わ`, se coerenti con il contesto, costituiscono invece un indizio forte.

## Perché il russo è una fonte secondaria

Negli archivi ufficiali esaminati, `AITranslatedItems_ru_RU.json` contrassegna 92.822 stringhe russe come tradotte tramite AI. La stessa stringa può inoltre risultare disallineata rispetto a inglese, cinese e giapponese.

Per confronto, l'elenco AI giapponese contiene 9.862 voci. La battuta di Lunara segnalata in gioco non ne fa parte e termina con il marcatore femminile `わ`:

```text
ふぅ……あまりの興奮で寝付けないわ……
```

La resa corretta è quindi:

```text
Uff... Sono troppo emozionata, non riesco ancora a dormire...
```

## Politica editoriale

- I personaggi identificati mantengono il genere confermato dal contesto e dalle fonti ufficiali.
- I gruppi misti seguono la normale concordanza italiana: per esempio, il protagonista maschile e Lunara insieme richiedono `svegliati entrambi`.
- Il personaggio giocante non riceve un genere arbitrario. Dove l'originale non lo specifica si preferiscono forme naturali come `Te la senti?`, `quando hai finito i preparativi` o `hai riportato ferite?`.
- Titoli, nomi propri, tag, segnaposto, maiuscole funzionali, spazi e ritorni a capo vengono conservati.
- Il russo non viene mai seguito se racconta una frase diversa o se la desinenza concorda con un oggetto invece che con il parlante.

## Verifica delle stringhe duplicate

È stato verificato se le stringhe duplicate potessero rappresentare varianti distinte per protagonista maschile e femminile.

- 59.629 chiavi appartengono a 9.312 gruppi con testo inglese identico.
- 559 gruppi duplicati si rivolgono direttamente al protagonista.
- Il confronto esteso ai marcatori `くん/ちゃん`, `学弟/学妹` e agli equivalenti coreani ha individuato esattamente 3 coppie coerenti maschile/femminile.
- Le tre coppie sono state tradotte separatamente, mantenendo il genere selezionato dal gioco.
- Gli altri gruppi sono riusi in missioni, schermate o contesti diversi, oppure cambiano il registro e il genere del parlante senza cambiare quello del protagonista.
- 893 candidati rivolti al protagonista esistono invece come chiave singola e non possono avere una seconda variante duplicata; nei casi effettivamente ambigui è stata usata una formulazione neutra.
- Il meccanismo dinamico `#playerGender#` compare in 9 stringhe ed è stato conservato senza alterazioni.

Le duplicazioni servono quindi soprattutto a riutilizzare lo stesso testo, ma includono tre eccezioni reali che il gioco seleziona in base al protagonista. Non costituiscono un sistema generale di concordanza grammaticale per l'italiano e vanno valutate singolarmente.

## Audit completo del cast nella v0.3.10

Il file runtime `pmdata.bin`, incluso in `LuaScripts.xdf`, contiene record separati per chiave del testo e chiave del parlante. L'audit riproducibile in `tools/audit_npc_gender.py` ricostruisce questo collegamento e lo confronta con il master italiano e con le localizzazioni inglese, giapponese e russa.

- 7.672 battute correnti attribuite al rispettivo parlante;
- 290 etichette di parlante controllate;
- 550 candidati grammaticali esaminati;
- 158 stringhe corrette e registrate in `data/gender_audit_v0.3.10.json`;
- 49 battute di personaggi femminili, 11 riferimenti a personaggi femminili e 2 battute di personaggi maschili corretti;
- 96 frasi del protagonista selezionabile o rivolte al protagonista riscritte in italiano naturale e neutro.

## Chiusura globale nella v0.3.11

- 532 candidati legati a speaker o prima persona ricontrollati;
- 304 candidati aggiuntivi in tutorial, stati di gioco, saluti e UI;
- 110 correzioni ad alta confidenza;
- nessun nuovo errore reale nel genere proprio del parlante NPC dopo l'audit v0.3.10;
- tutte le anomalie confermate riguardavano invece accordi fissi rivolti al protagonista selezionabile;
- secondo controllo automatico sulle proposte finali, senza neutralizzazioni parziali residue;
- zero alterazioni di tag, variabili o segnaposto.

Questo controllo ha confermato, fra gli altri, Sunia, Nicole, Fannie, Awen, Irelia, Lunara, Caitlin, Velouria, Baboni e Senior Loulla come personaggi femminili. Ha inoltre corretto due errori inversi: Aeolus e Sorora sono maschili. Le specie o le etichette riutilizzate senza prove sufficienti non ricevono un genere biologico arbitrario; in quei casi la frase viene resa neutra.

Le traduzioni russe mostrano numerose concordanze maschili errate anche per personaggi inequivocabilmente femminili. Restano quindi una fonte secondaria: prevalgono i pronomi inglesi espliciti, il contesto della missione e i marcatori giapponesi della stessa chiave.
