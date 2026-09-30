# Verifiche tecniche — 1.0.3551601.0-R1

- Build verificata: Steam 3551601 / patch 1.0.3551601.0 (`steamapps\common\Aniimo`).
- Master traduzione: 112.187 chiavi; 112.187 tradotte in italiano (100,00%), 0 mancanti.
- Correzione Windows Defender CFA: cartella di lavoro predefinita `%LOCALAPPDATA%\AniimoItalianTranslation`, supporto a variabile `ANIIMO_WORK_DIR` e CLI `--work-dir`.
- Gestione `LuaCacheVer.txt`: salvataggio nel backup di ogni archivio Lua attivo, hashing SHA-256 nel manifest, ripristino bit-a-bit e risincronizzazione automatica per backup legacy.
- Usabilità: aggiunta funzione `open_backup_folder()` con comando menu `5` e subcommand CLI `backup-dir`.
- Suite test PyUnit: 132 test superati su 132 (0 fallimenti, 0 errori).
- Compilazione standalone con PyInstaller 6.15.0 con icona ufficiale italiana.
- Diagnostica standalone: rilevamento automatico Steam (`steamapps\common\Aniimo`), compatibilità 100% verde confermata.
