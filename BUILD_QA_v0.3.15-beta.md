# Build QA — v0.3.15 beta

Data: 13 luglio 2026

## Compatibilità Aniimo

- Build verificata: `3048640`.
- Installazione reale: `F:\Pawprint\Aniimo\game`.
- Chiavi ufficiali: `92984`.
- Fingerprint chiavi: `51b0b48cfee2ff71b790226cc158a68e775a880b4a67ad58b3ee3354b4ba09b5`.
- Archivi Lua rilevati e ricostruiti separatamente: 2.
- Overlay Lua installato SHA-256: `2DA1AF961188A7200F7308E23613DFAE87C50B4FB25A2D6C0C614A4C2E3C3490`.
- Archivio Lua base installato SHA-256: `D42041D7C2C4660F36BBD13DDEDACBC172D54069F295AB599F2321CE60831DF9`.

## Correzioni italiane

- Etichette `Free` corrette: 8 / 8, rese con `<size=-6>Gratis</size>` nelle card strette.
- Dialogo Jilly corretto: `Sono impressionata`.
- Date dinamiche visibili verificate in `GG/MM/AAAA`: capitoli, missioni `Astra Era`, posta, album, foto, registro attività ed eventi.
- Timer card negozio verificato con unità `h/m/s`; pattern CJK assente.
- Metadati runtime patchati SHA-256: `DFD6B764978664474F73211634BE9C9F21595057C2BBCA1FDD5CA4E5962000A5`.
- Dimensione metadati invariata: `23378280` byte.

## Test automatici

- Suite completa: 93 test superati.
- Test installer: 55 superati.
- Test dati traduzione: 38 superati.
- Copertura: 92.984 / 92.984 testi, 0 fallback.
- Verifiche aggiunte: pattern data univoci e idempotenti, timer a lunghezza invariata, doppio archivio, alias manifest, backup multiplo, ripristino legacy e moderno.

## Generazione e installazione reali

- Patch generata dagli archivi reali della build 3048640.
- Testi ricostruiti: 92.984.
- Traduzioni corrispondenti all'installer: 92.984 / 92.984.
- Font accentato `English -> UI_Font_Vietnamese`: verificato.
- Date italiane su entrambi gli archivi: verificate.
- Timer italiano nei metadati live: verificato.
- Backup reale: `20260713-235355`, con hash SHA-256 per due coppie Lua e metadati runtime.
- Stato installato: `installed=true`, `matches_current=true`, `date_italian=true`, `countdown_italian=true`.

## Installer finale

- File: `Aniimo-Italian-Translation.exe`.
- Dimensione: `34171559` byte.
- SHA-256: `C5996FA85E7A647C94987C666F3623181EEEFCF1D9E00B161316B5B170D6ACE6`.
- Avvio, `--help` e controllo compatibilità sulla build reale: superati.
- Unico artefatto destinato alla release: confermato.
