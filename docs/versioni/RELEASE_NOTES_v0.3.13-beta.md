# Aniimo — Traduzione italiana v0.3.13 beta

Questa release corregge i residui emersi durante la verifica diretta in gioco e rende più rigorosi i controlli dell'installer.

## Dialoghi e trattini lunghi

La battuta segnalata viene ora visualizzata come:

```text
Io voglio...
Oh, Snowy, vieni qui!
```

È stata corretta anche la frase dell'Ombra di Velouria:

```text
Vi serve una mano con il trasloco?
Con le nostre ali sarà tutto molto più facile.
```

Il controllo dei trattini non si limita più alla fine dell'intera stringa: sono state esaminate tutte le 226 righe contenenti `—` o `–`, anche prima di un ritorno a capo. Altre 65 pause o interruzioni di dialogo sono state convertite in `...`; separatori grafici, intervalli, onomatopee e usi intenzionali restano invariati.

## Toponimi coerenti

I nomi ufficiali di aree e luoghi restano in inglese in tutta la traduzione, mentre articoli, preposizioni e testo circostante rimangono italiani.

Sono stati inventariati 42 toponimi canonici e corrette 176 stringhe. Fra le incongruenze eliminate:

- `Stretto Argentato` → `Argent Strait`;
- `Costa Tideblossom` → `Tideblossom Coast`;
- `Ponte Terrestre Zephyrus` → `Zephyrus Landbridge`;
- `Sala dei ricordi di Astra` → `Astra Hall of Memories`.

La regola è stata applicata anche nei dialoghi, nelle missioni e nelle descrizioni, adattando in modo naturale le preposizioni italiane.

## Date italiane in capitoli, mail e interfaccia

La v0.3.12 correggeva la data della schermata capitolo, ma il gioco usa un secondo formattatore per mail e altre schermate. Per questo una mail del 12 luglio poteva ancora apparire come `07/12/2026`.

La v0.3.13 modifica e verifica entrambi i formattatori:

- capitoli: `AAAA/MM/GG` → `GG/MM/AAAA`;
- mail e UI condivisa: `MM/GG/AAAA` → `GG/MM/AAAA`.

L'installer mostra `✓ ITALIANO (GG/MM/AAAA)` soltanto quando entrambe le modifiche sono presenti. Un'installazione parziale viene ora indicata correttamente come `⚠ DA AGGIORNARE`.

## Verifica tecnica

- 77 test automatici superati.
- Patch generata dalla copia reale del gioco per la revisione `4eb81a98d0e3934af67064cbde06218e`.
- 92.954/92.954 testi ricostruiti e identici al master.
- Zero fallback e zero differenze.
- Entrambi gli script delle date riconosciuti e verificati nel formato italiano.
- Distribuzione in un unico file `Aniimo-Italian-Translation.exe`.

SHA-256: `35ED88178D701E9C8D5ABCCAA7902C6E2FF28CE76773A2AE612EC3A25F10F35E`
