# Aniimo — Traduzione italiana

Traduzione italiana amatoriale completa per **Aniimo**, con installazione automatica, backup e ripristino.

## ☕ Sostieni il progetto

La traduzione viene revisionata e aggiornata gratuitamente. Se ti è utile e vuoi aiutarmi a mantenerla compatibile con le future versioni di Aniimo, puoi offrirmi un caffè.

[![Offrimi un caffè e sostieni la traduzione italiana](https://img.shields.io/badge/Offrimi_un_caff%C3%A8-Sostieni_la_traduzione-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=000000)](https://buymeacoffee.com/sici29)

**Grazie di cuore a chi sceglie di sostenere il progetto e le future traduzioni italiane.**

## Scarica e installa

### 1. Scarica un solo file

[**Scarica l'ultima versione da GitHub Releases**](https://github.com/Sici29/Aniimo-Italian-Translation/releases/latest)

Il file da scaricare è:

```text
Aniimo-Italian-Translation.exe
```

### 2. Chiudi il gioco

Chiudi **Aniimo** e il suo launcher prima di continuare.

### 3. Apri l'installer

Fai doppio clic su `Aniimo-Italian-Translation.exe`, poi premi **Invio**.

All'apertura compare un riepilogo immediato, senza un elenco di codici tecnici:

- un titolo grande indica se è tutto aggiornato, se puoi installare o se Aniimo è stato aggiornato;
- tre sole righe mostrano **Gioco**, **Traduzione** e **Installer**;
- sotto **COSA FARE** trovi una sola istruzione chiara, per esempio `Premi Invio per installarla`.

Hash, build supportate, digest, verifica delle date e unità del timer restano disponibili soltanto scegliendo `6. Mostra i dettagli tecnici`.

L'installer cerca automaticamente il gioco, controlla la compatibilità e crea un backup prima di modificare qualsiasi file.

### 4. Seleziona Inglese nel gioco

Avvia Aniimo e scegli **Inglese** dal menu della lingua.

La traduzione continua a usare lo slot English, sempre disponibile nel gioco. L'installer gli assegna automaticamente il font vietnamita già incluso in Aniimo, che comprende tutte le lettere accentate italiane. Le altre lingue non vengono modificate.

> Non servono Python, programmi aggiuntivi, archivi da estrarre o configurazioni manuali.

## Se l'installer non trova Aniimo

Se il percorso non viene trovato, l'installer propone subito di selezionarlo con una normale finestra di Windows. Scegli la cartella che contiene `Aniimo_Data`:

```text
Aniimo\game\
├── Aniimo_Data\
└── Aniimo-Italian-Translation.exe
```

Per recuperare il percorso:

1. apri la cartella in cui **Pawprint** ha installato Aniimo;
2. entra nella sottocartella `game`, se presente;
3. verifica che al suo interno sia presente `Aniimo_Data`;
4. seleziona quella cartella nella finestra dell'installer.

Esempio:

```text
F:\Pawprint\Aniimo\game
```

È anche possibile incollare direttamente il percorso. Dopo la verifica verrà salvato e riutilizzato automaticamente. Per cambiarlo successivamente, apri l'installer e scegli l'opzione `4`.

## Ripristina i file originali

1. Chiudi Aniimo e il launcher.
2. Apri nuovamente `Aniimo-Italian-Translation.exe`.
3. Digita `2` e premi **Invio**.

Verrà ripristinato automaticamente l'ultimo backup. I backup sono conservati in:

```text
Documenti\AniimoItalianTranslation\backups
```

## Stato della traduzione

- Copertura: **93.029 / 93.029 chiavi**.
- Versioni del gioco verificate: **3032670**, **3036569**, **3048640** e **3053563**.
- Revisioni hot update verificate: **7113f88e39827a2d13591a55b395f1c6** e **4eb81a98d0e3934af67064cbde06218e**.
- Versione della traduzione: **0.3.16 beta**.
- Lingua da selezionare nel gioco: **Inglese**.
- Revisione: terminologia, dialoghi, generi, UI, tag, spaziature e naturalezza dell'italiano.
- Audit v0.3.5: **359 fallback recuperati**, **220 residui inglesi corretti** e **651 uniformazioni di glossario e coerenza**, incluso `Principal` → `Preside`.
- Audit v0.3.6: **419 stringhe corrette**, verifica delle concordanze con priorità al giapponese, controllo semantico del russo e 3 vere coppie protagonista maschile/femminile conservate separatamente.
- Correzione v0.3.7: tradotto `Three...` in `Tre...` nel conto alla rovescia di Jaeger e accorciata una notifica della Fioritura che superava il riquadro.
- Audit notifiche v0.3.7: **726 avvisi a riga singola controllati**, **78 testi accorciati** e limite automatico di 80 caratteri visibili.
- Audit indizi v0.3.7: **14 bolle controllate**, **4 testi accorciati** e limite automatico di 34 caratteri visibili.
- Audit inglese v0.3.7: **151 residui aggiuntivi corretti**, inclusi `Three`, didascalie, mesi, impostazioni, titoli funzionali, oggetti, cosmetici, anglicismi generici e denominazioni incoerenti.
- Correzione v0.3.8: registrata la revisione `4eb81a98d0e3934af67064cbde06218e` come verificata, eliminando l'avviso errato `⚠ NUOVA` dall'installer.
- Sistema Indizi v0.3.8: **32 testi UI brevi controllati**, **6 accorciati** e limite automatico di 34 caratteri; la frase segnalata è ora `Analizza gli indizi già trovati`.
- Bolle Indizio v0.3.9: controllo rifatto sulla larghezza di ogni riga; tutte le 14 bolle rispettano ora un massimo di 2 righe da 15 caratteri. Riviste `Fragranza misteriosa!` e `Flutternym vivacissimo!`.
- Audit completo dei generi v0.3.10: ricostruite dai dati runtime 7.672 associazioni fra battuta e parlante, controllati 290 speaker e revisionati 550 candidati. Corrette 158 stringhe fra concordanze del cast, riferimenti a personaggi e formulazioni neutre per il protagonista selezionabile.
- Audit qualità v0.3.11: nuova passata su tutte le **92.954 righe**, con **714 correzioni uniche** a genere, naturalezza, testi tronchi, terminologia e UI. Revisionati altri 836 candidati di genere; neutralizzati 110 testi rivolti al protagonista, uniformati `Vigore`, `Congegno Holo`, nomi abilità e terminologia di sistema.
- Controllo finale v0.3.11: eliminate tutte le flessioni artificiali come `secondo/i`, corretti 10 contenuti tronchi o segnaposto, verificati 197 possibili residui inglesi e conservati soltanto 138 prestiti italiani o tecnici appropriati, documentati singolarmente.
- Audit editoriale v0.3.12: prima passata con **175 correzioni uniche ad alta confidenza** fra calchi, fluidità e tempi verbali.
- Revisione profonda v0.3.12: rilette tutte le **92.954 righe**, raggruppando soltanto i duplicati perfettamente identici in **42.637 testi sorgente unici**; 426 proposte riesaminate e **423 correzioni** approvate dopo l'ultima verifica editoriale.
- Controllo residuale v0.3.12: altri **443 interventi** su interiezioni, onomatopee, residui inglesi, duplicati divergenti, famiglie UI, date e spaziature. In totale la v0.3.12 applica **1.041 interventi editoriali su 1.038 chiavi uniche**, oltre alle 190 normalizzazioni di punteggiatura.
- Localizzazione residuale v0.3.12: corrette **297 interiezioni e onomatopee inglesi**; conservati soltanto nomi ufficiali come `Master Woof` e `Little Lightning Chirp` e vocalizzi realmente ambigui. Rimossi inoltre `AM`/`PM` da tutte le 22 stringhe che usano già l'orario italiano a 24 ore.
- Rifinitura v0.3.12: l'installer confronta versione e contenuti installati; 190 trattini lunghi finali ereditati dall'inglese sono stati uniformati ai punti di sospensione italiani.
- Data dinamica v0.3.12: la schermata capitolo usa ora il formato italiano `GG/MM/AAAA`; la modifica è verificata byte per byte e viene inclusa nel backup e nel ripristino automatici.
- Punteggiatura v0.3.13: controllate tutte le 226 righe contenenti `—` o `–`, in qualunque posizione. Altre 65 pause e interruzioni di dialogo sono state convertite in `...`; separatori grafici, intervalli, onomatopee e usi intenzionali restano invariati.
- Toponimi v0.3.13: inventariati 42 nomi ufficiali e uniformate 176 righe. Aree e luoghi con nome proprio restano coerentemente in inglese, mentre articoli, preposizioni e testo circostante restano in italiano.
- Date dinamiche v0.3.13: oltre alla schermata capitolo, anche il formattatore condiviso usato da mail e altre schermate passa da `MM/GG/AAAA` a `GG/MM/AAAA`. L'installer considera la data aggiornata soltanto quando entrambi i formattatori sono verificati.
- Compatibilità v0.3.14: verificata la build **3048640** sull'installazione reale. Integrate 30 nuove chiavi, aggiornate 1.977 sorgenti inglesi e corrette 342 traduzioni rese obsolete dai cambi ufficiali, più 19 uniformazioni di famiglia.
- Installer v0.3.14: il riepilogo iniziale è stato ridotto a tre righe e una sola azione consigliata. I dati tecnici sono disponibili separatamente con l'opzione `6`.
- English ufficiale v0.3.14: le 359 stringhe significative che prima valevano `0` sono ora presenti direttamente nel gioco; restano soltanto 5 zeri tecnici intenzionali.
- Date dinamiche v0.3.15: controllate tutte le superfici UI realmente visibili. Capitoli missione, `Astra Era`, posta, album, dettagli foto, registri attività ed eventi usano ora `GG/MM/AAAA`.
- Installer v0.3.15: rileva, salva e corregge indipendentemente sia l'overlay Lua dell'hot update sia l'archivio base/fallback, verificandoli dopo la copia e mantenendo compatibili i vecchi backup.
- Timer v0.3.15: il conto alla rovescia delle card del negozio non mostra più unità cinesi come `15分0秒`, ma il formato compatto `15 m 0 s`.
- Correzioni v0.3.15: `Gratis` resta su una sola riga nelle card strette e Jilly dice correttamente `Sono impressionata`.
- Compatibilità v0.3.16: verificata la build **3053563** sull'installazione reale. Integrate tutte le 45 nuove chiavi, equivalenti a 9 testi unici, e aggiornate le 5 sorgenti inglesi modificate dal gioco.
- Revisione v0.3.16: tradotte le nuove descrizioni di Uova Aniimo, Aniimo Prismana, materiali, squadre e missioni d'indagine; corrette le quattro traduzioni il cui significato ufficiale è cambiato.
- Font v0.3.16: riconosciuto il nuovo bundle della build `3053563` e verificato nuovamente il reindirizzamento dello slot English al font con accenti italiani completi.

La verifica non si limita a controllare che ogni chiave abbia un valore: confronta numero e fingerprint delle chiavi con la build realmente verificata. Nelle versioni precedenti l'installer recuperava anche 359 voci significative che lo slot English esponeva come `0`; dalla build 3048640 quei testi sono finalmente presenti nell'English ufficiale.

I conteggi e il confronto con tutte le lingue ufficiali sono documentati nell'[audit completo delle lingue](LANGUAGE_AUDIT.md). Il metodo usato per le concordanze è descritto nell'[audit dei generi](GENDER_AUDIT.md). La passata editoriale più recente è riepilogata nell'[audit qualità v0.3.11](QUALITY_AUDIT.md).

## Accenti italiani completi

La versione consigliata usa accenti italiani reali:

```text
qualità   perché   può   già   più
```

Il gioco contiene già un font vietnamita completo, ma normalmente lo slot English usa un font base privo di accenti. L'installer modifica soltanto questa associazione: i testi restano nello slot English, mentre la visualizzazione usa il font vietnamita incluso in Aniimo. Non vengono installati font esterni e rimangono corretti anche nomi e termini ufficiali come `Timothée`, `Déjà Vu`, `Molière`, `Café` e `Português`.

## Aggiornamenti

L'installer controlla automaticamente GitHub Releases a ogni avvio. Quando trova una versione più recente:

1. chiede conferma con **Sì** già selezionato;
2. scarica il nuovo `Aniimo-Italian-Translation.exe`;
3. verifica dimensione e hash **SHA-256** pubblicati da GitHub;
4. sostituisce il vecchio installer e riapre automaticamente quello nuovo.

Al termine viene mostrata una conferma verde con versione precedente, versione attuale e indicazione che il riavvio automatico è riuscito.

Il nuovo installer viene riaperto in una console Windows visibile e indipendente, anche se l'assistente di sostituzione lavora in background. In questo modo il menu non può restare aperto invisibilmente.

L'installer impedisce l'apertura contemporanea di più finestre. Ogni tentativo di aggiornamento usa inoltre un file temporaneo distinto, evitando conflitti con download precedenti rimasti nella cache. Se il vecchio EXE è ancora occupato, compare un avviso visibile per chiudere le altre finestre e riprovare senza perdere il download verificato.

Questa funzione è disponibile dalla versione **0.3.0 beta** in poi. Se il controllo non è disponibile, per esempio perché il PC è offline, installazione e ripristino continuano a funzionare normalmente.

Se Aniimo riceve un aggiornamento non ancora verificato, il pannello lo segnala chiaramente. Il controllo delle chiavi di testo impedisce l'installazione su risorse incompatibili, salvo uso volontario dell'opzione avanzata `--force`.

Alcuni hot update mantengono lo stesso numero di versione del gioco. L'installer usa quindi build, fingerprint completo delle chiavi e struttura degli archivi per decidere la compatibilità. Un digest locale lasciato da una precedente installazione non viene considerato automaticamente una nuova revisione ufficiale; le informazioni diagnostiche sono visibili solo nei dettagli tecnici.

Se l'aggiornamento automatico non riesce, l'installer mostra sempre il collegamento per il download manuale.

## Crediti e collegamenti

L'installer mostra il collegamento GitHub direttamente nel pannello. Con l'opzione `5` è possibile visualizzare:

- crediti del progetto e della traduzione italiana: **Sici29**;
- repository GitHub;
- pagina per segnalare problemi;
- collegamento per sostenere il progetto.

## Segnala un problema

Puoi usare la sezione [Issues](https://github.com/Sici29/Aniimo-Italian-Translation/issues) per segnalare:

- una frase poco naturale o rimasta in inglese;
- un errore di genere o concordanza;
- un testo tagliato nell'interfaccia;
- un problema con installazione o ripristino.

Se possibile, allega uno screenshot e indica dove appare il testo.

<details>
<summary><strong>Informazioni per traduttori e sviluppatori</strong></summary>

Il repository usa un solo master autorevole:

- `data/translation_it.csv`: traduzione completa con accenti e punteggiatura italiana reali, installata nello slot English.

Dalla versione 0.3.6 non viene più mantenuta una seconda copia “accentata”: il font vietnamita incluso in Aniimo rende già correttamente tutti i caratteri italiani. Chiavi, tag, segnaposto, maiuscole funzionali, spazi e ritorni a capo vengono controllati automaticamente. Le date dinamiche vengono riordinate localmente in `GG/MM/AAAA` soltanto quando ogni pattern LuaJIT visibile corrisponde esattamente alla versione verificata; allo stesso modo, le unità CJK del timer vengono sostituite senza modificare la lunghezza dei metadati. Il repository non contiene archivi originali di Aniimo: testi, font, date e timer vengono modificati localmente a partire dai file della copia installata dall'utente.

</details>

## Nota legale

Questa è una traduzione amatoriale non ufficiale e non è affiliata agli sviluppatori o al publisher di Aniimo. Per utilizzarla è necessaria una copia installata del gioco.
