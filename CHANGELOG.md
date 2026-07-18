# Changelog

## 0.3.18 Beta - 2026-07-18

- Verificata la build Aniimo `3064863`: 93.029 chiavi, nessuna aggiunta o rimozione e nessuna sorgente English modificata rispetto alla build `3062823`; compatibilità riconosciuta automaticamente.
- Individuata la causa delle battute English segnalate nella sequenza di Fannie: il gioco usa un elenco runtime separato e ignorava il testo italiano per 359 chiavi storicamente recuperate, pur essendo tutte tradotte nel master.
- Corretto l'installer affinché reinserisca sempre le 359 chiavi nell'elenco `AITranslatedItems_en`, evitando il fallback inglese per l'intero gruppo e non soltanto per le cinque righe segnalate.
- Rilette e rifinite le cinque battute mostrate negli screenshot, mantenendo tag, ritorni a capo e terminologia della Base.
- Aggiunta all'eseguibile una nuova icona ad alta risoluzione con mascotte Aniimo e badge della bandiera italiana, completa delle dimensioni Windows da 16 a 256 pixel.
- Estesi audit e test di regressione per verificare numero delle chiavi recuperate, presenza delle cinque segnalazioni e contenuti italiani attesi.

## 0.3.17 Beta - 2026-07-16

- Resa automatica la verifica di compatibilità: il numero di build è ora informativo e l'installer confronta l'intero insieme di chiavi e il contenuto reale di ogni stringa.
- Le build mai viste vengono accettate senza aggiornare l'installer quando i testi corrispondono all'English ufficiale noto, alla traduzione italiana inclusa o a una combinazione sicura dei due.
- L'installazione viene bloccata se cambia la struttura delle chiavi o se compare anche un testo ufficiale sconosciuto; i dettagli tecnici indicano il tipo di controllo e il numero di stringhe da revisionare.
- Riconosciute le traduzioni già installate e quelle precedenti aggiornabili, evitando che un archivio italiano venga scambiato per un aggiornamento incompatibile del gioco.
- Verificata la build Aniimo `3058113`: 93.029 chiavi, nessuna chiave aggiunta o rimossa e nessuna sorgente English modificata rispetto alla build `3053563`; compatibilità rilevata automaticamente.
- Aggiunto il supporto verificato alla build `3062823`: il totale resta di 93.029 chiavi, con 2 chiavi aggiunte, 2 rimosse e 28 sorgenti English aggiornate.
- Tradotte e revisionate tutte le 30 righe interessate, inclusi i nuovi testi della Closed Beta Globale, del Lancio Globale, i premi evento, i check-in con fuso orario, il Sensore di movimento e l'elenco dei bloccati.
- Corretti anche tre refusi presenti nell'English ufficiale (`Global Launc` e `Global Launcha`) interpretandoli in modo coerente come `Global Launch` grazie al confronto con le stringhe duplicate e le altre lingue.
- Il flusso interno di migrazione conserva ora le note storiche degli audit e gli spazi significativi dei testi già revisionati, evitando regressioni silenziose durante i futuri aggiornamenti.

## 0.3.16 Beta - 2026-07-14

- Aggiunto il supporto verificato alla build Aniimo `3053563` usando l'installazione reale aggiornata da Pawprint.
- Integrate tutte le 45 nuove chiavi ufficiali, corrispondenti a 9 testi sorgente unici: copertura aggiornata a 93.029 / 93.029 senza chiavi rimosse o fallback inglesi.
- Tradotte le nuove descrizioni delle Uova Aniimo Prismana e scintillanti, dei materiali, delle squadre e delle missioni d'indagine del Polaris Institute.
- Aggiornate 5 sorgenti inglesi modificate dal gioco: 4 traduzioni italiane sono state riscritte per il nuovo significato e una correzione grammaticale inglese non ha richiesto modifiche all'italiano.
- Confermata la compatibilità byte per byte di tutti i formattatori data `GG/MM/AAAA` su entrambi gli archivi Lua e delle unità italiane `h/m/s` nei metadati runtime.
- Rilevato e verificato il nuovo bundle font della build `3053563`, mantenendo il reindirizzamento dello slot English al font vietnamita compatibile con tutti gli accenti italiani.
- Aggiornati fingerprint, hash dell'overlay Lua ufficiale, manifest di compatibilità e test di regressione per impedire installazioni incomplete su build future non verificate.

## 0.3.15 Beta - 2026-07-13

- Corretto definitivamente il formato delle date dinamiche visibili: capitoli missione, schermata `Astra Era`, posta, album, dettagli foto, registro attività e pannelli evento ora usano `GG/MM/AAAA`.
- Individuate e gestite separatamente le due copie di `LuaScripts.xdf/xdt`: la traduzione resta nell'overlay hot update, mentre gli script data vengono corretti e verificati in entrambe senza copiare un archivio sopra l'altro.
- Estesi backup e ripristino a tutte le copie Lua, con percorsi relativi sicuri, hash SHA-256 e compatibilità con i backup creati dagli installer precedenti.
- Il rilevamento considera la traduzione pienamente aggiornata soltanto se ogni archivio attivo contiene tutti i formati data italiani verificati.
- Sostituite le unità CJK del conto alla rovescia nelle card del negozio (`15分0秒`) con il formato compatto `15 m 0 s`, tramite una modifica dei metadati a lunghezza invariata e completamente ripristinabile.
- Aggiornato correttamente il manifest locale anche per gli alias storici `worldx_Data`, conservando l'associazione dell'archivio Lua all'overlay e aggiungendo i metadati runtime modificati.
- Ridotta l'etichetta `Gratis` nelle otto card strette del negozio, evitando la divisione grafica `Grati` / `s` senza abbreviare la parola.
- Corretta Jilly: `Sono impressionato` diventa `Sono impressionata` nel dialogo in cui parla di sé.
- Aggiunte verifiche post-generazione e post-copia degli archivi, dei relativi indici, della traduzione, delle date e del timer; completata anche una generazione reale della patch sui file della build `3048640`.

## 0.3.14 Beta - 2026-07-13

- Aggiunto il supporto verificato alla build Aniimo `3048640` usando i file reali installati da Pawprint.
- Integrate tutte le 30 nuove chiavi ufficiali: copertura aggiornata a 92.984 / 92.984, senza chiavi rimosse o mancanti.
- Aggiornate 1.977 sorgenti English modificate dal gioco e revisionate in parallelo le differenze semantiche: corrette 342 traduzioni italiane rese obsolete dal nuovo significato.
- Uniformate altre 19 etichette duplicate delle famiglie `Companion Mode` e `Rewards`, mantenendo le maiuscole funzionali.
- Riconosciuto che le 359 voci significative prima esposte come `0` sono ora presenti direttamente nell'English ufficiale; restano soltanto 5 zeri tecnici intenzionali.
- Confermata senza modifiche la compatibilità del font accentato e dei due formattatori dinamici `GG/MM/AAAA`.
- Ridisegnata la schermata iniziale dell'installer: titolo di stato, tre sole righe (`Gioco`, `Traduzione`, `Installer`) e una singola istruzione sotto `COSA FARE`.
- Spostati build storiche, digest, stato date e altri dati diagnostici nell'opzione `6. Mostra i dettagli tecnici`.
- Evitato di trattare il digest locale `87eaffe8...`, ereditato dal manifest patchato precedente, come una revisione ufficiale della nuova build.
- Aggiunti audit riproducibile, test di regressione e generazione reale della patch: 92.984 / 92.984 testi, 0 discrepanze, date e font verificati.

## 0.3.13 Beta - 2026-07-12

- Corrette le battute segnalate `Io voglio—` e `Vi serve aiuto a traslocare? / Abbiamo le ali: renderà...`, ora rese con punteggiatura e italiano naturali.
- Esteso l'audit dei trattini lunghi a ogni posizione della stringa, comprese le interruzioni prima di un ritorno a capo: 226 righe controllate e 65 ulteriori pause di dialogo convertite in `...`.
- Conservati intenzionalmente soltanto separatori grafici, intervalli, marcatori di battuta, onomatopee, scansioni sillabiche e altri usi funzionali documentati.
- Uniformati i toponimi ufficiali alla grafia inglese del gioco: 42 nomi canonici inventariati e 176 stringhe corrette fra etichette, dialoghi, missioni e descrizioni.
- Corrette in particolare le incongruenze della mappa `Stretto Argentato`, `Costa Tideblossom` e `Ponte Terrestre Zephyrus`, ora `Argent Strait`, `Tideblossom Coast` e `Zephyrus Landbridge`.
- Estesa la stessa regola a `Astra Hall of Memories` e `Hall of Memories`, mantenendo naturali articoli, preposizioni e ruoli italiani.
- Individuato un secondo formattatore dinamico usato dalle mail e da altre schermate: il formato inglese `MM/GG/AAAA` viene ora convertito in `GG/MM/AAAA` insieme alla data dei capitoli.
- Corretto lo stato dell'installer: `✓ ITALIANO` compare soltanto se entrambi i formattatori delle date sono verificati; le installazioni parziali mostrano `⚠ DA AGGIORNARE`.
- Aggiunti test di regressione e una generazione reale della patch sui 92.954 testi, con entrambi gli script data verificati byte per byte.

## 0.3.12 Beta - 2026-07-12

- Separata la semplice presenza della traduzione dalla verifica della sua versione e dei contenuti effettivamente installati.
- Il pannello mostra ora `Versione trad. installata`, `Versione trad. proposta` e un confronto completo fra tutti i testi.
- Una traduzione precedente ma ancora rilevabile viene segnalata come `DIVERSI — AGGIORNAMENTO CONSIGLIATO` invece di apparire genericamente installata.
- Se cambia soltanto l'installer e i testi coincidono già al 100%, compare `IDENTICI — nessun aggiornamento necessario`, evitando reinstallazioni inutili.
- Le vecchie installazioni prive di ricevuta vengono indicate come `Non registrata`, senza rinunciare al confronto reale dei contenuti.
- Aggiunti test specifici per versioni registrate, percorsi di gioco differenti e corrispondenza esatta della traduzione.
- Uniformate 190 battute che ereditavano un trattino lungo finale dall'inglese: in italiano terminano ora con i punti di sospensione, mentre i trattini interni semanticamente utili restano invariati.
- Eseguita una prima passata editoriale con 175 correzioni uniche ad alta confidenza, fra 106 calchi e referenti artificiali, 65 rifiniture di fluidità italiana e 4 incoerenze nei tempi verbali.
- Rilette tutte le 92.954 righe in tre blocchi indipendenti, equivalenti a 42.637 testi sorgente unici dopo il solo raggruppamento dei duplicati perfetti: 426 proposte, 423 approvate e 3 respinte durante l'adjudication finale.
- Aggiunto un controllo residuale globale con altri 443 interventi: 297 interiezioni e onomatopee localizzate, famiglie UI rese naturali, duplicati uniformati, residui inglesi rimossi e 22 stringhe orarie convertite al formato italiano senza `AM`/`PM`.
- La revisione v0.3.12 comprende complessivamente 1.041 interventi editoriali su 1.038 chiavi uniche, oltre alle 190 normalizzazioni di punteggiatura.
- Corretta la frase su Snowy in tutte le quattro varianti: un Aniimo non riceve un “passaggio” dall'Aniipod, ma viene portato al suo interno.
- Italianizzata la data dinamica della schermata capitolo: il formato passa da `AAAA/MM/GG` a `GG/MM/AAAA` mediante una modifica verificata dello script LuaJIT, inclusa nel normale backup e ripristino.
- Il pannello dell'installer mostra anche lo stato del formato data e considera la modifica nel confronto reale dei contenuti installati.

## 0.3.11 Beta - 2026-07-12

- Eseguita una nuova passata globale su tutte le 92.954 righe e applicate 714 correzioni uniche, registrate in un manifesto riproducibile e idempotente.
- Revisionati 836 ulteriori candidati di genere su 7.672 dialoghi attribuiti a 290 speaker: nessun nuovo errore nel genere proprio degli NPC, ma 110 testi rivolti al protagonista o appartenenti alla UI sono stati resi naturali e neutri.
- Uniformate 119 occorrenze di `Stamina` in `Vigore` e 93 varianti `Holo-gizmo`/`Holo-gadget` in `Congegno Holo`/`Congegni Holo`.
- Uniformati i nomi `Furia Sfrenata`, `Attrazione Gravitazionale` e `Viaggio tra le Stelle`; tradotti `Matchmaking`, `stage`, `cutscene`, `quest`, `upgrade`, `drop`, `Skin` e altri frammenti inglesi incoerenti.
- Corretti 10 testi tronchi, ripetuti o sostituiti da segnaposto tecnici e 70 descrizioni di combattimento/UI, incluse tutte le forme artificiali `secondo/i`, `volta/e`, `moneta/e` e simili.
- Rifinite 61 frasi italiane ad alta confidenza fra calchi, concordanze, articoli duplicati, sintassi tecnica e regole evento.
- Verificati singolarmente 197 possibili residui inglesi finali: 59 corretti e 138 prestiti italiani o tecnici appropriati conservati con motivazione.
- Aggiunto un audit automatico permanente per tag, segnaposto, flessioni con slash, residui inglesi, finali sospetti, lunghezze anomale e varianti incoerenti.

## 0.3.10 Beta - 2026-07-12

- Ricostruite 7.672 associazioni reali battuta→parlante da `pmdata.bin`, superando il limite del semplice controllo del CSV.
- Controllati 290 speaker e revisionati manualmente 550 candidati di concordanza con inglese, giapponese, contesto delle missioni e russo solo come fonte secondaria.
- Corrette 49 battute di personaggi femminili, incluse Sunia, Nicole, Fannie, Awen, Irelia, Lunara, Caitlin, Velouria, Baboni e Senior Loulla.
- Corretti 11 riferimenti esterni a personaggi femminili, fra cui Avetine, Cress, Haidt, Snowy e la giovane Iris.
- Corretti i due errori inversi confermati: Aeolus e Sorora sono maschili.
- Neutralizzate 96 frasi del protagonista selezionabile o rivolte al protagonista, eliminando maschili fissi come `sono pronto`, `benvenuto`, `ti sei fatto male` e `sei stato il primo`.
- Aggiunti un inventario di audit riproducibile, un manifesto di 158 correzioni per chiave e test automatici di regressione.

## 0.3.9 Beta - 2026-07-11

- Corretto l'audit delle 14 bolle `Indizio`: il precedente limite sulla lunghezza totale non rappresentava la larghezza effettiva delle singole righe.
- Imposto un controllo conservativo di massimo 2 righe e 15 caratteri visibili per riga su tutte le bolle note.
- `Un profumo floreale misterioso!`, ancora troncata in gioco, diventa `Fragranza misteriosa!`.
- `Quel Flutternym era vivacissimo!`, che con il nuovo criterio avrebbe occupato tre righe, diventa `Flutternym vivacissimo!`.
- Verificate nuovamente le altre 12 bolle, già compatibili con il nuovo criterio per riga.

## 0.3.8 Beta - 2026-07-11

- Registrata come verificata la revisione hot update `4eb81a98d0e3934af67064cbde06218e`, compatibile con tutte le 92.954 chiavi note.
- Corretto il pannello dell'installer, che la mostrava erroneamente come `⚠ NUOVA` pur avendo già superato l'audit e l'installazione reale.
- Conservata anche la precedente revisione `7113f88e39827a2d13591a55b395f1c6` nell'elenco delle revisioni supportate.
- Aggiunto un test di regressione specifico per impedire che la revisione corrente torni a essere segnalata come nuova.
- Controllati tutti i 32 testi UI brevi del sistema Indizi e accorciati i 6 che superavano la larghezza sicura.
- `Clicca sugli indizi esistenti da analizzare` diventa `Analizza gli indizi già trovati`; compattati anche due segnaposto e l'avviso di sblocco dell'indizio comune.
- Aggiunto un limite automatico di 34 caratteri visibili per l'intera categoria compatta del sistema Indizi.

## 0.3.7 Beta - 2026-07-11

- Tradotta in `Tre...` la battuta `Three...` rimasta in inglese nel conto alla rovescia del dialogo di Jaeger.
- Verificate anche le altre sequenze numeriche brevi: `One`, `Two` e i conti alla rovescia completi risultano già tradotti.
- Eseguito un nuovo audit globale dei residui inglesi: corrette 151 voci aggiuntive fra UI, didascalie, mesi, impostazioni, titoli funzionali, oggetti, cosmetici, anglicismi generici e testi misti.
- Uniformate `Hall of Memories` in `Sala dei Ricordi` e `Old Town` in `Città Vecchia`; tradotto il minigioco `Roll Out` in `Palla di fango rotolante` dopo il confronto con giapponese, cinese e coreano.
- Conservati i toponimi che il glossario dichiara ufficiali e invariabili, fra cui `Sea of Flowers`.
- Tradotte altre 24 etichette brevi rimaste identiche all'inglese, comprese `Hot Cocoa`, `Mouse Pad`, `Ice Storm`, la famiglia Gull e `Chat in {0}`.
- Distinti secondo il contesto i quattro `Build` e i tre `Record`; conservati nomi propri, abilità ufficiali, brand e prestiti standard come `Open Beta` e `open world`.
- Accorciata la notifica sul livello del Ramo collegato alla Fioritura, che superava la larghezza del riquadro e appariva troncata.
- Compattate le notifiche per Aniimo volanti, da nuoto e da arrampicata non equipaggiati, mantenendo l'indicazione della scheda Esplorazione.
- Identificate automaticamente 726 notifiche a riga singola e accorciate 78 traduzioni che superavano la larghezza sicura del riquadro.
- Aggiunto un controllo automatico: testo visibile, tag esclusi, massimo 80 caratteri per tutte le notifiche note.
- Identificati separatamente i 14 testi delle bolle `Indizio`: accorciati i 4 che venivano tagliati e imposto un limite automatico di 34 caratteri visibili.
- Rifinite le traduzioni delle scelte `The timing is weird...` e `Her character seems off...`.
- L'installer registra ora come tradotte le 359 voci recuperate che nell'English ufficiale valgono `0`, impedendo al percorso runtime speciale di sostituirle nuovamente con frasi inglesi.
- Aggiunto un controllo automatico per impedire la ricomparsa della stringa inglese.

## 0.3.6 Beta - 2026-07-11

- Corretto il genere di Lunara nelle battute e nelle didascalie confermate dal giapponese, compresi `Sono troppo emozionata` e `Lunara sembra sorpresa`.
- Eseguito un nuovo audit delle concordanze confrontando inglese, cinese, giapponese e, solo quando semanticamente allineato, russo.
- Individuato che 92.822 voci russe provengono dall'elenco ufficiale delle traduzioni AI: il russo non viene quindi più usato da solo come autorità sul genere.
- Conservati i maschili e femminili confermati dei personaggi identificati; neutralizzate le frasi in cui il parlante o il genere del protagonista non sono determinabili con sicurezza.
- Corrette 419 stringhe e identificate 3 vere coppie duplicate che il gioco seleziona per protagonista maschile o femminile; le due varianti restano distinte.
- Aggiunti controlli automatici contro le regressioni nelle battute di Lunara e nelle concordanze già revisionate.
- Unificati i due master identici in `data/translation_it.csv`, ora unica fonte autorevole con accenti italiani reali.

## 0.3.5 Beta - 2026-07-11

- Individuata la causa delle frasi inglesi ancora visibili: 364 chiavi dello slot English ufficiale contenevano il solo valore `0`, attivando testi inglesi di fallback a runtime.
- Recuperate e tradotte dalle altre localizzazioni ufficiali 359 voci significative; conservati soltanto 5 zeri realmente tecnici e identici in tutte le lingue.
- Corrette le tre risposte del dialogo sui solventi: oli, etanolo e acqua pura.
- Tradotta la sequenza narrativa dell'Istruttore che racconta gli avvenimenti e li confronta con il sogno.
- Ripulite 220 stringhe inglesi o miste con interventi mirati e uniformate altre 651 voci secondo glossario e coerenza interna.
- Tradotto sistematicamente il titolo scolastico `Principal` come `Preside`, comprese tutte le occorrenze di `Preside Oswen` in dialoghi, obiettivi e nomi dell'interlocutore.
- Rafforzati i test automatici per distinguere la copertura delle chiavi dalla reale copertura linguistica.

## 0.3.4 Beta - 2026-07-11

- Tradotta la forma `Sea of Flowers Form` come `Forma Fiorita`, evitando il testo misto inglese/italiano e il taglio nell'interfaccia Aspetto.
- Uniformate 475 occorrenze di `élite` in `Elite`/`elite`, eliminando la resa errata `E'lite` nello slot English.
- Lo slot English usa ora il font vietnamita già incluso in Aniimo, completo di tutti gli accenti italiani.
- Attivati gli accenti reali nell'intera traduzione e conservati correttamente `Timothée`, `Déjà Vu`, `Molière`, `Café` e `Português`.
- Verificata direttamente in gioco l'associazione `English → UI_Font_Vietnamese`.
- Il backup e il ripristino includono anche il pacchetto font modificato.
- Ripristinate le parentesi decorative corrotte nelle descrizioni degli effetti `Parassitico` e `Maturo`.
- Corretto il riavvio post-aggiornamento che poteva ereditare la modalità nascosta dell'assistente in background.
- Il nuovo installer viene ora avviato esplicitamente in una console Windows visibile e indipendente.
- Eliminato il caso in cui il menu restava invisibile in attesa di input mantenendo attivo il blocco della singola istanza.
- Verificata la chiusura normale della v0.3.3 senza processi residui.

## 0.3.3 Beta - 2026-07-11

- Corretto l'errore Windows `Accesso negato` quando una copia già scaricata era ancora aperta nella cache.
- Ogni aggiornamento usa ora un nome temporaneo univoco, evitando collisioni tra tentativi successivi.
- Impedita l'apertura simultanea di più finestre interattive dell'installer.
- Se il vecchio EXE rimane occupato, compare un avviso in primo piano per chiudere le altre finestre e riprovare.
- In caso di sostituzione fallita, il nuovo EXE non viene più avviato dalla cache e il vecchio installer resta intatto.
- I vecchi download dell'installer vengono rimossi automaticamente senza toccare file estranei.
- Riparata e verificata la copia `v0.3.2-beta` sul Desktop interessata dal problema.

## 0.3.2 Beta - 2026-07-11

- Aggiunta la revisione dell'hot update separata dal numero principale del gioco.
- La compatibilità viene mostrata separatamente ed è determinata dalle chiavi reali dei testi.
- Registrata e verificata la nuova revisione `7113f88e39827a2d13591a55b395f1c6`, ancora compatibile con tutte le 92.954 chiavi note.
- La revisione ufficiale viene conservata prima della patch, evitando che l'hash generato dall'installazione venga scambiato per un nuovo hot update.
- Aggiunti GitHub visibile nel pannello e menu `5` con crediti, segnalazioni e sostegno al progetto.
- Confermato che l'ultimo aggiornamento del gioco rimuove la traduzione ma non richiede modifiche ai testi italiani.
- Dopo un aggiornamento automatico, il nuovo installer mostra una conferma verde e si riavvia direttamente nel menu.

## 0.3.1 Beta - 2026-07-11

- Il pannello indica se il percorso di Aniimo è stato trovato automaticamente o recuperato da quello salvato.
- Il pannello rileva dalle risorse reali se la traduzione italiana è già installata.
- Se Aniimo non viene trovato, l'installer permette di scegliere la cartella con la finestra di Windows oppure di incollare il percorso.
- Aggiunte istruzioni immediate per riconoscere la cartella corretta contenente `Aniimo_Data`.
- Il percorso verificato viene salvato e può essere modificato in qualsiasi momento con la nuova opzione `4`.
- Estesi i controlli automatici per rilevamento traduzione, percorso salvato e pannello di stato.

## 0.3.0 Beta - 2026-07-11

- Aggiunto l'aggiornamento automatico direttamente da GitHub Releases.
- Il nuovo EXE viene accettato soltanto dopo la verifica di dimensione e hash SHA-256.
- Aggiunta la sostituzione sicura dell'installer in uso con riavvio automatico su Windows.
- Nuovo pannello iniziale con versione gioco supportata e rilevata, compatibilità colorata, versione installer attuale e nuova versione disponibile.
- Aggiunto il rilevamento reale della versione di Aniimo tramite `verlist.txt`.
- Corretta la versione gioco verificata da `3036569` a `3032670`, riscontrata nell'installazione e nel backup originali.
- Estesi i test automatici dell'installer da 5 a 12, includendo download alterati, confronto versioni e sostituzione dell'EXE.

## 0.2.1 Beta - 2026-07-11

- Seconda revisione completa dedicata alla naturalezza dell'italiano.
- Integrati 2.788 interventi aggiuntivi su dialoghi, narrativa, UI, missioni, calchi e residui inglesi.
- Uniformate tutte le descrizioni duplicate dei forzieri misteriosi e le famiglie terminologiche collegate.
- Migliorati concordanze, reggenze, neutralità di genere, ritmo dei dialoghi e messaggi UI.
- Semplificato il README con installazione in quattro passaggi e sostegno al progetto ben visibile.
- Reso più chiaro il menu dell'installer; le scelte non valide non avviano più l'installazione.
- Rigenerati e validati il master accentato e la variante compatibile con lo slot `English`.

## 0.2.0 Beta - 2026-07-11

- Revisione professionale completa di tutte le 92.954 stringhe note.
- Integrati 695 interventi editoriali e tecnici su dialoghi, terminologia, generi, UI, tag e spaziature.
- Aggiunto il master parallelo con accenti italiani reali, già pronto per un futuro font compatibile.
- Rigenerata la variante pubblica per lo slot `English`, con apostrofi e punteggiatura compatibile.
- Rafforzati backup e ripristino: vengono rimossi soltanto i file creati dalla patch.
- Aggiunti controlli sull'header delle risorse e sincronizzazione della versione MAP/BIN.
- Distribuzione semplificata in un unico file `Aniimo-Italian-Translation.exe` autonomo.

## 0.1.0 Beta

- Prima versione pubblicabile della traduzione italiana.
- Copertura completa delle 92.954 stringhe note della versione testata.
- Installer con backup automatico.
- Controllo versione/stringhe per ridurre il rischio dopo gli aggiornamenti del gioco.
- Installazione consigliata sullo slot `English`.
