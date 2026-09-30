# Aniimo — Traduzione italiana 1.0.3616231.0

Aggiornamento completo per la nuova patch del client Steam **1.0.3616231.0** (build 3616231) con supporto alla selezione della lingua da sostituire.

### Novità dell'aggiornamento:

- **Selezione della lingua da sostituire (Inglese e Italiano insieme!)** *(grazie a @Kaen89 — PR #22)*:
  - Ora puoi scegliere quale lingua sostituire con l'Italiano: puoi mantenere l'Inglese intatto e sacrificare un'altra lingua che non utilizzi (ad es. il Portoghese `pt_PT`, lo Spagnolo `es_ES`, il Francese `fr_FR`, il Tedesco `de_DE`, ecc.).
  - Nelle impostazioni di lingua di Aniimo rimarranno disponibili sia **English** che **Italiano**, permettendoti di passare comodamente dall'uno all'altro in qualunque momento senza disinstallare nulla (ideale per giocare con amici esteri o confrontare termini).
  - La lingua da sostituire può essere selezionata dall'installer interattivo (opzione `8`) oppure tramite riga di comando (`--target <slot>`).
  - **100% retrocompatibile**: premendo semplicemente Invio al primo avvio, l'installer continua a sostituire l'inglese di default come sempre.
- **Supporto ufficiale alla build Steam 3616231**:
  - Piena compatibilità con l'aggiornamento di Aniimo rilasciato il 28 settembre 2026.
  - Catalogo aggiornato a **112.214 chiavi totali** con copertura professionale al **100,00%** (zero stringhe mancanti o non tradotte).
  - Tradotta la nuova funzione di emergenza **Unstuck** (*"Sbloccati"*) presente nei menu e nelle impostazioni per liberare il personaggio o l'Aniimo dalla mappa.
  - Tradotta la nuova notifica per i pigmenti speciali (*"Questo Aniimo è una variante speciale e non può usare questo Pigmento Scintillante."*).
  - Aggiornate le descrizioni dei trasformatori di Forma Prismana (per Whisperwake Isles e Breezy Plains) per riflettere le nuove regole sulle forme sbloccate e il mantenimento dei Potenziali Acquisiti.
- **Guardia automatica sul download del patcher di gioco**:
  - L'installer rileva automaticamente se Steam ha aggiornato l'eseguibile mentre la cartella `cvs` deve ancora essere sincronizzata dal client di gioco, evitando che la traduzione venga inavvertitamente sovrascritta al primo avvio.
- **Qualità e test**:
  - Suite di test estesa a **159 test unitari** interamente superati (copertura totale di regressione, integrità dei 13 slot lingua e sicurezza dei backup).

### Installazione

1. Chiudi Aniimo e il launcher.
2. Apri **Aniimo-Italian-Translation.exe** e premi Invio (oppure opzione 8 per cambiare la lingua da sostituire).
3. Nel gioco seleziona la lingua sostituita (Inglese per impostazione predefinita, oppure la lingua scelta).

Se il gioco non viene trovato automaticamente, sposta l'installer accanto ad `Aniimo.exe` e riaprilo, oppure seleziona la cartella con l'opzione 4.
