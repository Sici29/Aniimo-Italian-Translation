# Aniimo — Traduzione italiana v0.3.3 Beta

Questa release corregge un conflitto Windows osservato durante l'aggiornamento automatico.

## Correzione aggiornamento

In presenza di più finestre dell'installer, il vecchio EXE poteva rimanere bloccato. Il nuovo file veniva quindi avviato dalla cache e un secondo tentativo restituiva `WinError 5 - Accesso negato`.

La nuova versione:

- impedisce di aprire contemporaneamente più finestre interattive;
- usa un file di download univoco per ogni tentativo;
- mostra un avviso visibile se un'altra finestra sta bloccando la sostituzione;
- permette di chiudere le altre finestre e premere **Riprova**;
- non avvia più dalla cache un EXE che non è riuscito a sostituire quello vecchio;
- lascia sempre intatto il vecchio installer in caso di errore.
- pulisce automaticamente i vecchi download dell'installer rimasti nella cache.

## Installazione

La release contiene un solo file: `Aniimo-Italian-Translation.exe`.

La traduzione resta compatibile con Aniimo `3032670`, revisione `7113f88e39827a2d13591a55b395f1c6`, per tutte le 92.954 chiavi note.
