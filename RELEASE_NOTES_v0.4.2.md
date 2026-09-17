# Aniimo — Traduzione italiana v0.4.2

Release per il client Steam (build 3544783).

- **112.187 chiavi su 112.187 tradotte in italiano (100,00%)**, zero fallback e zero stringhe mancanti.
- Supporto e traduzione completa della nuova build Steam **3544783**:
  - Integrate le 4 nuove stringhe introdotte dagli sviluppatori (oggetti vincolati Sol Lion/Lunara, sblocco desideri, Edizione contratto Zanna Feroce).
  - Revisionate e aggiornate tutte le 97 stringhe modificate (aggiornamento terminologico Hexxin, eventi crossover Sparkelf, requisiti livello 45/50/55, limiti settimanali Monete Voxel, nutrizione degli ecosistemi ai Rami).
- Installer aggiornato con sincronizzazione tra StreamingAssets e cache cvs: garantisce priorità automatica all'archivio più recente quando Steam rilascia una nuova versione, applicando la traduzione a tutti gli archivi di gioco.
- Un solo file EXE standalone con rilevamento prioritario automatico di Steam, fallback Pawprint e supporto a selezione manuale o posizionamento nella root del gioco.
- Rilevamento dinamico per future versioni di Aniimo: compatibilità automatica 100% se i testi non cambiano, fallback selettivo all'inglese con avviso per eventuali nuove stringhe.
- Backup automatico ad ogni installazione e ripristino immediato con opzione 2.

### Installazione

1. Chiudi Aniimo e il launcher.
2. Apri **Aniimo-Italian-Translation.exe** e premi Invio.
3. In gioco seleziona **Inglese**.

Se il percorso non viene trovato automaticamente, sposta l'installer accanto ad Aniimo.exe e riaprilo, oppure seleziona la cartella con l'opzione 4.
