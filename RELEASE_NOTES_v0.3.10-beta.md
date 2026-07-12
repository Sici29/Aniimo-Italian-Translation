# Aniimo — Traduzione italiana v0.3.10 beta

Questa release chiude l'audit esteso delle concordanze di genere usando l'attribuzione reale delle battute contenuta nei dati runtime del gioco.

## Correzioni principali

- Corretta Sunia in tutte le battute confermate: `nata`, `piccola`, `passata`, `entrata`, `svegliata`, `arresa`, `sicura`, `cieca`, `decisa`, `fatta` e `ripresa`.
- Corretti anche Nicole, Fannie, Awen, Irelia, Lunara, Caitlin, Velouria, Baboni, Senior Cecelia, Senior Loulla, Fantine, Lana e altri personaggi femminili.
- Corretti i riferimenti a Avetine, Cress, Haidt, Snowy, Awen, Baboni e alla giovane Iris.
- Ripristinato il maschile corretto per Aeolus e Sorora.
- Riscritte in forma italiana naturale e neutra le battute del protagonista selezionabile e le frasi rivolte al protagonista: niente più maschili fissi come `sono pronto`, `benvenuto` o `ti sei fatto male` nelle chiavi prive di variante femminile.

## Verifica tecnica

- 7.672 battute attribuite al rispettivo parlante tramite `pmdata.bin`.
- 290 etichette di parlante controllate.
- 550 candidati grammaticali revisionati.
- 158 stringhe corrette e registrate per chiave.
- 59 test automatici superati.
- Installazione e ripristino verificati su una copia isolata del gioco.
- Tutte le 92.954 stringhe dell'archivio installato confrontate con il master.

L'installer continua a distribuire tutto in un unico file:

```text
Aniimo-Italian-Translation.exe
```

SHA-256: `A2A0719E82A767956FDBB482063BF7E81C2922F49D93895854EA93826284CB80`
