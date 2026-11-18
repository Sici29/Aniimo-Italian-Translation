# Quality Assurance & Verifica Tecnica — 1.0.3973445.0

- **Data di rilascio**: 2026-11-18
- **Build di gioco testata**: Steam `3973445`
- **Revisione Lua testata**: `680016f12fe1cfcaffb3c142e27abfdb`
- **Hash archivio XDF originale**: `09642fd222f371965835967c2c2f1df5695b1b99dc8f7e6f04f17f3fa4ee35c5`
- **Dimensione XDT originale**: 3.127.994 byte
- **Stringa cache target**: `1.0.3973445,3127994,680016f12fe1cfcaffb3c142e27abfdb`

---

## 1. Conteggio chiavi e differenziale

- **Chiavi totali build 3973445**: 136.024
- **Chiavi totali build 3934365**: 136.037
- **Differenziale**:
  - Nuove chiavi aggiunte: 3
  - Chiavi aggiornate: 19
  - Chiavi obsolete rimosse: 16
- **Copertura traduzione italiana**: **136.024 / 136.024 (100,00%)**
- **Stringhe mancanti (fallback)**: **0**

---

## 2. Verifica integrità e tag

- **Rich Text Tags**: `<style=...>`, `<color=...>`, `<link=...>`, `<timeAutoChangeServer>` verificati e perfettamente bilanciati.
- **Funzioni speciali**: `<customRichText(...)>` preservate integralmente con tutti i parametri originali.
- **Segnaposto variabili**: `{0}`, `{1}`, `%s`, `%d`, `{playerGender, select, ...}`, `#playerName#`, `#k...#z`, `#c...#z` verificati al 100%.
- **Sincronizzazione cache**: `LuaCacheVer.txt` allineato sia in `StreamingAssets\cvs\res\lua` che in `Aniimo_Data\cvs\res\lua`.

---

## 3. Esiti suite di test

- **Test unitari**: 161 test eseguiti, 161 superati, 0 falliti, 0 errori.
- **Verifica installazione reale**:
  - Modalità rilevamento: Steam standard.
  - Verifica archivio: 100% compatibile (testi italiani correnti).
  - Testi nuovi o modificati: 0 (compatibilità assoluta).
