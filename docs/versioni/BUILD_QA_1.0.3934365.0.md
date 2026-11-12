# Quality Assurance & Verifica Tecnica — 1.0.3934365.0

- **Data di rilascio**: 2026-11-12
- **Build di gioco testata**: Steam `3934365`
- **Revisione Lua testata**: `aa93c4cd128e0b3fafb955fe526424ec`
- **Hash archivio XDF originale**: `f043cfe74521483e74a0be39c6d635356c4d0313cef3169c62a5ff69c12d7e06`
- **Dimensione XDT originale**: 3.127.994 byte
- **Stringa cache target**: `1.0.3934365,3127994,aa93c4cd128e0b3fafb955fe526424ec`

---

## 1. Conteggio chiavi e differenziale

- **Chiavi totali build 3934365**: 136.037
- **Chiavi totali build 3887621**: 134.298
- **Differenziale**:
  - Nuove chiavi aggiunte: 1.804
  - Chiavi aggiornate: 778
  - Chiavi obsolete rimosse: 65
- **Copertura traduzione italiana**: **136.037 / 136.037 (100,00%)**
- **Stringhe mancanti (fallback)**: **0**

---

## 2. Verifica integrità e tag

- **Rich Text Tags**: `<style=...>`, `<color=...>`, `<link=...>` verificati e perfettamente bilanciati.
- **Funzioni speciali**: `<customRichText(...)>` preservate integralmente con tutti i parametri originali.
- **Segnaposto variabili**: `{0}`, `{1}`, `%s`, `%d`, `{playerGender, select, ...}`, `#playerName#`, `#k...#z` verificati al 100%.
- **Sincronizzazione cache**: `LuaCacheVer.txt` allineato sia in `StreamingAssets\cvs\res\lua` che in `Aniimo_Data\cvs\res\lua`.

---

## 3. Esiti suite di test

- **Test unitari**: 161 test eseguiti, 161 superati, 0 falliti, 0 errori.
- **Verifica installazione reale**:
  - Modalità rilevamento: Steam standard.
  - Verifica archivio: 100% compatibile (testi italiani correnti).
  - Testi nuovi o modificati: 0 (compatibilità assoluta).
