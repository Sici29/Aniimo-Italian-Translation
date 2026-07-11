# Aniimo — Traduzione italiana v0.3.0 Beta

Questa release rende l'installer più semplice e autonomo, senza cambiare la traduzione completa già revisionata.

## Novità principali

- aggiornamento automatico confrontato con la release GitHub più recente;
- download del nuovo EXE verificato tramite dimensione e hash SHA-256;
- sostituzione e riavvio automatici dell'installer su Windows;
- pannello iniziale con versione gioco supportata e rilevata, compatibilità, versione installer attuale e nuova versione disponibile;
- rilevamento reale della versione del gioco tramite `verlist.txt`;
- supporto verificato per Aniimo `3032670`.

## Installazione

1. Chiudi Aniimo e il launcher.
2. Scarica **solo** `Aniimo-Italian-Translation.exe` qui sotto.
3. Aprilo e premi **Invio**.
4. Avvia il gioco e seleziona **English**.

Non servono Python, programmi aggiuntivi o archivi da estrarre. Dalla versione 0.3.0 beta, i futuri aggiornamenti dell'installer potranno essere applicati direttamente dall'EXE.

## Sicurezza e ripristino

Prima dell'installazione viene creato automaticamente un backup. Per ripristinare i file originali, riapri l'installer, digita `2` e premi **Invio**.

Se GitHub non fornisce un hash SHA-256 valido o il download non coincide, l'aggiornamento automatico viene annullato e il vecchio installer non viene modificato.
