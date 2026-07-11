# Changelog

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
