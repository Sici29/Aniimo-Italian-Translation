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

L'installer cerca automaticamente il gioco, controlla che la versione sia compatibile e crea un backup prima di modificare qualsiasi file.

### 4. Seleziona English nel gioco

Avvia Aniimo e scegli **English** dal menu della lingua. La traduzione italiana sostituisce temporaneamente quello slot.

> Non servono Python, programmi aggiuntivi, archivi da estrarre o configurazioni manuali.

## Se l'installer non trova Aniimo

Copia `Aniimo-Italian-Translation.exe` nella cartella del gioco, accanto a `Aniimo_Data`, quindi riaprilo:

```text
Aniimo\game\
├── Aniimo_Data\
└── Aniimo-Italian-Translation.exe
```

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
- Versione del gioco verificata: **hot update 3036569**.
- Versione della traduzione: **0.2.1 beta**.
- Lingua da selezionare nel gioco: **English**.
- Revisione: terminologia, dialoghi, generi, UI, tag, spaziature e naturalezza dell'italiano.

## Perché alcune parole usano l'apostrofo?

Il font associato allo slot English non mostra correttamente molte lettere accentate italiane. Per evitare parole troncate come `Qualit`, la versione installata usa temporaneamente forme come:

```text
qualita'   perche'   puo'   gia'   piu'
```

Il progetto conserva anche il master completo con accenti reali (`qualità`, `perché`, `può`, `già`, `più`). È già pronto per sostituire la versione attuale non appena il gioco offrirà un font compatibile.

## Aggiornamenti

L'installer controlla automaticamente se è disponibile una traduzione più recente. Se Aniimo riceve un aggiornamento non ancora supportato, l'installazione viene fermata per evitare di danneggiare i file del gioco.

In quel caso, scarica l'ultima release oppure apri una segnalazione.

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
