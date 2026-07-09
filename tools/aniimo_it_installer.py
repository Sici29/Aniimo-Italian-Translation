#!/usr/bin/env python3
"""Public installer for Aniimo Italian Translation.

The installer builds a local patch from the user's own game files. It does not
ship original Aniimo archives.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


LUA_RELS = [
    Path(r"Aniimo_Data\cvs\res\lua"),
    Path(r"Aniimo_Data\StreamingAssets\cvs\res\lua"),
    Path(r"worldx_Data\StreamingAssets\cvs\res\lua"),
]
XDF_NAME = "LuaScripts.xdf"
XDT_NAME = "LuaScripts.xdt"
TEXT_MAP = "xfs/luascripts/Data/I18N/NewTextMap_{lang}.json"
COMPRESS = "xfs/luascripts/Data/I18N/Compress_{lang}.bin"
if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent
    BUNDLE_DIR = Path(getattr(sys, "_MEIPASS", APP_DIR))
else:
    APP_DIR = Path(__file__).resolve().parents[1]
    BUNDLE_DIR = APP_DIR

DATA_DIR = BUNDLE_DIR / "data"
USER_WORK_DIR = Path.home() / "Documents" / "AniimoItalianTranslation"


@dataclass(frozen=True)
class GamePaths:
    game_dir: Path
    lua_dir: Path
    xdf: Path
    xdt: Path


def md5_bytes(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def md5_file(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_keys(keys: list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(keys)).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def local_manifest() -> dict:
    return read_json(DATA_DIR / "supported_versions.json")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def looks_like_game_dir(path: Path) -> bool:
    return (path / "Aniimo_Data").exists() or any((path / rel / XDF_NAME).exists() for rel in LUA_RELS)


def load_translations() -> dict[str, str]:
    csv_path = DATA_DIR / "translation_it.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing translation file: {csv_path}")
    translations: dict[str, str] = {}
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            key = (row.get("key") or "").strip()
            text = row.get("it") or ""
            if key and text:
                translations[key] = text
    return translations


def parse_steam_libraries() -> list[Path]:
    libraries: list[Path] = []
    if os.name != "nt":
        return libraries
    try:
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            (
                "$paths=@(); "
                "foreach($k in 'HKLM:\\SOFTWARE\\WOW6432Node\\Valve\\Steam','HKCU:\\SOFTWARE\\Valve\\Steam'){"
                "try{$p=(Get-ItemProperty $k -ErrorAction Stop).InstallPath; if($p){$paths+=$p}}catch{}}; "
                "$paths -join [Environment]::NewLine"
            ),
        ]
        output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    except Exception:
        output = ""
    for line in output.splitlines():
        steam = Path(line.strip())
        if not steam.exists():
            continue
        libraries.append(steam)
        vdf = steam / "steamapps" / "libraryfolders.vdf"
        if vdf.exists():
            text = vdf.read_text(encoding="utf-8", errors="ignore")
            for match in re.finditer(r'"path"\s+"([^"\\]*(?:\\.[^"\\]*)*)"', text):
                raw = match.group(1).replace("\\\\", "\\")
                p = Path(raw)
                if p.exists():
                    libraries.append(p)
    return list(dict.fromkeys(libraries))


def candidate_game_dirs() -> list[Path]:
    candidates: list[Path] = []
    env = os.environ.get("ANIIMO_GAME_DIR")
    if env:
        candidates.append(Path(env))

    # Best user experience: extract the release into the game root and run it.
    candidates.extend([APP_DIR, APP_DIR.parent, Path.cwd(), Path.cwd().parent])

    for drive in [f"{letter}:\\" for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ"]:
        root = Path(drive)
        if not root.exists():
            continue
        candidates.extend(
            [
                root / "Pawprint" / "Aniimo" / "game",
                root / "Pawprint" / "Aniimo",
                root / "Aniimo" / "game",
                root / "Aniimo",
            ]
        )
    for lib in parse_steam_libraries():
        candidates.extend(
            [
                lib / "steamapps" / "common" / "Aniimo" / "game",
                lib / "steamapps" / "common" / "Aniimo",
            ]
        )
    return list(dict.fromkeys(candidates))


def resolve_game_dir(raw: str | None) -> Path:
    if raw:
        p = Path(raw).expanduser().resolve()
        if looks_like_game_dir(p):
            return p
        if looks_like_game_dir(p / "game"):
            return p / "game"
        raise FileNotFoundError(f"Invalid Aniimo folder: {p}")
    for candidate in candidate_game_dirs():
        if looks_like_game_dir(candidate):
            return candidate.resolve()
    raise FileNotFoundError(
        "Cartella di Aniimo non trovata. Metti questo eseguibile nella root del gioco, "
        "accanto ad Aniimo_Data, oppure avvialo con --game-dir \"PERCORSO\\game\"."
    )


def resolve_paths(game_dir: Path) -> GamePaths:
    candidates: list[tuple[float, Path, Path, Path]] = []
    for rel in LUA_RELS:
        lua_dir = game_dir / rel
        xdf = lua_dir / XDF_NAME
        xdt = lua_dir / XDT_NAME
        if xdf.exists() and xdt.exists():
            candidates.append((max(xdf.stat().st_mtime, xdt.stat().st_mtime), lua_dir, xdf, xdt))
    if not candidates:
        checked = "\n".join(str(game_dir / rel) for rel in LUA_RELS)
        raise FileNotFoundError(f"Non trovo {XDF_NAME}/{XDT_NAME}. Percorsi controllati:\n{checked}")
    _, lua_dir, xdf, xdt = max(candidates, key=lambda item: item[0])
    return GamePaths(game_dir, lua_dir, xdf, xdt)


def decode_map(map_data: bytes, bin_data: bytes) -> tuple[dict, list[dict], bytes]:
    mapping = json.loads(map_data.decode("utf-8-sig"))
    records: list[dict] = []
    min_offset: int | None = None
    for key, value in mapping.items():
        if str(key).startswith("_") or not isinstance(value, list) or len(value) != 2:
            continue
        offset, length = int(value[0]), int(value[1])
        min_offset = offset if min_offset is None else min(min_offset, offset)
        text = bin_data[offset : offset + length].decode("utf-8", errors="replace")
        records.append({"key": str(key), "offset": offset, "length": length, "text": text})
    records.sort(key=lambda r: int(r["key"]) if r["key"].isdigit() else r["key"])
    return mapping, records, bin_data[: min_offset or 0]


def load_language(zf: zipfile.ZipFile, lang: str) -> tuple[dict, list[dict], bytes]:
    return decode_map(zf.read(TEXT_MAP.format(lang=lang)), zf.read(COMPRESS.format(lang=lang)))


def check_supported(source_records: list[dict], force: bool) -> dict:
    manifest = local_manifest()
    keys = [r["key"] for r in source_records]
    current = {
        "key_count": len(keys),
        "key_sha256": sha256_keys(keys),
        "expected_key_count": manifest.get("known_source_key_count"),
        "expected_key_sha256": manifest.get("known_source_key_sha256"),
    }
    ok = current["key_count"] == current["expected_key_count"] and current["key_sha256"] == current["expected_key_sha256"]
    current["supported"] = ok
    if not ok and not force:
        raise RuntimeError(
            "Versione testi del gioco non supportata. Scarica una release aggiornata della traduzione, "
            "oppure usa --force solo se accetti che eventuali testi nuovi restino non tradotti.\n"
            f"Righe note: {current['expected_key_count']} | Righe trovate: {current['key_count']}"
        )
    return current


def normalize_version(version: str) -> tuple[int, ...]:
    raw = version.strip().lower().lstrip("v")
    raw = raw.replace("-beta", ".0").replace("beta", ".0")
    nums = []
    for part in re.split(r"[^0-9]+", raw):
        if part:
            nums.append(int(part))
    return tuple(nums or [0])


def fetch_latest_release(manifest: dict) -> dict | None:
    repo = manifest.get("github_repo")
    if not repo:
        return None
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "AniimoItalianTranslationInstaller"})
    with urllib.request.urlopen(request, timeout=8) as response:
        return json.loads(response.read().decode("utf-8"))


def check_for_updates(silent: bool = False) -> dict:
    manifest = local_manifest()
    current = str(manifest.get("translation_version", "0.0.0"))
    repo = manifest.get("github_repo", "")
    releases_url = manifest.get("github_releases_url") or (f"https://github.com/{repo}/releases" if repo else "")
    result = {"current": current, "latest": current, "update_available": False, "releases_url": releases_url}
    try:
        latest = fetch_latest_release(manifest)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        result["error"] = str(exc)
        if not silent:
            print("Controllo aggiornamenti non disponibile. Puoi comunque installare normalmente.")
        return result
    if not latest:
        return result
    tag = str(latest.get("tag_name") or latest.get("name") or current)
    result["latest"] = tag
    result["releases_url"] = latest.get("html_url") or releases_url
    result["update_available"] = normalize_version(tag) > normalize_version(current)
    if not silent:
        if result["update_available"]:
            print("È disponibile una release più recente della traduzione:", tag)
            print("Download:", result["releases_url"])
        else:
            print("Traduzione aggiornata:", current)
    return result


def build_map_and_bin(source_records: list[dict], translations: dict[str, str], header: bytes) -> tuple[bytes, bytes, dict]:
    blob = bytearray(header)
    mapping: dict[str, object] = {"_count": len(source_records), "_version": int(time.time())}
    translated = 0
    reused = 0
    seen: dict[str, tuple[int, int]] = {}
    for rec in sorted(source_records, key=lambda r: int(r["key"]) if r["key"].isdigit() else r["key"]):
        key = rec["key"]
        text = translations.get(key, rec["text"])
        if key in translations:
            translated += 1
        if text in seen:
            offset, length = seen[text]
            reused += 1
        else:
            data = text.encode("utf-8")
            offset, length = len(blob), len(data)
            blob.extend(data)
            seen[text] = (offset, length)
        mapping[key] = [offset, length]
    return json.dumps(mapping, ensure_ascii=False, indent=4).encode("utf-8"), bytes(blob), {
        "source_count": len(source_records),
        "translated_count": translated,
        "fallback_count": len(source_records) - translated,
        "reused_strings": reused,
        "bin_size": len(blob),
    }


def local_data_offset(zip_path: Path, info: zipfile.ZipInfo) -> int:
    with zip_path.open("rb") as f:
        f.seek(info.header_offset + 26)
        name_len, extra_len = struct.unpack("<HH", f.read(4))
    return info.header_offset + 30 + name_len + extra_len


def repack_xdf(source_xdf: Path, source_xdt: Path, replacements: dict[str, bytes], out_xdf: Path, out_xdt: Path) -> None:
    out_xdf.parent.mkdir(parents=True, exist_ok=True)
    manifest = read_json(source_xdt)
    manifest_by_name = {entry["CEName"]: entry for entry in manifest.get("CMList", [])}
    with zipfile.ZipFile(source_xdf, "r") as zin, zipfile.ZipFile(out_xdf, "w") as zout:
        for info in zin.infolist():
            data = replacements.get(info.filename)
            if data is None:
                data = zin.read(info.filename)
            new_info = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            new_info.compress_type = info.compress_type
            new_info.comment = info.comment
            new_info.extra = info.extra
            new_info.internal_attr = info.internal_attr
            new_info.external_attr = info.external_attr
            new_info.create_system = info.create_system
            zout.writestr(new_info, data)

    new_list = []
    with zipfile.ZipFile(out_xdf, "r") as zout:
        for index, info in enumerate(zout.infolist()):
            data = zout.read(info.filename)
            entry = dict(manifest_by_name.get(info.filename, {"CEName": info.filename}))
            entry["CEName"] = info.filename
            entry["CEMD5"] = md5_bytes(data)
            entry["CESize"] = len(data)
            entry["CEIndex"] = index
            entry["CEOffset"] = local_data_offset(out_xdf, info)
            entry["CECSize"] = info.compress_size
            entry["CEContainer"] = entry.get("CEContainer", 0)
            new_list.append(entry)
    manifest["CMDataLen"] = out_xdf.stat().st_size
    manifest["CMDataMD5"] = md5_file(out_xdf)
    manifest["CMEntryNum"] = len(new_list)
    manifest["CMList"] = new_list
    write_json(out_xdt, manifest)


def process_running() -> list[str]:
    if os.name != "nt":
        return []
    try:
        output = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", "Get-Process | Select-Object -ExpandProperty ProcessName"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return []
    watched = {"aniimo", "worldx", "pc-launcher"}
    return sorted({line.strip() for line in output.splitlines() if line.strip().lower() in watched})


def update_local_manifests(game_dir: Path, patch_dir: Path) -> dict:
    result = {"md5list_updated": False, "verlist_updated": False, "touched": []}
    md5_path = game_dir / "md5list.txt"
    ver_path = game_dir / "verlist.txt"
    if not md5_path.exists():
        return result
    replacements = {
        "aniimo_data/cvs/res/lua/luascripts.xdf": patch_dir / XDF_NAME,
        "aniimo_data/cvs/res/lua/luascripts.xdt": patch_dir / XDT_NAME,
        "worldx_data/streamingassets/cvs/res/lua/luascripts.xdf": patch_dir / XDF_NAME,
        "worldx_data/streamingassets/cvs/res/lua/luascripts.xdt": patch_dir / XDT_NAME,
        "aniimo_data/streamingassets/cvs/res/lua/luascripts.xdf": patch_dir / XDF_NAME,
        "aniimo_data/streamingassets/cvs/res/lua/luascripts.xdt": patch_dir / XDT_NAME,
    }
    out_lines = []
    for line in md5_path.read_text(encoding="utf-8-sig").splitlines():
        parts = line.split(",", 2)
        if len(parts) == 3:
            rel = parts[2].replace("\\", "/").lower()
            patch_file = replacements.get(rel)
            if patch_file and patch_file.exists():
                out_lines.append(f"{md5_file(patch_file)},{patch_file.stat().st_size},{parts[2]}")
                result["touched"].append(parts[2])
                continue
        out_lines.append(line)
    out_md5 = patch_dir / "md5list.txt"
    out_md5.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    result["md5list_updated"] = True
    if ver_path.exists():
        raw = ver_path.read_text(encoding="utf-8-sig").strip()
        version = raw.split(",", 1)[0] if raw else "0"
        out_ver = patch_dir / "verlist.txt"
        out_ver.write_text(f"{version},{md5_file(out_md5)},{out_md5.stat().st_size}\n", encoding="utf-8")
        result["verlist_updated"] = True
    return result


def backup_live(paths: GamePaths) -> Path:
    backup = USER_WORK_DIR / "backups" / time.strftime("%Y%m%d-%H%M%S")
    backup.mkdir(parents=True, exist_ok=True)
    shutil.copy2(paths.xdf, backup / XDF_NAME)
    shutil.copy2(paths.xdt, backup / XDT_NAME)
    live_i18n = paths.lua_dir / "LuaScripts" / "Data" / "I18N"
    if live_i18n.exists():
        for file in live_i18n.glob("*.*"):
            if file.is_file():
                target = backup / "LuaScripts" / "Data" / "I18N" / file.name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, target)
    for name in ["md5list.txt", "verlist.txt"]:
        src = paths.game_dir / name
        if src.exists():
            shutil.copy2(src, backup / name)
    write_json(backup / "backup_manifest.json", {"game_dir": str(paths.game_dir), "lua_dir": str(paths.lua_dir)})
    return backup


def build_patch(paths: GamePaths, target_langs: list[str], force: bool) -> tuple[Path, dict]:
    translations = load_translations()
    patch_dir = USER_WORK_DIR / "patches" / time.strftime("%Y%m%d-%H%M%S")
    replacements: dict[str, bytes] = {}
    stats: dict[str, object] = {"target_languages": target_langs, "languages": {}}
    with zipfile.ZipFile(paths.xdf, "r") as zf:
        _, source_records, _ = load_language(zf, "en")
        stats["version_check"] = check_supported(source_records, force)
        for lang in target_langs:
            _, _, header = load_language(zf, lang)
            map_bytes, bin_bytes, lang_stats = build_map_and_bin(source_records, translations, header)
            replacements[TEXT_MAP.format(lang=lang)] = map_bytes
            replacements[COMPRESS.format(lang=lang)] = bin_bytes
            out_i18n = patch_dir / "LuaScripts" / "Data" / "I18N"
            out_i18n.mkdir(parents=True, exist_ok=True)
            (out_i18n / f"NewTextMap_{lang}.json").write_bytes(map_bytes)
            (out_i18n / f"Compress_{lang}.bin").write_bytes(bin_bytes)
            stats["languages"][lang] = lang_stats
    repack_xdf(paths.xdf, paths.xdt, replacements, patch_dir / XDF_NAME, patch_dir / XDT_NAME)
    stats["local_manifests"] = update_local_manifests(paths.game_dir, patch_dir)
    write_json(patch_dir / "patch_stats.json", stats)
    return patch_dir, stats


def copy_patch_into_game(paths: GamePaths, patch_dir: Path) -> None:
    shutil.copy2(patch_dir / XDF_NAME, paths.xdf)
    shutil.copy2(patch_dir / XDT_NAME, paths.xdt)
    patch_i18n = patch_dir / "LuaScripts" / "Data" / "I18N"
    live_i18n = paths.lua_dir / "LuaScripts" / "Data" / "I18N"
    if patch_i18n.exists():
        live_i18n.mkdir(parents=True, exist_ok=True)
        for file in patch_i18n.glob("*.*"):
            shutil.copy2(file, live_i18n / file.name)
    for name in ["md5list.txt", "verlist.txt"]:
        src = patch_dir / name
        if src.exists():
            shutil.copy2(src, paths.game_dir / name)


def cmd_check(args: argparse.Namespace) -> int:
    if not args.no_update_check:
        check_for_updates()
    paths = resolve_paths(resolve_game_dir(args.game_dir))
    with zipfile.ZipFile(paths.xdf, "r") as zf:
        _, source_records, _ = load_language(zf, "en")
        status = check_supported(source_records, args.force)
    print("Cartella gioco:", paths.game_dir)
    print("Risorse Lua:", paths.lua_dir)
    print("Stringhe:", status["key_count"])
    print("Versione supportata:", "sì" if status["supported"] else "no")
    return 0


def cmd_install(args: argparse.Namespace) -> int:
    if not args.no_update_check:
        update_status = check_for_updates()
        if update_status.get("update_available") and not args.ignore_update:
            print("Installazione fermata: scarica prima l'ultima traduzione.")
            print("Usa --ignore-update se vuoi comunque installare questo pacchetto.")
            return 3
    running = process_running()
    if running and not args.force_open:
        print("Chiudi prima gioco/launcher:", ", ".join(running))
        return 2
    paths = resolve_paths(resolve_game_dir(args.game_dir))
    target_langs = [args.target]
    if args.also_english and "en" not in target_langs:
        target_langs.append("en")
    print("Cartella gioco:", paths.game_dir)
    print("Creo backup...")
    backup = backup_live(paths)
    print("Backup:", backup)
    print("Genero patch italiana...")
    patch_dir, stats = build_patch(paths, target_langs, args.force)
    copy_patch_into_game(paths, patch_dir)
    print("Patch installata.")
    print("Lingua consigliata in gioco: Italiano. Se non compare, seleziona Tiếng Việt.")
    print("Statistiche:", json.dumps(stats.get("languages", {}), ensure_ascii=False))
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    status = check_for_updates()
    if status.get("update_available"):
        print("Apri la pagina Releases e scarica l'ultima versione:")
        print(status.get("releases_url", ""))
        return 1
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    running = process_running()
    if running and not args.force_open:
        print("Chiudi prima gioco/launcher:", ", ".join(running))
        return 2
    paths = resolve_paths(resolve_game_dir(args.game_dir))
    backups = sorted((USER_WORK_DIR / "backups").glob("*"), reverse=True)
    if not backups:
        raise FileNotFoundError(r"Nessun backup trovato in Documenti\AniimoItalianTranslation\backups")
    backup = backups[0]
    shutil.copy2(backup / XDF_NAME, paths.xdf)
    shutil.copy2(backup / XDT_NAME, paths.xdt)
    backup_i18n = backup / "LuaScripts" / "Data" / "I18N"
    live_i18n = paths.lua_dir / "LuaScripts" / "Data" / "I18N"
    if backup_i18n.exists():
        live_i18n.mkdir(parents=True, exist_ok=True)
        for file in backup_i18n.glob("*.*"):
            shutil.copy2(file, live_i18n / file.name)
    for name in ["md5list.txt", "verlist.txt"]:
        src = backup / name
        if src.exists():
            shutil.copy2(src, paths.game_dir / name)
    print("Backup ripristinato:", backup)
    return 0


def run_menu() -> int:
    print("Aniimo - Traduzione Italiana")
    print()
    print("1. Installa / aggiorna traduzione")
    print("2. Ripristina ultimo backup")
    print("3. Controlla aggiornamenti")
    print("0. Esci")
    print()
    choice = input("Scelta [1]: ").strip() or "1"
    if choice == "0":
        return 0
    if choice == "2":
        class Args:
            game_dir = None
            force_open = False
        return cmd_restore(Args())
    if choice == "3":
        class Args:
            pass
        return cmd_update(Args())
    class Args:
        game_dir = None
        force = False
        no_update_check = False
        target = "en"
        also_english = False
        force_open = False
        ignore_update = False
    return cmd_install(Args())


def pause_if_needed(enabled: bool) -> None:
    if enabled and os.name == "nt":
        try:
            input("\nPremi Invio per chiudere...")
        except EOFError:
            pass


def main() -> int:
    menu_mode = len(sys.argv) == 1
    if menu_mode:
        code = run_menu()
        pause_if_needed(True)
        return code

    parser = argparse.ArgumentParser(description="Aniimo Italian Translation installer")
    sub = parser.add_subparsers(dest="command", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--game-dir", help="Aniimo game folder")
    common.add_argument("--force", action="store_true", help="Install even if the game text version is unknown")
    common.add_argument("--no-update-check", action="store_true", help="Skip GitHub update check")
    check = sub.add_parser("check", parents=[common], help="Check compatibility")
    check.set_defaults(func=cmd_check)
    install = sub.add_parser("install", parents=[common], help="Install Italian translation")
    install.add_argument("--target", default="en", choices=["en", "vi_VN"], help="Language slot to replace")
    install.add_argument("--also-english", action="store_true", help="Also replace English; not recommended if accents are missing")
    install.add_argument("--force-open", action="store_true", help="Install even if game/launcher seem open")
    install.add_argument("--ignore-update", action="store_true", help="Install this package even if GitHub has a newer release")
    install.set_defaults(func=cmd_install)
    update = sub.add_parser("update", help="Check GitHub for a newer translation release")
    update.set_defaults(func=cmd_update)
    restore = sub.add_parser("restore", help="Restore latest backup")
    restore.add_argument("--game-dir", help="Aniimo game folder")
    restore.add_argument("--force-open", action="store_true")
    restore.set_defaults(func=cmd_restore)
    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as exc:
        print("Error:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
