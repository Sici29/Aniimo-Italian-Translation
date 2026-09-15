# Verifiche tecniche — 0.4.0 Preview

- Build installata letta: 3509129, sorgente English corrente identica al master.
- Master: 112.065 chiavi; 111.941 compilate, 124 fallback originali documentati.
- Ultimo lotto: 246 nuove traduzioni, riconciliazione esatta di chiavi, sorgenti, numeri, tag e spazi marginali.
- 84 test installer superati: 63 core, 15 rilevamento percorso, 6 profilo finale.
- Generazione XDF/XDT e decodifica del payload verificati.
- Installazione e ripristino provati su una copia isolata: 9 file ripristinati byte per byte.
- Gioco reale non modificato. Font e metadati runtime rimasti identici.
- EXE confezionato eseguito in modalità check: 112.065 chiavi, zero sorgenti sconosciute, compatibilità tecnica positiva.
- Anche l'EXE effettivamente consegnato è stato eseguito con install e restore su una copia isolata: entrambi terminati con codice 0, versione e percorso registrati correttamente, 9 file ripristinati byte per byte. Il profilo utente del test era interno all'area di lavoro; il gioco reale è rimasto invariato.
- EXE: 25.376.778 byte, icona italiana incorporata, firma digitale assente.
- SHA-256: C858198B087EBEBAEC70471DB200B9FD103FE877E073B56D3AF9B5D4F749106A.

## Limiti ancora aperti

La verifica grafica in gioco non è stata eseguita. La release rimane in bozza.
La revisione editoriale generale è rinviata su richiesta: restano 55 sorgenti ambigue (124 chiavi).
I test editoriali storici riguardano il corpus beta da 93.040 chiavi e sono esplicitamente esclusi dal nuovo profilo: il loro porting alla finale non è completato.
I controlli strutturali non certificano assenza di errori linguistici o troncamenti UI.

La build finale conserva i metadati workflow ufficiali, che hanno sostituito la vecchia lista numerica: non inventa stati di traduzione per il nuovo formato.
