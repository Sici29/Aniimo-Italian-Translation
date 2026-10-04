# Aniimo — Traduzione italiana 1.0.3634150.1

Release correttiva per la build Steam **3634150**, incentrata sulla risoluzione completa di tutte le disallineazioni storiche segnalate nella **Issue #25** (grazie a @Kaen89!).

### Novità e correzioni dell'aggiornamento:

- **Risoluzione disallineamenti storici nel catalogo (Issue #25)**:
  - Corrette **105 chiavi complessive** che presentavano testi italiani scambiati o associati a chiavi errate (ereditati dalle prime versioni beta del progetto).
  - Tra queste:
    - Titolo missione principale `1829593311`: corretto da *"Ricevere un regalo da un amico conferisce 30 punti Affinità bonus."* a **"Valutazione: Testimone della Luce Stellare"** (*Assessment: Starlight's Witness*).
    - Descrizioni dei chip, degli amplificatori d'attacco temporanei e delle unità protettive (*Illusory Attack Amplifier - Might/Tactics*, *Illusory Advanced Capacity Expansion Chip*, ecc.).
    - Nomi, battute e descrizioni delle decorazioni dei Susuta (*Sunset Susuta*, *Splashy Susuta*, *Spring Stroll Susuta*, ecc.).
    - Testi di sistema e di avviso manutenzione server, supporto dispositivi e personalizzazione personaggio.
    - Casi dubbi verificati e corretti: `1173585695` *Home Girl* → **"Ragazza Casalinga"**, `1782344601` *Mantis Lady* → **"Signora Mantide"**, `1745656882` *Lin Xi's Rest Set* → **"Set Riposo di Lin Xi"**.
    - Ripristinati i segnaposto e titoli invertiti per `{0} {1}` e *The Land Reawakens* (chiavi `1226459316`, `1241323712`, `1991632583`).
    - Corretto parametro del buff per la Benedizione Spinosa (`1573680957`).
- **Verifiche di qualità e coerenza terminologica**:
  - Ogni stringa è stata revisionata confrontandola con i testi originali in inglese e le versioni ufficiali in francese e spagnolo per garantire coerenza contestuale e concordanza grammaticale.
  - Tutti i tag (`<customRichText(...)>`, `<style=...>`, `<color=...>`) e segnaposto (`{0}`, `{1}`) sono stati convalidati con test di coerenza automatica al 100%.
- **Suite di test**:
  - Tutti i **161 test unitari superati con successo**.
  - Installazione e verifica live con esito 100% compatibile sui file reali di Steam.

### Installazione

1. Chiudi Aniimo e il launcher.
2. Apri **Aniimo-Italian-Translation.exe** e premi Invio (oppure opzione 8 per cambiare la lingua da sostituire).
3. Nel gioco seleziona la lingua sostituita (Inglese per impostazione predefinita, oppure la lingua scelta).

Se il gioco non viene trovato automaticamente, sposta l'installer accanto ad `Aniimo.exe` e riaprilo, oppure seleziona la cartella con l'opzione 4.
