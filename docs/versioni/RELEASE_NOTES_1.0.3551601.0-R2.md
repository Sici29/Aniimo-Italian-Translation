# Aniimo — Traduzione italiana 1.0.3551601.0-R2

Revisione R2 per la patch del client Steam **1.0.3551601.0** (build 3551601).

Questa revisione risolve un problema critico di visualizzazione dei testi emerso su installazioni con cache preesistente o file sciolti (*loose files*):

- **Risolto problema dei testi troncati / sfasati in gioco**:
  - In precedenza, in presenza di un vecchio file `Compress_en.bin` nella cartella prioritaria di runtime (`Aniimo_Data\cvs\res\lua\LuaScripts\Data\I18N`), il motore del gioco combinava la nuova mappa dei testi con il vecchio buffer binario non sincronizzato, provocando lo slittamento dei byte e stringhe tagliate o incomplete (es. nei menu, scritte dei comandi e descrizioni di oggetti).
  - L'installer ora rileva la presenza di file di localizzazione sciolti non allineati (`check_loose_i18n_sync`), li segnala nell'interfaccia (`↑ FILE LINGUA DISALLINEATI`) e garantisce la sincronizzazione completa e bidirezionale in **tutti** gli archivi e percorsi di runtime del gioco (`StreamingAssets` e cartelle `cvs`).
- **Backup e ripristino multi-archivio per file sciolti**:
  - I file sciolti di localizzazione presenti in qualsiasi archivio attivo vengono ora tracciati singolarmente nel manifest di backup e rimossi/ripristinati in modo pulito al momento del ripristino (opzione 2).
- **Mantenute tutte le funzionalità introdotte con R1**:
  - Piena compatibilità con l'Accesso alle cartelle controllato di Windows Defender (cartella di lavoro in `%LOCALAPPDATA%\AniimoItalianTranslation`).
  - Supporto al parametro `--work-dir` e alla variabile d'ambiente `ANIIMO_WORK_DIR`.
  - Risincronizzazione e tracciamento rigoroso di `LuaCacheVer.txt`.
  - Apertura immediata della cartella dei backup (opzione 5 / `backup-dir`).
- **Traduzione invariata al 100,00%**: 112.187 chiavi su 112.187 tradotte con zero fallback e piena compatibilità terminologica.

### Installazione

1. Chiudi Aniimo e il launcher.
2. Apri **Aniimo-Italian-Translation.exe** e premi Invio.
3. In gioco seleziona **Inglese**.

Se il percorso non viene trovato automaticamente, sposta l'installer accanto ad Aniimo.exe e riaprilo, oppure seleziona la cartella con l'opzione 4.
