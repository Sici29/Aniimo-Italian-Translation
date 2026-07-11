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

All'apertura compare un riepilogo semplice con:

- versione del gioco supportata e versione rilevata;
- revisione dell'hot update, anche quando il numero del gioco non cambia;
- compatibilità reale verificata confrontando tutte le chiavi dei testi;
- percorso del gioco trovato automaticamente o inserito dall'utente;
- traduzione italiana già installata oppure non installata;
- stato di compatibilità evidenziato a colori;
- versione dell'installer in uso;
- eventuale nuova versione disponibile.

L'installer cerca automaticamente il gioco, controlla la compatibilità e crea un backup prima di modificare qualsiasi file.

### 4. Seleziona English nel gioco

Avvia Aniimo e scegli **English** dal menu della lingua. La traduzione italiana sostituisce temporaneamente quello slot.

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

- Copertura: **92.954 / 92.954 stringhe**.
- Versione del gioco verificata: **3032670**.
- Revisione hot update verificata: **7113f88e39827a2d13591a55b395f1c6**.
- Versione della traduzione: **0.3.4 beta**.
- Lingua da selezionare nel gioco: **English**.
- Revisione: terminologia, dialoghi, generi, UI, tag, spaziature e naturalezza dell'italiano.

## Perché alcune parole usano l'apostrofo?

Il font associato allo slot English non mostra correttamente molte lettere accentate italiane. Per evitare parole troncate come `Qualit`, la versione installata usa temporaneamente forme come:

```text
qualita'   perche'   puo'   gia'   piu'
```

L'apostrofo sostituisce soltanto un accento italiano finale. Non viene inserito dentro le parole: termini come `Elite` e nomi come `Timothee` restano leggibili e non diventano `E'lite` o `Timothe'e`.

Il progetto conserva anche il master completo con accenti reali (`qualità`, `perché`, `può`, `già`, `più`). È già pronto per sostituire la versione attuale non appena il gioco offrirà un font compatibile.

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

Alcuni hot update mantengono lo stesso numero di versione del gioco. Per questo l'installer mostra separatamente la revisione delle risorse e la compatibilità effettiva dei testi. La revisione ufficiale viene conservata anche dopo l'applicazione della traduzione.

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

Il repository contiene due file sincronizzati:

- `data/translation_it_accented.csv`: master editoriale con accenti e punteggiatura italiana reali;
- `data/translation_it.csv`: versione derivata per il font dello slot English.

Chiavi, tag, segnaposto, maiuscole funzionali, spazi e ritorni a capo vengono controllati automaticamente. Il repository non contiene archivi originali di Aniimo: la patch viene generata localmente dai file della copia installata dall'utente.

</details>

## Nota legale

Questa è una traduzione amatoriale non ufficiale e non è affiliata agli sviluppatori o al publisher di Aniimo. Per utilizzarla è necessaria una copia installata del gioco.
