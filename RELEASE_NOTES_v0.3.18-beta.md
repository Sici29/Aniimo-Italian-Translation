# Aniimo — Traduzione italiana v0.3.18 Beta

Questa release corregge definitivamente un fallback runtime che poteva mostrare in inglese 359 battute già tradotte e conferma la compatibilità con la build Aniimo `3064863`.

## Novità principali

- Verificata la build `3064863`: 93.029 chiavi e contenuti English identici alla build precedente, quindi nessuna nuova stringa da tradurre.
- Corretto l'elenco interno `AITranslatedItems_en` usato da Aniimo: tutte le 359 chiavi storicamente recuperate vengono ora abilitate esplicitamente.
- Risolte così le cinque battute English segnalate nella sequenza introduttiva di Fannie e ogni altra riga appartenente alla stessa categoria.
- Rilette e rifinite le cinque traduzioni, mantenendo tag, ritorni a capo e terminologia della Base.
- Aggiunta una nuova icona dell'installer con mascotte Aniimo e badge della bandiera italiana, completa di trasparenza e dimensioni Windows da 16 a 256 pixel.

## Verifiche

- Copertura completa: 93.029 / 93.029 testi.
- 359 / 359 fallback storici inclusi nell'elenco runtime italiano.
- Le cinque chiavi segnalate sono presenti nel master, nell'archivio generato e nell'elenco runtime corretto.
- Strutture tecniche, font accentato, date italiane e timer verificati.
- 104 test automatici superati.

## Installazione

1. Chiudi Aniimo e il launcher Pawprint.
2. Scarica `Aniimo-Italian-Translation.exe`.
3. Apri l'installer e premi **Invio**.
4. Nel gioco seleziona **Inglese**.

Chi usa una versione precedente deve reinstallare la traduzione con questo EXE per applicare la correzione ai fallback. La release contiene un solo file eseguibile.
