#!/usr/bin/env python3
"""Aniimo String Extractor (Extract original texts from LuaScripts.xdf).

Standalone tool to extract text tables (English by default, or any other language)
from Aniimo into a clean, ready-to-translate CSV file.
Requires only standard Python 3. No external pip libraries needed.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import sys
import zipfile
from pathlib import Path


def find_steam_libraries() -> list[Path]:
    libraries: list[Path] = []
    if os.name != "nt":
        return libraries
    import winreg
    steam_roots: list[Path] = []
    for hive, subkey in [
        (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam"),
    ]:
        try:
            with winreg.OpenKey(hive, subkey) as key:
                val = winreg.QueryValueEx(key, "SteamPath")[0]
                if val:
                    steam_roots.append(Path(val))
        except OSError:
            pass

    for steam in set(steam_roots):
        if not steam.exists():
            continue
        libraries.append(steam)
        vdf = steam / "steamapps" / "libraryfolders.vdf"
        if vdf.is_file():
            try:
                content = vdf.read_text(encoding="utf-8", errors="ignore")
                for match in re.finditer(r'"path"\s+"([^"\\]*(?:\\.[^"\\]*)*)"', content):
                    p = Path(match.group(1).replace(r"\\", "\\"))
                    if p.exists():
                        libraries.append(p)
            except OSError:
                pass
    return list(dict.fromkeys(libraries))


def find_aniimo_folder() -> Path | None:
    # 1. Check current directory or parent directory
    candidates = [
        Path.cwd(),
        Path.cwd().parent,
        Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd(),
        Path(__file__).resolve().parents[1] if "__file__" in globals() else Path.cwd(),
    ]
    for c in candidates:
        if (c / "Aniimo.exe").is_file():
            return c
        if (c / "game" / "Aniimo.exe").is_file():
            return c / "game"

    # 2. Check Steam libraries
    for lib in find_steam_libraries():
        for sub in [
            lib / "steamapps" / "common" / "Aniimo",
            lib / "steamapps" / "common" / "Aniimo" / "game",
        ]:
            if (sub / "Aniimo.exe").is_file():
                return sub

    # 3. Check common Pawprint / local installation folders
    for drive in ["C", "D", "E", "F"]:
        for root in [
            Path(f"{drive}:/Pawprint/Aniimo/game"),
            Path(f"{drive}:/Pawprint/Aniimo"),
            Path(f"{drive}:/Program Files/Pawprint/Aniimo/game"),
            Path(f"{drive}:/Program Files (x86)/Pawprint/Aniimo/game"),
            Path(f"{drive}:/Games/Aniimo"),
        ]:
            if (root / "Aniimo.exe").is_file():
                return root

    return None


def locate_luascripts_xdf(game_dir: Path) -> Path | None:
    relative_paths = [
        Path(r"Aniimo_Data\cvs\res\lua\LuaScripts.xdf"),
        Path(r"Aniimo_Data\StreamingAssets\cvs\res\lua\LuaScripts.xdf"),
        Path(r"worldx_Data\StreamingAssets\cvs\res\lua\LuaScripts.xdf"),
    ]
    for rel in relative_paths:
        target = game_dir / rel
        if target.is_file():
            return target
    return None


def extract_language_from_xdf(xdf_path: Path, lang: str = "en") -> list[tuple[str, str, str]]:
    map_entry = f"xfs/luascripts/Data/I18N/NewTextMap_{lang}.json"
    bin_entry = f"xfs/luascripts/Data/I18N/Compress_{lang}.bin"

    with zipfile.ZipFile(xdf_path, "r") as zf:
        namelist = set(zf.namelist())
        if map_entry not in namelist or bin_entry not in namelist:
            available = [
                m.group(1)
                for name in namelist
                if (m := re.match(r"xfs/luascripts/Data/I18N/NewTextMap_([a-zA-Z0-9_]+)\.json", name))
            ]
            raise KeyError(
                f"Language '{lang}' not found in {xdf_path.name}.\n"
                f"Available languages in this archive: {', '.join(sorted(available))}"
            )

        mapping = json.loads(zf.read(map_entry).decode("utf-8-sig"))
        bin_data = zf.read(bin_entry)

    records = []
    for key, value in mapping.items():
        if str(key).startswith("_") or not isinstance(value, list) or len(value) != 2:
            continue
        offset, length = int(value[0]), int(value[1])
        text = bin_data[offset : offset + length].decode("utf-8", errors="replace")
        sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
        numeric_key = int(key) if str(key).isdigit() else 999999999
        records.append((numeric_key, str(key), sha256, text))

    records.sort(key=lambda item: item[0])
    return [(k, sha, text) for _, k, sha, text in records]


def main() -> int:
    print("=" * 60)
    print(" Aniimo String Extractor")
    print("=" * 60)

    # 1. Find Game Folder or XDF path
    xdf_path: Path | None = None
    if len(sys.argv) > 1:
        arg_path = Path(sys.argv[1].strip().strip('"'))
        if arg_path.is_file() and arg_path.name.lower() == "luascripts.xdf":
            xdf_path = arg_path
        elif arg_path.is_dir():
            xdf_path = locate_luascripts_xdf(arg_path)

    if not xdf_path:
        game_dir = find_aniimo_folder()
        if game_dir:
            print(f"[+] Found Aniimo installation at: {game_dir}")
            xdf_path = locate_luascripts_xdf(game_dir)
        
    if not xdf_path:
        print("[-] Could not automatically find Aniimo or LuaScripts.xdf.")
        user_input = input("Enter path to your Aniimo folder or LuaScripts.xdf: ").strip().strip('"')
        if not user_input:
            print("Operation cancelled.")
            return 1
        p = Path(user_input)
        if p.is_file() and p.name.lower() == "luascripts.xdf":
            xdf_path = p
        elif p.is_dir():
            xdf_path = locate_luascripts_xdf(p)

    if not xdf_path or not xdf_path.is_file():
        print("[-] LuaScripts.xdf could not be found.")
        return 1

    print(f"[+] Using archive: {xdf_path}")

    # Detect version if possible
    version_str = "unknown"
    lua_ver = xdf_path.parent / "LuaCacheVer.txt"
    if lua_ver.is_file():
        try:
            line = lua_ver.read_text(encoding="utf-8-sig", errors="replace").strip()
            first = line.split(",", 1)[0].strip()
            if first:
                version_str = first
        except OSError:
            pass
    print(f"[+] Game build: {version_str}")

    lang = "en"
    if len(sys.argv) > 2:
        lang = sys.argv[2].strip()

    print(f"[+] Extracting language '{lang}'...")
    try:
        records = extract_language_from_xdf(xdf_path, lang)
    except Exception as e:
        print(f"[-] Error extracting strings: {e}")
        return 1

    out_csv = Path(f"translation_{lang}.csv")
    print(f"[+] Writing {len(records)} strings to {out_csv.resolve()}...")
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["key", "source_sha256", lang])
        for k, sha, text in records:
            writer.writerow([k, sha, text])

    print("=" * 60)
    print(f"[OK] Extraction complete! Successfully exported {len(records)} strings.")
    print(f"File saved to: {out_csv.resolve()}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    res = 0
    try:
        res = main()
    finally:
        if sys.stdin and sys.stdin.isatty():
            try:
                input("\nPress Enter to exit...")
            except (EOFError, KeyboardInterrupt):
                pass
    sys.exit(res)
