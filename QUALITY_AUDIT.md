# Audit qualità v0.3.11

La v0.3.11 sottopone l'intero master italiano a una nuova revisione globale, riproducibile e distinta dagli audit precedenti.

## Copertura

- 92.954 righe e 92.954 chiavi uniche controllate.
- 42.637 testi sorgente inglesi unici confrontati.
- 7.672 dialoghi attribuiti al rispettivo parlante tramite i dati runtime.
- 290 speaker e 836 candidati di genere revisionati.
- 772 testi appartenenti alle famiglie UI con limiti noti ricontrollati.

## Correzioni applicate

Il manifesto `data/quality_audit_v0.3.11.json` registra **714 chiavi corrette** e conserva per ognuna testo precedente, testo finale, ambito e motivazione.

- 110 proposte confermate per testi rivolti al protagonista, tutorial, stati di gioco e saluti UI.
- 119 occorrenze di `Stamina` uniformate in `Vigore`.
- 93 varianti `Holo-gizmo` e `Holo-gadget` uniformate in `Congegno Holo` o `Congegni Holo`.
- 70 descrizioni di combattimento e UI dinamica riscritte senza perdere valori o codici.
- 61 interventi editoriali ad alta confidenza su calchi, sintassi e naturalezza.
- 10 testi tronchi, ripetuti o sostituiti da segnaposto tecnici riparati.
- 197 possibili residui inglesi finali revisionati singolarmente: 59 corretti e 138 conservati.

## Decisioni terminologiche

- `Elite` resta senza accento, secondo la scelta editoriale del progetto.
- La statistica `Stamina` è resa sempre come `Vigore`.
- Il sistema `Holo-gizmo` è reso come `Congegno Holo`.
- `Fast and Furious`, `Gravity Pull` e `Starbound Journey` diventano rispettivamente `Furia Sfrenata`, `Attrazione Gravitazionale` e `Viaggio tra le Stelle`.
- `Matchmaking`, `stage`, `cutscene`, `quest`, `upgrade`, `drop` e `Skin` sono localizzati secondo il contesto.
- Prestiti ormai normali in italiano o tecnicismi informatici appropriati, fra cui `outfit`, `feedback`, `display`, `online`, `offline`, `reset`, `build`, `team`, `spawn` e `client`, restano soltanto dove la revisione riga per riga ne ha confermato l'uso.

## Controlli automatici finali

- zero tag o segnaposto alterati;
- zero flessioni artificiali come `secondo/i`, `volta/e`, `moneta/e` e simili;
- zero residui delle famiglie obbligatorie sopra elencate;
- zero overflow nelle 726 notifiche, 14 bolle Indizio e 32 intestazioni Indizio già mappate;
- 359 fallback significativi dello slot English ancora recuperati e 5 zeri tecnici conservati;
- 63 test automatici superati.

L'audit euristico resta volutamente conservativo: segnala anche frammenti dinamici, etichette tecniche e testi degli sviluppatori che non sono errori dimostrati. Le modifiche automatiche vengono applicate soltanto dopo revisione umana e sono protette da test di regressione.
