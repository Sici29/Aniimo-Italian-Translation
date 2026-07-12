# Build QA — v0.3.11 beta

## Contenuto

- Versione traduzione: `0.3.11-beta`
- Chiavi nel master: `92.954`
- Correzioni uniche dell'audit qualità: `714`
- Candidati di genere revisionati: `836`
- Speaker controllati: `290`
- Output pubblico previsto: un solo `Aniimo-Italian-Translation.exe`

## Controlli obbligatori

- [x] Manifesto di 714 correzioni applicato integralmente e in modo idempotente.
- [x] Tutte le 92.954 righe sottoposte agli audit di genere, inglese, troncamento e naturalezza.
- [x] Inglese, giapponese e contesto confrontati nei casi di genere; russo usato solo come fonte secondaria.
- [x] Zero tag, segnaposto o codici di controllo alterati.
- [x] Zero flessioni artificiali con slash residue.
- [x] Zero residui delle famiglie terminologiche obbligatorie.
- [x] Tutti i 63 test automatici superati.
- [x] Build pulita dell'EXE con UnityPy e NumPy incluse.
- [x] Installazione isolata completata: 92.954/92.954 stringhe coincidenti col master.
- [x] Font accentato verificato: lo slot English usa il font vietnamita incluso in Aniimo.
- [x] Ripristino isolato verificato: 7/7 file identici per percorso, dimensione e SHA-256.
- [x] Installazione reale completata e verificata con rapporto di corrispondenza `1.0`.

## Artefatto verificato

- File: `Aniimo-Italian-Translation.exe`
- Dimensione: `33.974.316` byte
- SHA-256: `E5C822F436020B0ABEA5B459F1A3A12BDD810683D5DACDA2CD54C3A27EA30CCB`

## Da completare durante il rilascio

- [ ] Release GitHub normale, non pre-release, impostata come Latest.
