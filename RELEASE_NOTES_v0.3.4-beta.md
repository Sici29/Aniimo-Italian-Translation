# Aniimo — Traduzione italiana v0.3.4 Beta

Questa release completa la correzione del riavvio automatico su Windows.

## Finestra visibile dopo l'aggiornamento

L'assistente che sostituisce l'EXE lavora intenzionalmente in background. Nella versione precedente, il nuovo installer poteva ereditare la stessa modalità senza finestra: il menu rimaneva attivo ma invisibile e il controllo della singola istanza lo considerava ancora aperto.

La `v0.3.4-beta` avvia sempre il nuovo installer in una console Windows visibile e indipendente. Al termine compaiono quindi regolarmente:

- conferma verde di aggiornamento completato;
- versione precedente e versione attuale;
- pannello con stato gioco e traduzione;
- crediti e link GitHub;
- menu interattivo.

La release contiene un solo file: `Aniimo-Italian-Translation.exe`.
