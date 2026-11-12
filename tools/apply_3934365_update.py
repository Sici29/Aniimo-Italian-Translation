import csv
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH_DIR = ROOT / "tools" / "batches"
DATA_DIR = ROOT / "data"
GAME_DIR = Path(r"D:\SteamLibrary\steamapps\common\Aniimo")
STREAMING_LUA = GAME_DIR / "Aniimo_Data" / "StreamingAssets" / "cvs" / "res" / "lua"
CVS_LUA = GAME_DIR / "Aniimo_Data" / "cvs" / "res" / "lua"
XDF_PATH = STREAMING_LUA / "LuaScripts.xdf"
XDT_PATH = STREAMING_LUA / "LuaScripts.xdt"

EXPECTED_KEY_COUNT = 136037
TARGET_UPDATE = "3934365"
TARGET_REVISION = "aa93c4cd128e0b3fafb955fe526424ec"
TARGET_XDT_SIZE = 3127994
TARGET_XDF_SHA256 = "f043cfe74521483e74a0be39c6d635356c4d0313cef3169c62a5ff69c12d7e06"

def load_official_en() -> dict[str, str]:
    with zipfile.ZipFile(XDF_PATH, "r") as zf:
        mapping = json.loads(zf.read("xfs/luascripts/Data/I18N/NewTextMap_en.json").decode("utf-8-sig"))
        bin_data = zf.read("xfs/luascripts/Data/I18N/Compress_en.bin")

    official_en = {}
    for k, v in mapping.items():
        if not str(k).startswith("_") and isinstance(v, list) and len(v) == 2:
            off, length = int(v[0]), int(v[1])
            text = bin_data[off : off + length].decode("utf-8", errors="replace")
            official_en[str(k)] = text

    print(f"[+] Loaded {len(official_en)} official English strings from build {TARGET_UPDATE}.")
    assert len(official_en) == EXPECTED_KEY_COUNT, f"Expected {EXPECTED_KEY_COUNT} keys, got {len(official_en)}"
    return official_en

def assemble_translations() -> dict[str, str]:
    out_trans_path = ROOT / "tools" / "translations_3934365.json"
    if out_trans_path.is_file():
        data = json.loads(out_trans_path.read_text(encoding="utf-8"))
        if len(data) >= 2590:
            print(f"[+] Loaded {len(data)} cached translations from {out_trans_path.name}")
            return data

    # 1. Load batch translations
    batch_translations = {}
    for i in range(1, 11):
        out_file = BATCH_DIR / f"output_batch_{i}.json"
        if not out_file.is_file():
            raise FileNotFoundError(f"Missing batch output: {out_file}")
        data = json.loads(out_file.read_text(encoding="utf-8"))
        for tid, trans in data.items():
            batch_translations[int(tid)] = trans

    print(f"[+] Loaded {len(batch_translations)} translations from 10 batch outputs.")

    # 2. Map task IDs to keys using batch inputs
    task_id_to_keys = {}
    for i in range(1, 11):
        in_file = BATCH_DIR / f"input_batch_{i}.json"
        data = json.loads(in_file.read_text(encoding="utf-8"))
        for task in data:
            task_id_to_keys[int(task["id"])] = task["keys"]

    updated_translations = {}
    for tid, trans in batch_translations.items():
        keys = task_id_to_keys.get(tid, [])
        for k in keys:
            updated_translations[str(k)] = trans

    # 3. Load diff data for automated mappings
    with open(ROOT / "tools" / "diff_3934365_data.json", "r", encoding="utf-8") as f:
        diff_data = json.load(f)

    # Load old translation catalog
    old_csv_path = DATA_DIR / "translation_it.csv"
    with open(old_csv_path, "r", encoding="utf-8") as f:
        old_catalog = {row["key"]: row["it"] for row in csv.DictReader(f)}

    # Old EN -> IT mapping for exact matches among added keys
    import os
    old_xdf = Path(os.environ["LOCALAPPDATA"]) / "AniimoItalianTranslation" / "backups" / "20261106-175559" / "LuaScripts.xdf"
    with zipfile.ZipFile(old_xdf, "r") as zf:
        old_map = json.loads(zf.read("xfs/luascripts/Data/I18N/NewTextMap_en.json").decode("utf-8-sig"))
        old_bin = zf.read("xfs/luascripts/Data/I18N/Compress_en.bin")
    old_en_to_it = {}
    for k, v in old_map.items():
        if not str(k).startswith("_") and isinstance(v, list) and len(v) == 2:
            txt = old_bin[int(v[0]):int(v[0])+int(v[1])].decode("utf-8", errors="replace")
            if str(k) in old_catalog:
                old_en_to_it.setdefault(txt, old_catalog[str(k)])

    # Added keys with exact EN match
    added_exact = 0
    for k, info in diff_data["added"].items():
        if k not in updated_translations:
            en = info["en"]
            if en in old_en_to_it:
                updated_translations[k] = old_en_to_it[en]
                added_exact += 1
            else:
                raise ValueError(f"Added key {k} missing translation: {repr(en)}")

    print(f"[+] Mapped {added_exact} added keys via exact English match with existing catalog.")

    # Changed quote only keys
    quote_only_count = 0
    for k in diff_data["changed_quote_only"]:
        if k not in updated_translations:
            if k in old_catalog:
                updated_translations[k] = old_catalog[k]
                quote_only_count += 1
            else:
                raise ValueError(f"Quote-only key {k} missing in old catalog")

    print(f"[+] Preserved {quote_only_count} quote-normalization keys.")

    # Minor punctuation / case keys
    with open(ROOT / "tools" / "punct_changes_3934365.json", "r", encoding="utf-8") as f:
        punct_data = json.load(f)

    punct_count = 0
    for k, pinfo in punct_data.items():
        if k not in updated_translations:
            updated_translations[k] = pinfo["it"]
            punct_count += 1

    print(f"[+] Preserved {punct_count} minor punctuation/case keys.")

    # Targeted QA fixes for legacy catalog anomalies
    legacy_fixes = {
        "1205057391": "<style=Hint_BgL>Oggetto temporaneo. Utilizzabile solo in questa partita. Non può essere portato fuori durante l'estrazione.</style>\nUn chip Amplificatore d'Attacco con l'abilità Teletrasporto lampo. Conferisce il Teletrasporto lampo più veloce e con il tempo di ricarica minimo.",
        "1240363901": "#playerName#, sei in piedi? Come hai dormito?",
        "1258101983": "Ottimo,\nentriamo a dare un'occhiata!",
        "1263609918": "...Oh, già. A pensarci bene, non te l'ho mai detto, vero, #playerName#?\nNon ha votato per me perché credeva nelle mie invenzioni. Ha votato per me perché è <style=Hint_BgD>mia madre</style>.",
        "1378227929": "<style=Hint_BgL>Oggetto temporaneo. Utilizzabile solo in questa partita. Non può essere portato fuori durante l'estrazione.</style>\nUn chip Amplificatore d'Attacco con l'abilità Illuminazione. Aumenta la visibilità nei Santuari Perduti.",
        "1536180125": "Quando è attivo, colpire un bersaglio con un attacco attiverà automaticamente l'<style=Hint_BgD>Aggancio</style> se non sei già in modalità <style=Hint_BgD>Aggancio</style>. Mentre l'<style=Hint_BgD>Aggancio</style> è attivo, i tuoi attacchi prenderanno automaticamente di mira il nemico agganciato.",
        "1612270366": "Sì, è anche la nostra teoria. Se vogliamo riuscirci...\nprobabilmente ci servirà il Prisma Ancestrale trovato da #playerName#.",
        "1840263800": "Trascina il <style=Hint_BgL>cursore</style> per aumentare o ridurre lo zoom nella schermata di Gestione della Struttura.",
        "1845980274": "I membri della squadra infliggono il <customRichText(calcData,buff,4006011,param0,2,%d)>% di danni in più, con un ulteriore aumento del <customRichText(calcData,buff,4006011,param1,2,%d)>% contro gli elementi che contrastano.",
        "1943954362": "Sembra che avremo bisogno dell'aiuto di <color=#d89c28>un Aniimo che sa nuotare</color>. Cerca nei pressi del fiume.",
        "2054960036": "<style=Hint_BgL>Oggetto temporaneo. Utilizzabile solo in questa partita. Non può essere portato fuori durante l'estrazione.</style>\nUn chip Unità Protettiva che aumenta moderatamente la difesa, attenuando la violenza degli attacchi del bersaglio.",
        "2091551820": "L'Impeto Selvaggio è terminato. Raggiungi la Fioritura per rilasciare l'Energia Prismatica accumulata!"
    }
    for k, val in legacy_fixes.items():
        updated_translations[k] = val
    print(f"[+] Applied {len(legacy_fixes)} targeted QA fixes.")

    # Save compiled translations to tools/translations_3934365.json
    out_trans_path = ROOT / "tools" / "translations_3934365.json"
    with open(out_trans_path, "w", encoding="utf-8") as f:
        json.dump(updated_translations, f, ensure_ascii=False, indent=2)

    print(f"[+] Total updated_translations: {len(updated_translations)} saved to {out_trans_path.name}")
    return updated_translations

def validate_tags(en_text: str, it_text: str, key: str) -> list[str]:
    errors = []
    # Rich text tags
    en_styles = re.findall(r'<style=[^>]+>', en_text)
    it_styles = re.findall(r'<style=[^>]+>', it_text)
    if sorted(en_styles) != sorted(it_styles):
        errors.append(f"Style tags mismatch in key {key}: EN={en_styles} vs IT={it_styles}")

    en_links = re.findall(r'<link=[^>]+>', en_text)
    it_links = re.findall(r'<link=[^>]+>', it_text)
    if sorted(en_links) != sorted(it_links):
        errors.append(f"Link tags mismatch in key {key}: EN={en_links} vs IT={it_links}")

    en_colors = re.findall(r'<color=[^>]+>', en_text)
    it_colors = re.findall(r'<color=[^>]+>', it_text)
    if sorted(en_colors) != sorted(it_colors):
        errors.append(f"Color tags mismatch in key {key}: EN={en_colors} vs IT={it_colors}")

    en_custom = re.findall(r'<customRichText\([^>]*\)>', en_text)
    it_custom = re.findall(r'<customRichText\([^>]*\)>', it_text)
    if sorted(en_custom) != sorted(it_custom):
        errors.append(f"customRichText mismatch in key {key}: EN={en_custom} vs IT={it_custom}")

    # Format placeholders
    en_ph = re.findall(r'\{[0-9]+\}', en_text)
    it_ph = re.findall(r'\{[0-9]+\}', it_text)
    if sorted(en_ph) != sorted(it_ph):
        errors.append(f"Numeric placeholder mismatch in key {key}: EN={en_ph} vs IT={it_ph}")

    en_fmt = re.findall(r'%[0-9]*\.?[0-9]*[dfs]', en_text)
    it_fmt = re.findall(r'%[0-9]*\.?[0-9]*[dfs]', it_text)
    if sorted(en_fmt) != sorted(it_fmt):
        errors.append(f"Format specifier mismatch in key {key}: EN={en_fmt} vs IT={it_fmt}")

    # Color tokens #cRRGGBB...#z
    en_ctags = re.findall(r'#c[0-9a-fA-F]{6}', en_text)
    it_ctags = re.findall(r'#c[0-9a-fA-F]{6}', it_text)
    if sorted(en_ctags) != sorted(it_ctags):
        errors.append(f"Inline color tag mismatch in key {key}: EN={en_ctags} vs IT={it_ctags}")

    # Strip color markup before looking for parameter tokens like #playerName#
    clean_en = re.sub(r'#c[0-9a-fA-F]{6}.*?#z', '', en_text)
    clean_it = re.sub(r'#c[0-9a-fA-F]{6}.*?#z', '', it_text)

    en_tokens = re.findall(r'#[a-zA-Z0-9_]+#', clean_en)
    it_tokens = re.findall(r'#[a-zA-Z0-9_]+#', clean_it)
    if sorted(en_tokens) != sorted(it_tokens):
        errors.append(f"Token placeholder mismatch in key {key}: EN={en_tokens} vs IT={it_tokens}")

    return errors

def main():
    print("=" * 60)
    print(f" Aniimo Update {TARGET_UPDATE} Translation Merger & QA")
    print("=" * 60)

    official_en = load_official_en()
    updated_translations = assemble_translations()

    # Load existing translation catalog
    old_csv_path = DATA_DIR / "translation_it.csv"
    with open(old_csv_path, "r", encoding="utf-8") as f:
        old_catalog = {row["key"]: row["it"] for row in csv.DictReader(f)}

    new_catalog = []
    missing_keys = []
    all_tag_errors = []

    # Sort numerically by key ID
    sorted_keys = sorted(official_en.keys(), key=lambda x: int(x) if x.isdigit() else 0)

    for k in sorted_keys:
        en_text = official_en[k]
        sha = hashlib.sha256(en_text.encode("utf-8")).hexdigest()
        if k in updated_translations:
            it_text = updated_translations[k]
        elif k in old_catalog:
            it_text = old_catalog[k]
        else:
            missing_keys.append((k, en_text))
            continue

        errors = validate_tags(en_text, it_text, k)
        if errors:
            all_tag_errors.extend(errors)

        new_catalog.append({"key": k, "source_sha256": sha, "it": it_text})

    if missing_keys:
        print(f"[-] ERROR: {len(missing_keys)} missing keys! Sample:")
        for k, en in missing_keys[:10]:
            print(f"  [{k}] {repr(en)}")
        sys.exit(1)

    if all_tag_errors:
        print(f"[-] ERROR: {len(all_tag_errors)} tag errors found! Sample:")
        for err in all_tag_errors[:10]:
            print(f"  {err}")
        sys.exit(1)

    print(f"[+] All {len(new_catalog)} keys verified with 0 tag errors and 0 missing!")

    # Write data/translation_it.csv
    with open(old_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["key", "source_sha256", "it"])
        writer.writeheader()
        writer.writerows(new_catalog)

    print(f"[+] Successfully wrote {len(new_catalog)} rows to data/translation_it.csv")

    # Synchronize cvs\res\lua with StreamingAssets
    CVS_LUA.mkdir(parents=True, exist_ok=True)
    shutil.copy2(XDF_PATH, CVS_LUA / "LuaScripts.xdf")
    shutil.copy2(XDT_PATH, CVS_LUA / "LuaScripts.xdt")

    # Update LuaCacheVer.txt in both locations
    cache_ver_line = f"1.0.{TARGET_UPDATE},{TARGET_XDT_SIZE},{TARGET_REVISION}\n"
    (STREAMING_LUA / "LuaCacheVer.txt").write_text(cache_ver_line, encoding="utf-8")
    (CVS_LUA / "LuaCacheVer.txt").write_text(cache_ver_line, encoding="utf-8")
    print(f"[+] Synced game files and updated LuaCacheVer.txt to: {cache_ver_line.strip()}")

    # Calculate known_source_key_sha256 and known_source_content_sha256 using installer functions
    sys.path.insert(0, str(ROOT / "tools"))
    import aniimo_it_installer as installer

    key_manifest_sha = installer.sha256_keys(sorted_keys)
    content_manifest_sha = installer.sha256_keyed_text(official_en)

    # Update supported_versions.json
    sup_path = DATA_DIR / "supported_versions.json"
    with open(sup_path, "r", encoding="utf-8") as f:
        sup_data = json.load(f)

    sup_data["translation_version"] = f"1.0.{TARGET_UPDATE}.0"
    sup_data["known_source_key_count"] = len(new_catalog)
    sup_data["known_source_key_sha256"] = key_manifest_sha
    sup_data["known_source_content_sha256"] = content_manifest_sha

    if TARGET_UPDATE not in sup_data["supported_game_updates"]:
        sup_data["supported_game_updates"].insert(0, TARGET_UPDATE)
    sup_data["latest_supported_game_update"] = TARGET_UPDATE

    if TARGET_REVISION not in sup_data["supported_game_revisions"]:
        sup_data["supported_game_revisions"].insert(0, TARGET_REVISION)

    sup_data["tested_game_update"] = TARGET_UPDATE
    sup_data["tested_game_revision"] = TARGET_REVISION
    sup_data["tested_archive_sha256"] = TARGET_XDF_SHA256
    sup_data["tested_date"] = "2026-11-12"
    sup_data["coverage"] = f"{len(new_catalog)}/{len(new_catalog)} keys translated (100.00%)"

    sup_data["notes"] = [
        f"Aggiornamento per la build Steam {TARGET_UPDATE} (patch 1.0.{TARGET_UPDATE}.0) con copertura di traduzione al 100% ({len(new_catalog):,} chiavi).",
        "Traduzione completa della nuova serie di missioni di indagine e trama al Villaggio di Marespecchio (Chompy lo Squarrel, Reefish Sognatore, Marilla, Fannie).",
        "Aggiunta e rifinitura delle nuove opzioni estetiche personalizzate del viso, voci del camper e aggiornamento abilità ed equipaggiamenti.",
        "Normalizzazione tipografica completa con allineamento delle virgolette dritte nei registri, note di ricerca e dialoghi.",
        "Preservazione assoluta di tutti i tag di formattazione nativi, codici colore, placeholder di genere e formattazione rich text.",
        "Compatibilità garantita con Steam e verifica automatica della cache LuaCacheVer.txt."
    ]

    with open(sup_path, "w", encoding="utf-8") as f:
        json.dump(sup_data, f, ensure_ascii=False, indent=2)

    print(f"[+] Updated data/supported_versions.json for {TARGET_UPDATE}.")

if __name__ == "__main__":
    main()
