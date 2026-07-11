# Changelog

## 0.3.2 Beta - 2026-07-11

- Aggiunta la revisione dell'hot update separata dal numero principale del gioco.
- La compatibilità viene mostrata separatamente ed è determinata dalle chiavi reali dei testi.
- Registrata e verificata la nuova revisione `7113f88e39827a2d13591a55b395f1c6`, ancora compatibile con tutte le 92.954 chiavi note.
- La revisione ufficiale viene conservata prima della patch, evitando che l'hash generato dall'installazione venga scambiato per un nuovo hot update.
- Aggiunti GitHub visibile nel pannello e menu `5` con crediti, segnalazioni e sostegno al progetto.
- Confermato che l'ultimo aggiornamento del gioco rimuove la traduzione ma non richiede modifiche ai testi italiani.
- Dopo un aggiornamento automatico, il nuovo installer mostra una conferma verde e si riavvia direttamente nel menu.

## 0.3.1 Beta - 2026-07-11

- Il pannello indica se il percorso di Aniimo è stato trovato automaticamente o recuperato da quello salvato.
- Il pannello rileva dalle risorse reali se la traduzione italiana è già installata.
- Se Aniimo non viene trovato, l'installer permette di scegliere la cartella con la finestra di Windows oppure di incollare il percorso.
- Aggiunte istruzioni immediate per riconoscere la cartella corretta contenente `Aniimo_Data`.
- Il percorso verificato viene salvato e può essere modificato in qualsiasi momento con la nuova opzione `4`.
- Estesi i controlli automatici per rilevamento traduzione, percorso salvato e pannello di stato.

## 0.3.0 Beta - 2026-07-11

- Aggiunto l'aggiornamento automatico direttamente da GitHub Releases.
- Il nuovo EXE viene accettato soltanto dopo la verifica di dimensione e hash SHA-256.
- Aggiunta la sostituzione sicura dell'installer in uso con riavvio automatico su Windows.
- Nuovo pannello iniziale con versione gioco supportata e rilevata, compatibilità colorata, versione installer attuale e nuova versione disponibile.
- Aggiunto il rilevamento reale della versione di Aniimo tramite `verlist.txt`.
- Corretta la versione gioco verificata da `3036569` a `3032670`, riscontrata nell'installazione e nel backup originali.
- Estesi i test automatici dell'installer da 5 a 12, includendo download alterati, confronto versioni e sostituzione dell'EXE.

## 0.2.1 Beta - 2026-07-11

- Seconda revisione completa dedicata alla naturalezza dell'italiano.
- Integrati 2.788 interventi aggiuntivi su dialoghi, narrativa, UI, missioni, calchi e residui inglesi.
- Uniformate tutte le descrizioni duplicate dei forzieri misteriosi e le famiglie terminologiche collegate.
- Migliorati concordanze, reggenze, neutralità di genere, ritmo dei dialoghi e messaggi UI.
- Semplificato il README con installazione in quattro passaggi e sostegno al progetto ben visibile.
- Reso più chiaro il menu dell'installer; le scelte non valide non avviano più l'installazione.
- Rigenerati e validati il master accentato e la variante compatibile con lo slot `English`.

## 0.2.0 Beta - 2026-07-11

- Revisione professionale completa di tutte le 92.954 stringhe note.
- Integrati 695 interventi editoriali e tecnici su dialoghi, terminologia, generi, UI, tag e spaziature.
- Aggiunto il master parallelo con accenti italiani reali, già pronto per un futuro font compatibile.
- Rigenerata la variante pubblica per lo slot `English`, con apostrofi e punteggiatura compatibile.
- Rafforzati backup e ripristino: vengono rimossi soltanto i file creati dalla patch.
- Aggiunti controlli sull'header delle risorse e sincronizzazione della versione MAP/BIN.
- Distribuzione semplificata in un unico file `Aniimo-Italian-Translation.exe` autonomo.

## 0.1.0 Beta

- Prima versione pubblicabile della traduzione italiana.
- Copertura completa delle 92.954 stringhe note della versione testata.
- Installer con backup automatico.
- Controllo versione/stringhe per ridurre il rischio dopo gli aggiornamenti del gioco.
- Installazione consigliata sullo slot `English`.
