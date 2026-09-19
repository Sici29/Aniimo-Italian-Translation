# Verifiche tecniche — 1.0.3551601.0-R2

- Build verificata: Steam 3551601 / patch 1.0.3551601.0 (`D:\SteamLibrary\steamapps\common\Aniimo`).
- Master traduzione: 112.187 chiavi; 112.187 tradotte in italiano (100,00%), 0 mancanti.
- Correzione disallineamento file I18N sciolti: funzione `check_loose_i18n_sync`, rilevamento disallineamento in `detect_translation_installation` e sincronizzazione multi-archivio in `copy_patch_into_game`.
- Tracciamento e ripristino per-archivio di `Compress_{lang}.bin` e `NewTextMap_{lang}.json` in `backup_manifest.json` e `cmd_restore`.
- Test decodifica stringhe in-game: verificate chiavi precedentemente corrotte (1099705801, 1208281719, 1830394518, 1901756109, 2041156366), 100% integre e leggibili in italiano.
- Suite test PyUnit: 132 test superati su 132 (0 fallimenti, 0 errori).
- Compilazione standalone con PyInstaller 6.15.0 con icona ufficiale italiana (`SHA-256: 8735B309E42447163C3C4B9B34BEBBB2EC44FCBDA9B1E23611164EEA0BD70330`).
- Diagnostica standalone: rilevamento automatico Steam `D:\SteamLibrary\steamapps\common\Aniimo`, compatibilità 100% verde confermata e `loose_i18n_in_sync = True`.
