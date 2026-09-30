# Aniimo — Traduzione italiana 1.0.3551601.0-R1

Revisione R1 per la patch del client Steam **1.0.3551601.0** (build 3551601).

Questa revisione introduce importanti correzioni di compatibilità e usabilità emerse dai test della community su GitHub:

- **Risolto errore `[WinError 2]` con Windows Defender (Accesso alle cartelle controllato)**:
  - Spostata la cartella predefinita per backup, impostazioni, cache di aggiornamento e lock in `%LOCALAPPDATA%\AniimoItalianTranslation`.
  - Windows Defender Controlled Folder Access protegge `%USERPROFILE%\Documents` bloccando le creazioni di directory; `%LOCALAPPDATA%` non è soggetto a questi blocchi ed è il percorso standard raccomandato su Windows.
  - Aggiunto il supporto alla variabile d'ambiente `ANIIMO_WORK_DIR` e al parametro da riga di comando `--work-dir <percorso>` per consentire una configurazione completamente personalizzata.
  - Mantenuta la lettura automatica e trasparente dei backup precedenti in `Documents`, protetta da eccezioni di sicurezza.
- **Risolto disallineamento al ripristino di `LuaCacheVer.txt`**:
  - `LuaCacheVer.txt` viene ora salvato nel backup di ciascun archivio Lua e verificato tramite hash SHA-256 nel manifest.
  - Durante l'installazione, `LuaCacheVer.txt` viene sincronizzato con la dimensione e l'hash del nuovo `LuaScripts.xdt`.
  - Durante il ripristino (opzione 2), `LuaCacheVer.txt` viene ripristinato fedelmente dal backup. Per eventuali backup creati con versioni precedenti, l'installer risincronizza automaticamente la riga con la versione, dimensione e hash del file originale ripristinato.
- **Accesso immediato alla cartella dei backup (opzione 5)**:
  - Aggiunta l'opzione **5** nel menu principale per mostrare il percorso esatto ed aprire direttamente la cartella dei backup in Esplora file di Windows.
- **Traduzione invariata al 100,00%**: 112.187 chiavi su 112.187 tradotte con zero fallback e piena compatibilità terminologica.

### Installazione

1. Chiudi Aniimo e il launcher.
2. Apri **Aniimo-Italian-Translation.exe** e premi Invio.
3. In gioco seleziona **Inglese**.

Se il percorso non viene trovato automaticamente, sposta l'installer accanto ad Aniimo.exe e riaprilo, oppure seleziona la cartella con l'opzione 4.
