# Aniimo Traduzione Italiana

Traduzione italiana amatoriale per **Aniimo**, pensata per essere semplice da installare e facile da aggiornare quando il gioco riceve nuove patch.

## Sostieni La Traduzione

Se la traduzione ti è utile e vuoi contribuire a mantenerla aggiornata, puoi offrirmi un caffè. Anche un piccolo sostegno aiuta a portare avanti il progetto e le future traduzioni italiane.

[![Offrimi un caffè e sostieni la traduzione italiana](https://img.shields.io/badge/Offrimi_un_caff%C3%A8-Sostieni_la_traduzione-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=000000)](https://buymeacoffee.com/sici29)

**Grazie di cuore a chi sceglierà di supportare il progetto.**

## Stato

- Copertura: **92.954 / 92.954** stringhe note.
- Versione testata: **hot update 3036569**.
- Versione traduzione: **0.1.0 beta**.
- Installazione consigliata: slot **English**.

La patch sostituisce lo slot inglese perché è sempre visibile nel menu lingua del gioco.

## Installazione Rapida

1. Chiudi Aniimo e il launcher.
2. Scarica `Aniimo-Italian-Translation.exe` da **Releases**.
3. Copia l'eseguibile nella root del gioco, cioè nella cartella dove si trova `Aniimo_Data`.
4. Avvia `Aniimo-Italian-Translation.exe`.
5. Apri il gioco e seleziona **English**.

Esempio di cartella corretta:

```text
Aniimo\game\
  Aniimo_Data\
  Aniimo-Italian-Translation.exe
```

L'eseguibile contiene già traduzione e installer: non servono Python, cartelle extra o altri file.

Se lo avvii fuori dalla cartella del gioco, prova comunque a trovare Aniimo da solo, sia nella versione launcher sia in eventuali librerie Steam. Se non riesce, puoi indicare il percorso manualmente:

```powershell
Aniimo-Italian-Translation.exe install --game-dir "F:\Pawprint\Aniimo\game"
```

## Ripristino

Per tornare ai file precedenti:

1. Chiudi Aniimo e il launcher.
2. Avvia `Aniimo-Italian-Translation.exe`.
3. Scegli **Ripristina ultimo backup** dal menu.

I backup vengono salvati in:

```text
Documenti\AniimoItalianTranslation\backups
```

## Accenti E Compatibilita'

La patch pubblica usa lo slot **English**. Al momento quel font non mostra bene molte lettere accentate italiane: per evitare parole troncate come `Qualit`, la versione installata converte gli accenti in apostrofi (`qualita'`, `perche'`, `abilita'`, `puo'`, `gia'`, `piu'`).

La traduzione master con accenti reali viene comunque conservata nel progetto di lavoro. Se in futuro Aniimo aggiungera' uno slot con font latino completo, o se sara' possibile usare uno slot come spagnolo/francese/tedesco, la patch potra' tornare agli accenti corretti senza rifare la traduzione da zero.

## Aggiornamenti Del Gioco

Aniimo è in beta, quindi può cambiare spesso. L'installer controlla le stringhe del gioco prima di applicare la patch.

L'installer controlla anche GitHub all'avvio: se trova una release più nuova, ti mostra il link e ferma l'installazione per evitare di applicare una versione vecchia.

Puoi controllare manualmente gli aggiornamenti avviando:

```text
Aniimo-Italian-Translation.exe update
```

Se dopo un aggiornamento appare un errore di versione non riconosciuta, non forzare l'installazione a caso: apri una segnalazione su GitHub e aggiornerò la traduzione.

## Feedback E Segnalazioni

Sì, puoi segnalare problemi direttamente su GitHub nella scheda **Issues**.

Quando segnali un errore, se possibile includi:

- screenshot del testo;
- punto del gioco in cui appare;
- testo attuale e testo suggerito;
- versione del gioco o del launcher;
- tipo di problema: testo inglese rimasto, frase poco naturale, apostrofo mancante, maschile/femminile errato, UI tagliata, installazione.

## Richiedi Una Traduzione

Vuoi proporre un altro gioco da tradurre in italiano?

Apri una Issue usando il template **Richiesta traduzione** e indica:

- nome del gioco;
- piattaforma o launcher;
- link Steam/Epic/sito ufficiale;
- se il gioco è Unity, Unreal o altro, se lo sai;
- quante parti vuoi tradotte: menu, sottotitoli, dialoghi, texture, immagini, ecc.;
- se esiste già una traduzione amatoriale da cui prendere spunto.

Non posso promettere che ogni gioco sia traducibile o pubblicabile, ma una richiesta fatta bene aiuta tantissimo a capire se il lavoro è realistico.

## Note

Questa è una traduzione amatoriale non ufficiale. Non è affiliata agli sviluppatori o publisher di Aniimo.

La repository non include archivi originali del gioco: l'installer genera la patch localmente usando i file della tua copia installata. Per usare la traduzione devi possedere e avere installato Aniimo.
