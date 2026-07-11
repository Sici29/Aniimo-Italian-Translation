# Audit completo delle lingue di Aniimo

Audit eseguito l'11 luglio 2026 sulle risorse ufficiali della versione gioco `3036569`, revisione `7113f88e39827a2d13591a55b395f1c6`.

## Lingua d'origine

Pawprint Studio si presenta ufficialmente come studio di sviluppo e pubblicazione con base a Singapore. La struttura delle risorse indica però che il testo sorgente di Aniimo è quasi certamente il **cinese semplificato**:

- le mappe cinese semplificato e tradizionale contengono il testo completo per 359 chiavi che nello slot English valgono soltanto `0`;
- giapponese, coreano e russo moderni contengono le stesse 359 voci, quindi sono localizzazioni complete dello stesso contenuto;
- English e vietnamita condividono invece tutti i 364 zeri, segno che quel ramo della pipeline non ha ricevuto quelle stringhe;
- Steam indica audio completo soltanto per English e cinese semplificato, mentre giapponese, cinese tradizionale e coreano hanno interfaccia e sottotitoli.

Fonti pubbliche: [Pawprint Studio](https://pawprintstudio.com/), [annuncio ufficiale FunPlus](https://funplus.com/aniimo-revealed-at-xbox-games-showcase/), [comunicato ufficiale Pawprint per il Giappone](https://prtimes.jp/main/html/rd/p/000000002.000183238.html), [pagina Steam di Aniimo](https://store.steampowered.com/app/4126040/Aniimo/).

## Confronto delle mappe moderne

| Lingua | Chiavi | Testi significativi | Valori `0` | Campi vuoti |
|---|---:|---:|---:|---:|
| English | 92.954 | 92.590 | 364 | 0 |
| Cinese semplificato | 92.952 | 92.945 | 5 | 2 |
| Cinese tradizionale | 92.954 | 92.949 | 5 | 0 |
| Giapponese (`ja_JP`) | 92.954 | 92.949 | 5 | 0 |
| Coreano (`ko_KR`) | 92.954 | 92.949 | 5 | 0 |
| Russo | 92.954 | 92.949 | 5 | 0 |
| Vietnamita | 92.954 | 92.590 | 364 | 0 |
| Italiano v0.3.5 | **92.954** | **92.949** | **5** | **0** |

Le mappe moderne English, cinese tradizionale, giapponese, coreano, russo, vietnamita e italiano condividono esattamente lo stesso insieme di chiavi:

```text
SHA-256 chiavi: 96be065e856b547226ea93cd7ce33d7671214a45c16783362a58da5bf9de6617
```

Il cinese semplificato ha quattro chiavi in meno rispetto al set moderno e due chiavi aggiuntive, entrambe vuote. Le quattro voci mancanti sono presenti nelle altre mappe e nella traduzione italiana; le due voci aggiuntive non contengono testo da tradurre.

## Correzione dei fallback

Lo slot English ufficiale contiene 364 chiavi con valore `0`:

- **359** hanno contenuto reale nelle altre lingue ufficiali e sono ora tradotte in italiano;
- **5** valgono `0` anche in cinese, giapponese, coreano e russo e sono quindi valori tecnici reali.

Questo difetto spiegava le frasi inglesi mostrate in gioco nonostante la copertura nominale completa. Quando Aniimo incontrava `0`, usava un testo inglese incorporato nel dialogo come fallback.

Tra le voci recuperate ci sono le tre scelte sui solventi e la sequenza in cui l'Istruttore racconta gli avvenimenti confrontandoli con il sogno.

## Esito

La v0.3.5 copre il **100% delle 92.954 chiavi testuali moderne** usate dallo slot English, non contiene campi vuoti e gestisce tutte le 359 voci di fallback significative note. I soli cinque zeri rimasti sono tecnici e confermati da tutte le localizzazioni complete.

Questo audit certifica il pacchetto di localizzazione della revisione indicata. Futuri hot update o testi incorporati in nuovi filmati devono essere verificati nuovamente quando il gioco cambia revisione.
