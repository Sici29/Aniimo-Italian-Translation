# Aniimo — Traduzione italiana 1.0.3629693.0

Aggiornamento completo per la nuova patch del client Steam **1.0.3629693.0** (build 3629693), con risoluzione del blocco del controllo di download della cache e avviso specifico per le installazioni non-Steam.

### Novità dell'aggiornamento:

- **Supporto ufficiale alla build Steam 3629693**:
  - Piena compatibilità con l'aggiornamento ufficiale di Aniimo rilasciato su Steam il 30 settembre 2026.
  - Catalogo espanso a **112.263 chiavi totali** con copertura al **100,00%** (49 nuove chiavi e 182 stringhe modificate, interamente tradotte e revisionate).
  - 0 stringhe mancanti o non tradotte.
- **Risoluzione del falso positivo di aggiornamento pendente (Issue #23)**:
  - Corretta la funzione di verifica della cache di gioco (`pending_cvs_download`): in precedenza l'archivio base originale di Steam (`StreamingAssets`) veniva confrontato con la nuova build generando un falso positivo che bloccava l'installazione anche dopo aver avviato il gioco.
  - L'installer ora verifica primariamente l'archivio attivo aggiornato dal gioco, sbloccando l'installazione per tutti gli utenti.
  - Aggiunta la possibilità interattiva di forzare l'installazione se desiderato e un consiglio diagnostico per ripulire la cache `Aniimo_Data\cvs\res\lua` qualora i file locali risultassero corrotti o bloccati.
- **Avviso per versioni non-Steam (Pawprint / standalone)**:
  - L'installer rileva automaticamente se la cartella selezionata non appartiene a un'installazione ufficiale di Steam e mostra un avviso chiaro ed esplicito per informare l'utente che le versioni non-Steam non sono ufficialmente supportate dalla patch italiana.
- **Selezione della lingua da sostituire (Inglese e Italiano insieme!)**:
  - Confermata e pienamente operativa la scelta della lingua da sostituire (opzione `8` nel menu o parametro `--target`): puoi sostituire una lingua alternativa (come Portoghese, Spagnolo, Francese o Tedesco) per conservare sia l'Inglese che l'Italiano e passare dall'uno all'altro nelle opzioni di Aniimo.
- **Qualità e test**:
  - Suite di test estesa a **161 test unitari**, tutti superati con successo (0 errori, 0 fallimenti).

### Installazione

1. Chiudi Aniimo e il launcher.
2. Apri **Aniimo-Italian-Translation.exe** e premi Invio (oppure opzione 8 per cambiare la lingua da sostituire).
3. Nel gioco seleziona la lingua sostituita (Inglese per impostazione predefinita, oppure la lingua scelta).

Se il gioco non viene trovato automaticamente, sposta l'installer accanto ad `Aniimo.exe` e riaprilo, oppure seleziona la cartella con l'opzione 4.
