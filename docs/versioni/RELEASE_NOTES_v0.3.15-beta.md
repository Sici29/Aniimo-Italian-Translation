# Aniimo — Traduzione italiana v0.3.15 Beta

Questa release corregge definitivamente i formati data visibili e il conto alla rovescia con unità cinesi, oltre a due segnalazioni sulla traduzione.

## Novità principali

- Tutte le superfici data verificate usano ora `GG/MM/AAAA`: capitoli missione, `Astra Era`, posta, album, dettagli foto, registri attività e pannelli evento.
- L'installer gestisce entrambe le copie degli archivi Lua presenti nella build 3048640, ricostruendole separatamente e verificandole dopo la copia.
- Il timer delle card del negozio passa da un formato come `15分0秒` a `15 m 0 s`.
- `Gratis` viene ridimensionato soltanto nelle otto etichette strette, così non viene più spezzato su due righe.
- Jilly si riferisce correttamente a sé stessa con `Sono impressionata`.

## Sicurezza dell'installazione

- Backup e ripristino includono ora entrambe le coppie `LuaScripts.xdf/xdt` e i metadati runtime del timer.
- Ogni backup registra gli hash SHA-256 dei file aggiuntivi.
- Gli archivi generati vengono aperti, verificati e confrontati con i relativi indici prima e dopo l'installazione.
- La patch delle date e quella del timer sono idempotenti e vengono rifiutate se il file del gioco non corrisponde esattamente alla struttura verificata.
- I backup creati dalle versioni precedenti dell'installer restano ripristinabili.

## Installazione

1. Chiudi Aniimo e il launcher Pawprint.
2. Scarica `Aniimo-Italian-Translation.exe`.
3. Apri l'installer e premi **Invio**.
4. Nel gioco seleziona **Inglese**.

La release contiene un solo file EXE. Non servono Python, estrazioni manuali o programmi aggiuntivi.
