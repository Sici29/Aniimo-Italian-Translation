# Aniimo — Traduzione italiana v0.3.12 beta

Questa release rende finalmente esplicita la differenza fra traduzione presente e traduzione realmente aggiornata.

## Nuovo controllo della traduzione installata

L'installer mostra ora tre informazioni separate:

- `Versione trad. installata`: la versione registrata durante l'ultima installazione;
- `Versione trad. proposta`: la versione contenuta nell'installer aperto;
- `Confronto contenuti`: verifica diretta di tutti i 92.954 testi installati.

Una traduzione precedente, per esempio la v0.3.8 aperta con l'installer v0.3.12, viene segnalata come `DIVERSI — AGGIORNAMENTO CONSIGLIATO`.

Se invece cambia soltanto l'installer e la traduzione installata è già identica, compare `IDENTICI — nessun aggiornamento necessario`: non occorre reinstallarla.

Le installazioni più vecchie prive di una versione registrata restano verificabili attraverso il confronto dei contenuti.

## Punteggiatura italiana

Revisionate tutte le battute che contenevano un trattino lungo. Le 190 frasi che terminavano con `—`, come `un mondo pieno di colori—`, usano ora i punti di sospensione italiani: `un mondo pieno di colori...`.

I trattini lunghi interni restano soltanto quando esprimono davvero un inciso o un'interruzione all'interno della frase.

## Revisione editoriale completa

Tutte le 92.954 righe sono state sottoposte a una nuova revisione mirata alla naturalezza dell'italiano. La prima passata ha applicato 175 correzioni uniche ad alta confidenza:

- 106 calchi, falsi amici o referenti artificiali;
- 65 rifiniture di dialoghi, descrizioni e testi UI;
- 4 incoerenze nei tempi verbali.

La frase relativa a Snowy è stata corretta in tutte le varianti: l'Aniimo viene portata nel proprio Aniipod, non riceve un “passaggio” come se l'Aniipod fosse un veicolo.

La revisione è stata poi ripetuta in tre blocchi indipendenti, leggendo 42.637 testi sorgente unici che coprono tutte le 92.954 righe. Delle 426 nuove proposte, 423 sono state approvate e 3 respinte durante la verifica editoriale finale.

Un ultimo controllo residuale ha aggiunto 443 interventi su interiezioni, onomatopee, residui inglesi, famiglie UI, duplicati divergenti, date e spaziature. La v0.3.12 comprende quindi 1.041 interventi editoriali su 1.038 chiavi uniche, oltre alle 190 normalizzazioni di punteggiatura.

Sono state localizzate 297 interiezioni e onomatopee inglesi; restano invariati soltanto nomi ufficiali come `Master Woof` e `Little Lightning Chirp` e vocalizzi senza una resa italiana univoca. Tutte le 22 stringhe che mostravano `AM` pur usando già un orario a 24 ore sono state italianizzate.

## Data dinamica italiana

La data della schermata capitolo non era una normale stringa, ma veniva generata dallo script di gioco. L'installer verificato la riordina ora automaticamente da `AAAA/MM/GG` a `GG/MM/AAAA`, per esempio `12/07/2026`.

La modifica viene applicata solo se il bytecode corrisponde esattamente alla struttura supportata ed è coperta dal normale backup e ripristino.

## Verifica tecnica

- 73 test automatici superati.
- Confronto esatto protetto da test di regressione.
- Copertura della traduzione invariata: 92.954/92.954 stringhe.
- Patch della data verificata sulla copia reale: 1 sequenza attesa sostituita, 0 sequenze residue nel vecchio ordine.
- Distribuzione in un unico file `Aniimo-Italian-Translation.exe`.

SHA-256: `6B6EED2D4AAFE8360284185CE7A1055DF7A774F68D2F37CE62F9A980137863CA`
