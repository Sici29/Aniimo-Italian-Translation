# Aniimo — Traduzione italiana v0.3.5 Beta

Questa release elimina una classe di testi inglesi che il precedente controllo di copertura non poteva riconoscere.

## Corretto il fallback inglese nascosto

La localizzazione English ufficiale contiene 364 chiavi con il solo valore `0`. Per 359 di queste, le altre lingue ufficiali contengono invece dialoghi, tutorial, descrizioni e scelte complete. In gioco, Aniimo sostituiva lo zero con un testo inglese incorporato a runtime: per questo alcune frasi restavano in inglese anche se la tabella risultava coperta al 100%.

La v0.3.5 recupera e traduce tutte le 359 voci significative. Restano invariati soltanto 5 zeri tecnici, confermati come tali in tutte le localizzazioni ufficiali.

Tra le correzioni confermate:

- `Use oils as a solvent.` → `Usa oli come solvente.`
- `Use ethanol as a solvent.` → `Usa etanolo come solvente.`
- `Use pure water as a solvent.` → `Usa acqua pura come solvente.`
- tradotta la sequenza in cui l'Istruttore racconta gli avvenimenti e conferma che coincidono con il sogno;
- ripulite 220 stringhe inglesi o miste con interventi mirati;
- uniformate altre 651 stringhe secondo glossario e coerenza interna, compresi `Principal` → `Preside`, nomi di luoghi, termini di combattimento, etichette brevi e testi provvisori degli sviluppatori.

## Controlli più severi

La copertura **92.954 / 92.954** ora indica sia la presenza delle chiavi sia la gestione delle voci di fallback note. I test verificano inoltre le due copie della traduzione, gli accenti, le correzioni segnalate e l'assenza dei residui inglesi confermati.

La release contiene un solo file: `Aniimo-Italian-Translation.exe`.
