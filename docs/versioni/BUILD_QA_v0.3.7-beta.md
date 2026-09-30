# Build QA — v0.3.7 beta

## Artefatto candidato

- File: `Aniimo-Italian-Translation.exe`
- Dimensione: 22.601.536 byte
- SHA-256: `AE1C53D035DD20C9DDF365B26EA949568ACE94E99F4032B3C070395823060A1C`

## Verifiche automatiche

- 54 test completati con esito positivo.
- 92.954 chiavi di traduzione presenti.
- 359 fallback significativi dello slot English recuperati.
- 359 chiavi aggiunte all'elenco runtime delle traduzioni English disponibili.
- 726 notifiche a riga singola identificate e controllate.
- 78 notifiche accorciate; massimo 80 caratteri visibili, tag esclusi.
- 14 bolle `Indizio` controllate; 4 accorciate e massimo reale di 32 caratteri visibili sul limite di 34.
- 151 residui inglesi o misti corretti nella v0.3.7, conservando i toponimi dichiarati invariabili dal glossario.
- Tag colore, tag di stile e placeholder conservati nelle notifiche revisionate.

## Prova d'installazione isolata

L'EXE è stato eseguito su una copia isolata delle risorse della versione gioco 3036569.

- Installazione completata senza errori.
- Versione registrata: `0.3.7-beta`.
- Slot di destinazione: English.
- Font: `UI_Font_Vietnamese`, con accenti italiani completi.
- Elenco English disponibile: 10.257 voci, contro le 9.898 dell'installazione precedente.
- Le chiavi `1409838404` e `1832874807` sono presenti sia nell'elenco disponibile sia nella mappa italiana.
- `Three...` è installato come `Tre...`.
- Nessuna delle 726 notifiche note supera il limite di 80 caratteri visibili.
- Nessuna delle 14 bolle `Indizio` supera il limite di 34 caratteri visibili.
- `Old Town`, `Hall of Memories` e `Roll Out` risultano uniformati rispettivamente in `Città Vecchia`, `Sala dei Ricordi` e `Palla di fango rotolante`.

## Verifica finale in gioco

- La candidata è stata installata nella copia reale della versione gioco 3036569.
- Verificate direttamente nelle risorse installate tutte le 92.954 chiavi e le 10.257 voci dell'elenco English disponibile.
- Confermati `Tre...`, le due scelte di dialogo recuperate, i quattro indizi compatti, `Città Vecchia` e `Palla di fango rotolante`.
- Confermate anche le 24 etichette brevi dell'ultimo audit, comprese `Cioccolata Calda`, `Tempesta di Ghiaccio`, `Tappetino per Mouse`, la famiglia Gabbiano e `Chat: {0}`.
- Resta consigliata una prova visiva in gioco delle due scelte, perché il problema originario dipendeva dal percorso fallback del runtime.
