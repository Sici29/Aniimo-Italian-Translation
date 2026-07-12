# Build QA — v0.3.10 beta

## Contenuto

- Versione traduzione: `0.3.10-beta`
- Chiavi nel master: `92.954`
- Correzioni audit completo dei generi: `158`
- Associazioni battuta→parlante controllate: `7.672`
- Speaker controllati: `290`
- Candidati grammaticali revisionati: `550`
- Output pubblico previsto: un solo `Aniimo-Italian-Translation.exe`

## Controlli obbligatori

- [x] Manifesto delle correzioni applicato integralmente e in modo idempotente.
- [x] Concordanze di Sunia verificate per chiave.
- [x] Personaggi femminili e maschili confermati confrontati con inglese e giapponese.
- [x] Russo usato soltanto come conferma quando semanticamente allineato.
- [x] Protagonista selezionabile neutralizzato nelle chiavi senza coppia maschile/femminile.
- [x] Tre coppie runtime maschile/femminile già note conservate separate.
- [x] Tag, segnaposto e struttura del master preservati.
- [x] Tutti i 59 test automatici superati.
- [x] Build pulita dell'EXE con tutte le dipendenze UnityPy incluse.
- [x] Installazione isolata verificata su una copia originale del gioco.
- [x] Tutte le 92.954 stringhe installate coincidono byte per byte con il master.
- [x] Tutte le 158 correzioni dell'audit risultano presenti nell'archivio installato.
- [x] Font accentato verificato: lo slot English usa il font vietnamita incluso in Aniimo.
- [x] XDF/XDT verificati: UTF-8, offset, versione map/BIN, dimensioni e MD5 coerenti.
- [x] Ripristino verificato: il fixture torna identico all'originale per percorsi, dimensioni e SHA-256.

## Artefatto verificato

- File: `Aniimo-Italian-Translation.exe`
- Dimensione: `33.908.094` byte
- SHA-256: `A2A0719E82A767956FDBB482063BF7E81C2922F49D93895854EA93826284CB80`

## Da completare durante il rilascio

- [ ] Release GitHub normale, non pre-release, impostata come Latest.
