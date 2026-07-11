# Aniimo — Traduzione italiana v0.3.4 Beta

Questa release introduce gli accenti italiani completi, corregge i testi segnalati in gioco e completa la correzione del riavvio automatico su Windows.

## Accenti italiani reali nello slot English

- Individuato nel gioco il font vietnamita già incluso, completo di `à è é ì ò ù` e relative maiuscole.
- Lo slot **English** continua a caricare i testi italiani, ma ora usa automaticamente il font vietnamita incluso in Aniimo.
- La traduzione usa `qualità`, `perché`, `può`, `già` e `più` senza parole troncate.
- Nessuna lingua visibile viene rimossa o sostituita: cinese tradizionale, cinese semplificato, giapponese e coreano restano invariati.
- Il collegamento English → font vietnamita è stato verificato direttamente in gioco.
- Rilevamento corretto dell'hot update **3036569**, distinto dalla vecchia versione base **3032670**.

## Revisione dei testi

- Conservati integralmente i termini ufficiali `Timothée`, `Déjà Vu`, `Molière`, `Café` e `Português`.
- Corretti i residui inglesi `Move Plot`, `New World`, `Roar of the Bouldus`, i titoli delle missioni segnalati e `[Song of Ice and Fire]`.
- Accorciate e differenziate varie etichette `Form` soggette a troncamento, tra cui `Forma Nebbiosa`, `Forma Boschiva`, `Forma Fangosa`, `Forma Piovosa`, `Forma Tonante` e `Forma d'Altura`.
- Confermate **92.954 / 92.954** stringhe coperte.

## Finestra visibile dopo l'aggiornamento

L'assistente che sostituisce l'EXE lavora intenzionalmente in background. Nella versione precedente, il nuovo installer poteva ereditare la stessa modalità senza finestra: il menu rimaneva attivo ma invisibile e il controllo della singola istanza lo considerava ancora aperto.

La `v0.3.4-beta` avvia sempre il nuovo installer in una console Windows visibile e indipendente. Al termine compaiono quindi regolarmente:

- conferma verde di aggiornamento completato;
- versione precedente e versione attuale;
- pannello con stato gioco e traduzione;
- crediti e link GitHub;
- menu interattivo.

La release contiene un solo file: `Aniimo-Italian-Translation.exe`.
