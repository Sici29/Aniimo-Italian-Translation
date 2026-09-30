# Aniimo — Traduzione italiana 1.0.3551601.0

Release per la patch del client Steam **1.0.3551601.0** (build 3551601).

- **Adozione del nuovo schema di versioning ufficiale**: la numerazione delle versioni della traduzione adotta direttamente il numero di patch del gioco (`1.0.<build>.0`), con suffissi `-R1`, `-R2`, ecc. riservati per eventuali revisioni testuali della stessa build.
- **112.187 chiavi su 112.187 tradotte in italiano (100,00%)**, zero fallback e zero stringhe mancanti.
- Supporto nativo per la nuova build Steam **3551601** (patch 1.0.3551601.0):
  - Verifica integrale dei testi del client: 0 stringhe modificate o aggiunte rispetto al master di gioco verificato (compatibilità al 100%).
  - Riconoscimento e supporto del nuovo bundle font Steam aggiornato (`bb25716c229ac94cbe6a0ffdadcf48aa`).
- Installer standalone `Aniimo-Italian-Translation.exe` aggiornato:
  - Rilevamento prioritario automatico della libreria Steam e installazioni personalizzate.
  - Sincronizzazione automatica tra `StreamingAssets` e cache `cvs`.
  - Motore di compatibilità dinamica: verifica in tempo reale le stringhe di gioco ad ogni patch; se una patch futura non cambia testi procede al 100%, altrimenti applica il fallback alle sole stringhe nuove.
  - Backup automatico ad ogni installazione e ripristino immediato con opzione 2.

### Installazione

1. Chiudi Aniimo e il launcher.
2. Apri **Aniimo-Italian-Translation.exe** e premi Invio.
3. In gioco seleziona **Inglese**.

Se il percorso non viene trovato automaticamente, sposta l'installer accanto ad Aniimo.exe e riaprilo, oppure seleziona la cartella con l'opzione 4.
