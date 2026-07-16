# Aniimo — Traduzione italiana v0.3.17 Beta

Questa release rende la compatibilità dell'installer automatica e aggiunge il supporto completo alla build Aniimo `3062823`.

## Novità principali

- L'installer non dipende più soltanto dal numero di build: confronta tutte le chiavi e il contenuto reale dei testi del gioco.
- Le future build con localizzazione invariata vengono riconosciute automaticamente come compatibili, senza richiedere una nuova versione dell'installer.
- Se il gioco aggiunge, rimuove o modifica testi ufficiali, l'installazione viene fermata finché le nuove stringhe non sono state revisionate.
- Verificata automaticamente la build `3058113`, che conserva le stesse 93.029 chiavi e gli stessi testi della build precedente.
- Integrata la build `3062823`: 2 chiavi aggiunte, 2 rimosse e 28 sorgenti English modificate, per un totale invariato di 93.029 chiavi.
- Tradotte e revisionate tutte le 30 righe interessate, inclusi Closed Beta Globale, Lancio Globale, premi evento, check-in, Sensore di movimento ed elenco dei bloccati.

## Verifiche

- Copertura completa: 93.029 / 93.029 testi.
- Nessuna stringa nuova o sconosciuta rimasta nella build `3062823`.
- Strutture tecniche, font accentato, date italiane e timer verificati.
- 103 test automatici superati.

## Installazione

1. Chiudi Aniimo e il launcher Pawprint.
2. Scarica `Aniimo-Italian-Translation.exe`.
3. Apri l'installer e premi **Invio**.
4. Nel gioco seleziona **Inglese**.

La release contiene un solo file EXE. Non servono Python, estrazioni manuali o programmi aggiuntivi.
