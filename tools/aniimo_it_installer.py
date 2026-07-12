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
import webbrowser
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
AI_TRANSLATED_EN = "xfs/luascripts/Data/I18N/AITranslatedItems/AITranslatedItems_en.json"
DATE_SCRIPT = "xfs/luascripts/Guis/Panels/SpecialTrainChapterTip/SpecialTrainChapterTipCtrl.lua"
LOCALIZED_DATE_SCRIPT = "xfs/luascripts/Utils/LuaUIUtils.lua"
# The verified LuaJIT function calls string.format("%d/%02d/%02d", year, month, day).
# Swapping only the two field-load operands changes it to day/month/year without
# recompiling or redistributing the game's script.
DATE_YMD_BYTECODE = bytes.fromhex("2708190036091a05360a1b05360b1c0542060502")
DATE_DMY_BYTECODE = bytes.fromhex("2708190036091c05360a1b05360b1a0542060502")
# The shared UI date formatter has a separate English branch using
# string.format("%02d/%02d/%04d", month, day, year). It is used by mail and
# other interface panels, so its month/day operands must be swapped as well.
DATE_MDY_UI_BYTECODE = bytes.fromhex(
    "27091700360a1004360b1104360c0f0442070502"
)
DATE_DMY_UI_BYTECODE = bytes.fromhex(
    "27091700360a1104360b1004360c0f0442070502"
)
FONT_CACHE_RELS = (
    Path(r"Aniimo_Data\cvs\res\uab\win\DefaultPackage\CacheBundleFiles"),
    Path(r"Aniimo_Data\StreamingAssets\cvs\res\uab\win\DefaultPackage\CacheBundleFiles"),
    Path(r"worldx_Data\StreamingAssets\cvs\res\uab\win\DefaultPackage\CacheBundleFiles"),
)
FONT_BUNDLE_HASHES = (
    "e7d36f54529f2284a0d49f91b851242f",  # hot update 3036569
    "1407a625504745c29c260cd06d634e8c",  # base package 3032670
)
FONT_CONFIG_ASSET = "Assets/Res/XGUI/Font/Font_Localization_Config.asset"
VIETNAMESE_FONT_RESOURCE = "$UI_Font_Vietnamese.asset"
ENGLISH_LANGUAGE_TYPE = 2
VIETNAMESE_LANGUAGE_TYPE = 5
FONT_PATCH_DIR = "FontBundle"
if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent
    BUNDLE_DIR = Path(getattr(sys, "_MEIPASS", APP_DIR))
else:
    APP_DIR = Path(__file__).resolve().parents[1]
    BUNDLE_DIR = APP_DIR

DATA_DIR = BUNDLE_DIR / "data"
USER_WORK_DIR = Path.home() / "Documents" / "AniimoItalianTranslation"
INSTALLER_ASSET_NAME = "Aniimo-Italian-Translation.exe"
UPDATE_APPLY_COMMAND = "_apply-update"
UPDATE_COMPLETE_COMMAND = "--update-complete"
UPDATE_SCHEDULED = 20
_INSTANCE_LOCK_HANDLE = None


class ConsoleColor:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"


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


def parse_game_update(raw: str) -> str | None:
    """Return the numeric Aniimo update stored in verlist.txt."""
    first = raw.lstrip("\ufeff").strip().split(",", 1)[0].strip()
    return first if first.isdigit() else None


def parse_game_version_info(raw: str) -> dict:
    parts = raw.lstrip("\ufeff").strip().split(",")
    update = parts[0].strip() if parts and parts[0].strip().isdigit() else None
    revision = parts[1].strip().lower() if len(parts) > 1 and re.fullmatch(r"[0-9a-fA-F]{32,64}", parts[1].strip()) else None
    manifest_size = int(parts[2]) if len(parts) > 2 and parts[2].strip().isdigit() else None
    return {"update": update, "revision": revision, "manifest_size": manifest_size}


def read_game_version_info(game_dir: Path) -> dict:
    verlist = game_dir / "verlist.txt"
    if verlist.is_file():
        result = parse_game_version_info(verlist.read_text(encoding="utf-8-sig", errors="replace"))
    else:
        result = {"update": None, "revision": None, "manifest_size": None}
    package_versions: list[str] = []
    for relative in (
        Path(r"Aniimo_Data\cvs\res\uab\win\DefaultPackage\ManifestFiles\PackageManifest_DefaultPackage.version"),
        Path(r"Aniimo_Data\StreamingAssets\cvs\res\uab\win\DefaultPackage\PackageManifest_DefaultPackage.version"),
        Path(r"worldx_Data\StreamingAssets\cvs\res\uab\win\DefaultPackage\PackageManifest_DefaultPackage.version"),
    ):
        path = game_dir / relative
        if not path.is_file():
            continue
        value = path.read_text(encoding="utf-8-sig", errors="replace").strip()
        if value.isdigit():
            package_versions.append(value)
    if package_versions:
        result["update"] = max(package_versions, key=int)
    return result


def read_game_update(game_dir: Path) -> str | None:
    return read_game_version_info(game_dir)["update"]


def supported_game_updates(manifest: dict) -> list[str]:
    values = manifest.get("supported_game_updates") or []
    return [str(value) for value in values if str(value).isdigit()]


def supported_game_revisions(manifest: dict) -> list[str]:
    values = manifest.get("supported_game_revisions") or []
    return [str(value).lower() for value in values if re.fullmatch(r"[0-9a-fA-F]{32,64}", str(value))]


def load_settings() -> dict:
    path = USER_WORK_DIR / "settings.json"
    if not path.is_file():
        return {}
    try:
        data = read_json(path)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_game_dir(game_dir: Path) -> None:
    write_json(USER_WORK_DIR / "settings.json", {"game_dir": str(game_dir.resolve())})


def load_installed_state() -> dict:
    path = USER_WORK_DIR / "installed_state.json"
    if not path.is_file():
        return {}
    try:
        data = read_json(path)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def recorded_translation_version(game_dir: Path) -> str | None:
    """Return the version recorded for this exact game installation."""
    state = load_installed_state()
    try:
        same_game = Path(str(state.get("game_dir") or "")).resolve() == game_dir.resolve()
    except (OSError, ValueError):
        same_game = False
    if not same_game:
        return None
    version = str(state.get("translation_version") or "").strip().lstrip("v")
    return version or None


def effective_game_revision(game_dir: Path, current_revision: str | None, translation_installed: bool) -> str | None:
    if not translation_installed:
        return current_revision
    state = load_installed_state()
    try:
        same_game = Path(str(state.get("game_dir") or "")).resolve() == game_dir.resolve()
    except (OSError, ValueError):
        same_game = False
    patched_revision = str(state.get("patched_game_revision") or "").lower()
    official_revision = str(state.get("official_game_revision") or "").lower()
    if same_game and current_revision == patched_revision and re.fullmatch(r"[0-9a-f]{32,64}", official_revision):
        return official_revision
    return current_revision


def record_installed_state(paths: GamePaths, official_info: dict) -> None:
    patched_info = read_game_version_info(paths.game_dir)
    write_json(USER_WORK_DIR / "installed_state.json", {
        "game_dir": str(paths.game_dir.resolve()),
        "translation_version": str(local_manifest().get("translation_version", "")),
        "game_update": official_info.get("update"),
        "official_game_revision": official_info.get("revision"),
        "patched_game_revision": patched_info.get("revision"),
        "installed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    })


def game_info_before_install(paths: GamePaths) -> dict:
    info = read_game_version_info(paths.game_dir)
    try:
        installed = detect_translation_installation(paths.game_dir)["installed"]
        info["revision"] = effective_game_revision(paths.game_dir, info.get("revision"), installed)
    except (FileNotFoundError, OSError, ValueError, KeyError, zipfile.BadZipFile, json.JSONDecodeError):
        pass
    return info


def clear_installed_state(game_dir: Path) -> None:
    path = USER_WORK_DIR / "installed_state.json"
    if not path.is_file():
        return
    state = load_installed_state()
    try:
        same_game = Path(str(state.get("game_dir") or "")).resolve() == game_dir.resolve()
    except (OSError, ValueError):
        same_game = False
    if same_game:
        path.unlink()


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def looks_like_game_dir(path: Path) -> bool:
    return (path / "Aniimo_Data").exists() or any((path / rel / XDF_NAME).exists() for rel in LUA_RELS)


def default_target_language_slot() -> str:
    return "en"


def translation_csv_for_slot(slot: str) -> Path:
    # English remains the visible language slot. Its font is redirected to the
    # bundled Vietnamese font, so the production master can use real accents.
    return DATA_DIR / "translation_it.csv"


def load_translations(slot: str | None = None) -> dict[str, str]:
    csv_path = translation_csv_for_slot(slot or default_target_language_slot())
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


def recovered_english_fallback_keys() -> list[str]:
    """Keys whose official English value is 0 but whose Italian text is complete."""
    csv_path = translation_csv_for_slot("en")
    recovered: list[str] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            key = (row.get("key") or "").strip()
            source = (row.get("source_en") or "").strip()
            text = (row.get("it") or "").strip()
            if key and source == "0" and text and text != "0":
                recovered.append(key)
    return recovered


def mark_english_fallbacks_as_translated(raw: bytes, keys: list[str]) -> tuple[bytes, int]:
    """Make Aniimo accept locally recovered English-slot fallbacks as translations.

    Aniimo keeps a separate allow-list for texts considered available in the
    English locale. Without these entries, some official 0 values bypass the
    patched text map and the runtime injects an English sentence instead.
    """
    values = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(values, list) or any(not isinstance(value, int) for value in values):
        raise ValueError("Elenco delle traduzioni English di Aniimo non valido.")
    existing = set(values)
    additions = sorted(
        (int(key) for key in keys if int(key) not in existing),
    )
    values.extend(additions)
    return (json.dumps(values, ensure_ascii=False, indent=2).encode("utf-8"), len(additions))


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


def resolve_game_dir_with_source(raw: str | None) -> tuple[Path, str]:
    if raw:
        p = Path(raw).expanduser().resolve()
        if looks_like_game_dir(p):
            return p, "manuale"
        if looks_like_game_dir(p / "game"):
            return (p / "game").resolve(), "manuale"
        raise FileNotFoundError(f"Invalid Aniimo folder: {p}")
    saved = str(load_settings().get("game_dir") or "").strip()
    if saved:
        p = Path(saved).expanduser().resolve()
        if looks_like_game_dir(p):
            return p, "salvato"
        if looks_like_game_dir(p / "game"):
            return (p / "game").resolve(), "salvato"
    for candidate in candidate_game_dirs():
        if looks_like_game_dir(candidate):
            return candidate.resolve(), "automatico"
    raise FileNotFoundError(
        "Cartella di Aniimo non trovata. Metti questo eseguibile nella root del gioco, "
        "accanto ad Aniimo_Data, oppure avvialo con --game-dir \"PERCORSO\\game\"."
    )


def resolve_game_dir(raw: str | None) -> Path:
    return resolve_game_dir_with_source(raw)[0]


def choose_game_dir_windows() -> str | None:
    if os.name != "nt":
        return None
    script = (
        "Add-Type -AssemblyName System.Windows.Forms; "
        "$dialog=New-Object System.Windows.Forms.FolderBrowserDialog; "
        "$dialog.Description='Seleziona la cartella di Aniimo che contiene Aniimo_Data'; "
        "$dialog.ShowNewFolderButton=$false; "
        "if($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK){$dialog.SelectedPath}"
    )
    try:
        output = subprocess.check_output(
            ["powershell", "-NoProfile", "-STA", "-Command", script],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return output or None
    except (OSError, subprocess.CalledProcessError):
        return None


def print_game_path_help() -> None:
    print("Come trovare la cartella giusta:")
    print("  1. Apri la cartella in cui Pawprint ha installato Aniimo.")
    print("  2. Apri la sottocartella 'game', se presente.")
    print("  3. Seleziona la cartella che contiene 'Aniimo_Data'.")
    print(r"     Esempio: F:\Pawprint\Aniimo\game")


def configure_game_dir() -> Path | None:
    print_game_path_help()
    print()
    raw = choose_game_dir_windows()
    if not raw:
        raw = input("Incolla qui il percorso, oppure premi Invio per annullare: ").strip().strip('"')
    if not raw:
        return None
    try:
        game_dir, _ = resolve_game_dir_with_source(raw)
    except FileNotFoundError:
        print("La cartella scelta non contiene Aniimo_Data. Nessun percorso è stato salvato.")
        return None
    save_game_dir(game_dir)
    print("Percorso verificato e salvato:", game_dir)
    return game_dir


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


def translation_match_status(source_records: list[dict], translations: dict[str, str]) -> dict:
    comparable = 0
    matched = 0
    for record in source_records:
        expected = translations.get(record["key"])
        if expected is None:
            continue
        comparable += 1
        if record["text"] == expected:
            matched += 1
    ratio = matched / comparable if comparable else 0.0
    return {
        "installed": comparable >= 100 and ratio >= 0.90,
        "matches_current": comparable >= 100 and comparable == len(translations) and matched == comparable,
        "matched": matched,
        "comparable": comparable,
        "ratio": ratio,
    }


def patch_dynamic_date_order(script_data: bytes) -> tuple[bytes, bool]:
    """Change the verified chapter date from YYYY/MM/DD to DD/MM/YYYY."""
    ymd_count = script_data.count(DATE_YMD_BYTECODE)
    dmy_count = script_data.count(DATE_DMY_BYTECODE)
    if ymd_count == 1 and dmy_count == 0:
        patched = script_data.replace(DATE_YMD_BYTECODE, DATE_DMY_BYTECODE, 1)
        if patched.count(DATE_YMD_BYTECODE) != 0 or patched.count(DATE_DMY_BYTECODE) != 1:
            raise RuntimeError("Verifica del formato data italiano non riuscita.")
        return patched, True
    if ymd_count == 0 and dmy_count == 1:
        return script_data, False
    raise ValueError(
        "Script della data dinamica non riconosciuto. La modifica GG/MM/AAAA non verrà applicata "
        "a una versione non verificata."
    )


def dynamic_date_is_italian(script_data: bytes) -> bool:
    return script_data.count(DATE_DMY_BYTECODE) == 1 and script_data.count(DATE_YMD_BYTECODE) == 0


def patch_localized_date_order(script_data: bytes) -> tuple[bytes, bool]:
    """Change the verified shared UI date from MM/DD/YYYY to DD/MM/YYYY."""
    mdy_count = script_data.count(DATE_MDY_UI_BYTECODE)
    dmy_count = script_data.count(DATE_DMY_UI_BYTECODE)
    if mdy_count == 1 and dmy_count == 0:
        patched = script_data.replace(DATE_MDY_UI_BYTECODE, DATE_DMY_UI_BYTECODE, 1)
        if (
            patched.count(DATE_MDY_UI_BYTECODE) != 0
            or patched.count(DATE_DMY_UI_BYTECODE) != 1
        ):
            raise RuntimeError("Verifica del formato data UI italiano non riuscita.")
        return patched, True
    if mdy_count == 0 and dmy_count == 1:
        return script_data, False
    raise ValueError(
        "Formattatore data UI non riconosciuto. La modifica GG/MM/AAAA non verrà "
        "applicata a una versione non verificata."
    )


def localized_date_is_italian(script_data: bytes) -> bool:
    return (
        script_data.count(DATE_DMY_UI_BYTECODE) == 1
        and script_data.count(DATE_MDY_UI_BYTECODE) == 0
    )


def detect_translation_installation(game_dir: Path) -> dict:
    paths = resolve_paths(game_dir)
    with zipfile.ZipFile(paths.xdf, "r") as zf:
        _, english_records, _ = load_language(zf, "en")
        try:
            date_italian = dynamic_date_is_italian(
                zf.read(DATE_SCRIPT)
            ) and localized_date_is_italian(zf.read(LOCALIZED_DATE_SCRIPT))
        except KeyError:
            date_italian = False
    result = translation_match_status(english_records, load_translations("en"))
    try:
        font_accented = english_uses_vietnamese_font(find_font_bundle(game_dir))
    except (FileNotFoundError, OSError, RuntimeError, ValueError):
        font_accented = False
    result["font_accented"] = font_accented
    result["date_italian"] = date_italian
    result["installed"] = result["installed"] and font_accented
    result["matches_current"] = result["matches_current"] and font_accented and date_italian
    result["installed_slots"] = ["en"] if result["installed"] else []
    result["detected_slot"] = "en"
    compatibility = check_supported(english_records, force=True)
    result["texts_supported"] = compatibility["supported"]
    result["key_count"] = compatibility["key_count"]
    result["key_sha256"] = compatibility["key_sha256"]
    return result


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
    core, separator, suffix = raw.partition("-")
    nums = [int(part) for part in re.findall(r"\d+", core)]
    nums = (nums + [0, 0, 0])[:3]
    stable_rank = 1 if not separator else 0
    suffix_nums = [int(part) for part in re.findall(r"\d+", suffix)]
    return tuple(nums + [stable_rank] + suffix_nums)


def fetch_latest_release(manifest: dict) -> dict | None:
    repo = manifest.get("github_repo")
    if not repo:
        return None
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "AniimoItalianTranslationInstaller"})
    with urllib.request.urlopen(request, timeout=8) as response:
        return json.loads(response.read().decode("utf-8"))


def find_installer_asset(release: dict) -> dict | None:
    for asset in release.get("assets") or []:
        if asset.get("name") == INSTALLER_ASSET_NAME:
            return asset
    return None


def check_for_updates(silent: bool = False) -> dict:
    manifest = local_manifest()
    current = str(manifest.get("translation_version", "0.0.0"))
    repo = manifest.get("github_repo", "")
    releases_url = manifest.get("github_releases_url") or (f"https://github.com/{repo}/releases" if repo else "")
    result = {
        "current": current,
        "latest": current,
        "update_available": False,
        "releases_url": releases_url,
        "release": None,
        "asset": None,
    }
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
    result["release"] = latest
    result["asset"] = find_installer_asset(latest)
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


def download_update_asset(asset: dict, destination: Path) -> str:
    url = str(asset.get("browser_download_url") or "")
    digest = str(asset.get("digest") or "")
    if not url.startswith("https://github.com/"):
        raise RuntimeError("Indirizzo di download GitHub non valido.")
    if not digest.lower().startswith("sha256:"):
        raise RuntimeError("GitHub non ha fornito l'hash SHA-256: aggiornamento automatico annullato.")
    expected_hash = digest.split(":", 1)[1].lower()
    expected_size = int(asset.get("size") or 0)
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_suffix(destination.suffix + ".download")
    request = urllib.request.Request(url, headers={"User-Agent": "AniimoItalianTranslationInstaller"})
    h = hashlib.sha256()
    size = 0
    try:
        with urllib.request.urlopen(request, timeout=30) as response, partial.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                output.write(chunk)
                h.update(chunk)
                size += len(chunk)
        if expected_size and size != expected_size:
            raise RuntimeError(f"Dimensione download non valida: attesi {expected_size} byte, ricevuti {size}.")
        actual_hash = h.hexdigest().lower()
        if actual_hash != expected_hash:
            raise RuntimeError("Hash SHA-256 non valido: il file scaricato non verrà eseguito.")
        os.replace(partial, destination)
        return actual_hash
    finally:
        if partial.exists():
            partial.unlink()


def acquire_installer_instance_lock() -> bool:
    """Keep a second interactive installer window from blocking self-update."""
    global _INSTANCE_LOCK_HANDLE
    if _INSTANCE_LOCK_HANDLE is not None or os.name != "nt":
        return True
    import msvcrt

    try:
        USER_WORK_DIR.mkdir(parents=True, exist_ok=True)
        handle = (USER_WORK_DIR / "installer.lock").open("a+b")
    except OSError:
        return True
    handle.seek(0, os.SEEK_END)
    if handle.tell() == 0:
        handle.write(b"0")
        handle.flush()
    handle.seek(0)
    try:
        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        handle.close()
        return False
    _INSTANCE_LOCK_HANDLE = handle
    return True


def prompt_close_other_installers() -> bool:
    if os.name != "nt":
        return False
    try:
        import ctypes

        message = (
            "Un'altra finestra di Aniimo - Traduzione Italiana sta usando il vecchio EXE.\n\n"
            "Chiudi tutte le altre finestre dell'installer, poi premi Riprova."
        )
        flags = 0x00000005 | 0x00000030 | 0x00040000  # Retry/Cancel, warning, topmost
        return ctypes.windll.user32.MessageBoxW(None, message, "Aggiornamento installer", flags) == 4
    except Exception:
        return False


def show_update_failure_message() -> None:
    if os.name != "nt":
        return
    try:
        import ctypes

        message = (
            "Aggiornamento non completato.\n\n"
            "Chiudi tutte le finestre dell'installer e riprova. "
            "Il vecchio EXE non è stato modificato."
        )
        ctypes.windll.user32.MessageBoxW(None, message, "Aniimo - Traduzione Italiana", 0x00000010 | 0x00040000)
    except Exception:
        pass


def cleanup_update_cache() -> int:
    updates = USER_WORK_DIR / "updates"
    if not updates.is_dir():
        return 0
    removed = 0
    current = Path(sys.executable).resolve()
    for file in updates.glob("*/*"):
        if not file.is_file() or not (
            file.name == INSTALLER_ASSET_NAME
            or file.name.startswith("Aniimo-Italian-Translation-")
            or file.name.endswith(".exe.download")
        ):
            continue
        try:
            if file.resolve() != current:
                file.unlink()
                removed += 1
        except OSError:
            pass
    return removed


def apply_update_payload(
    source: Path,
    target: Path,
    retries: int = 120,
    delay: float = 0.5,
    launch: bool = True,
    launch_args: list[str] | None = None,
) -> bool:
    """Replace the old EXE after it exits. This runs from the downloaded new EXE."""
    source = source.resolve()
    target = target.resolve()
    if source == target or target.suffix.lower() != ".exe":
        raise ValueError("Percorso di aggiornamento non valido.")
    staging = target.with_name(target.name + ".new")
    last_error: Exception | None = None
    for _ in range(retries):
        try:
            shutil.copy2(source, staging)
            os.replace(staging, target)
            if launch:
                launch_kwargs: dict[str, object] = {"cwd": str(target.parent)}
                if os.name == "nt":
                    launch_kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
                subprocess.Popen([str(target), *(launch_args or [])], **launch_kwargs)
            return True
        except (PermissionError, OSError) as exc:
            last_error = exc
            time.sleep(delay)
        finally:
            if staging.exists():
                try:
                    staging.unlink()
                except OSError:
                    pass
    raise RuntimeError(f"Impossibile sostituire il vecchio installer: {last_error}")


def schedule_self_update(status: dict) -> bool:
    if os.name != "nt" or not getattr(sys, "frozen", False):
        print("L'aggiornamento automatico è disponibile nell'installer EXE per Windows.")
        return False
    asset = status.get("asset")
    if not asset:
        raise RuntimeError("La release più recente non contiene l'installer previsto.")
    tag = re.sub(r"[^A-Za-z0-9._-]+", "_", str(status.get("latest") or "latest"))
    attempt = f"{os.getpid()}-{int(time.time() * 1000)}"
    downloaded = USER_WORK_DIR / "updates" / tag / f"Aniimo-Italian-Translation-{attempt}.exe"
    print("Scarico il nuovo installer da GitHub...")
    verified_hash = download_update_asset(asset, downloaded)
    print("Download verificato (SHA-256):", verified_hash.upper())
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    subprocess.Popen(
        [
            str(downloaded),
            UPDATE_APPLY_COMMAND,
            "--target-exe",
            str(Path(sys.executable).resolve()),
            "--previous-version",
            str(status.get("current") or ""),
        ],
        cwd=str(downloaded.parent),
        creationflags=creationflags,
    )
    print("Aggiornamento pronto. L'installer verrà riaperto automaticamente.")
    return True


def cmd_apply_update(args: argparse.Namespace) -> int:
    log_path = USER_WORK_DIR / "update_error.txt"
    try:
        completion_args = [UPDATE_COMPLETE_COMMAND]
        if args.previous_version:
            completion_args.append(str(args.previous_version))
        try:
            apply_update_payload(
                Path(sys.executable), Path(args.target_exe), retries=20, delay=0.25, launch_args=completion_args
            )
        except RuntimeError:
            if not prompt_close_other_installers():
                raise
            apply_update_payload(Path(sys.executable), Path(args.target_exe), launch_args=completion_args)
        if log_path.exists():
            log_path.unlink()
        return 0
    except Exception as exc:
        USER_WORK_DIR.mkdir(parents=True, exist_ok=True)
        log_path.write_text(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {exc}\n", encoding="utf-8")
        show_update_failure_message()
        return 1


def build_map_and_bin(source_records: list[dict], translations: dict[str, str], header: bytes) -> tuple[bytes, bytes, dict]:
    updated_header = bytearray(header)
    if len(updated_header) < 4:
        raise ValueError(f"Header localizzazione non valido: {len(updated_header)} byte")
    version = int(time.time())
    updated_header[:4] = struct.pack("<I", version)
    blob = bytearray(updated_header)
    mapping: dict[str, object] = {"_count": len(source_records), "_version": version}
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
        "map_version": version,
        "bin_version": struct.unpack("<I", blob[:4])[0] if len(blob) >= 4 else None,
    }


def redirect_english_font_variant(config_tree: dict) -> bool:
    """Make English use Aniimo's bundled Vietnamese TMP font.

    Aniimo normally has no explicit English variant, so it falls back to the
    base Chinese font. Reusing the hidden Vietnamese variant preserves every
    Italian accented glyph without shipping third-party game assets.
    """
    entries = config_tree.get("entries") or []
    variants = entries[0].get("variants") if len(entries) == 1 else None
    if not isinstance(variants, list):
        raise ValueError("Configurazione dei font di Aniimo inattesa.")
    english = [row for row in variants if row.get("language") == ENGLISH_LANGUAGE_TYPE]
    if english:
        if len(english) == 1 and english[0].get("fontResID") == VIETNAMESE_FONT_RESOURCE:
            return False
        raise ValueError("La lingua English usa già un font diverso e non riconosciuto.")
    vietnamese = [
        row
        for row in variants
        if row.get("language") == VIETNAMESE_LANGUAGE_TYPE
        and row.get("fontResID") == VIETNAMESE_FONT_RESOURCE
    ]
    if len(vietnamese) != 1:
        raise ValueError("Font vietnamita di Aniimo non trovato nella configurazione prevista.")
    vietnamese[0]["language"] = ENGLISH_LANGUAGE_TYPE
    return True


def find_font_bundle(game_dir: Path) -> Path:
    for relative in FONT_CACHE_RELS:
        cache = game_dir / relative
        for digest in FONT_BUNDLE_HASHES:
            candidate = cache / digest[:2] / digest / "cdata.uab"
            if candidate.is_file():
                return candidate
    raise FileNotFoundError(
        "Pacchetto font di Aniimo non trovato. Avvia il gioco una volta, attendi il completamento "
        "del download delle risorse e riprova."
    )


def load_font_config(font_bundle: Path):
    try:
        import UnityPy
    except ImportError as exc:
        raise RuntimeError("Componente interno per la gestione del font non disponibile.") from exc
    env = UnityPy.load(str(font_bundle))
    try:
        config_obj = env.container[FONT_CONFIG_ASSET].deref()
    except KeyError as exc:
        raise ValueError("Configurazione di localizzazione del font non trovata nel pacchetto Aniimo.")
    return env, config_obj, config_obj.read_typetree()


def english_uses_vietnamese_font(font_bundle: Path) -> bool:
    _, _, tree = load_font_config(font_bundle)
    entries = tree.get("entries") or []
    variants = entries[0].get("variants") if len(entries) == 1 else []
    return any(
        row.get("language") == ENGLISH_LANGUAGE_TYPE
        and row.get("fontResID") == VIETNAMESE_FONT_RESOURCE
        for row in variants
    )


def patch_font_bundle(source: Path, destination: Path) -> dict:
    env, config_obj, tree = load_font_config(source)
    changed = redirect_english_font_variant(tree)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if changed:
        config_obj.save_typetree(tree)
        destination.write_bytes(env.file.save(packer="original"))
    else:
        shutil.copy2(source, destination)
    if not english_uses_vietnamese_font(destination):
        raise RuntimeError("Verifica del font accentato non riuscita dopo la modifica.")
    return {
        "changed_now": changed,
        "source_md5": md5_file(source),
        "patched_md5": md5_file(destination),
        "source_size": source.stat().st_size,
        "patched_size": destination.stat().st_size,
        "mapping": "English -> UI_Font_Vietnamese",
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
    original_i18n_files: list[str] = []
    if live_i18n.exists():
        for file in live_i18n.glob("*.*"):
            if file.is_file():
                original_i18n_files.append(file.name)
                target = backup / "LuaScripts" / "Data" / "I18N" / file.name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, target)
    for name in ["md5list.txt", "verlist.txt"]:
        src = paths.game_dir / name
        if src.exists():
            shutil.copy2(src, backup / name)
    font_bundle = find_font_bundle(paths.game_dir)
    font_relative = font_bundle.relative_to(paths.game_dir)
    font_backup = backup / FONT_PATCH_DIR
    font_backup.mkdir(parents=True, exist_ok=True)
    shutil.copy2(font_bundle, font_backup / "cdata.uab")
    font_info = font_bundle.with_name("cinfo.bin")
    if font_info.is_file():
        shutil.copy2(font_info, font_backup / "cinfo.bin")
    write_json(backup / "backup_manifest.json", {
        "game_dir": str(paths.game_dir),
        "lua_dir": str(paths.lua_dir),
        "original_i18n_files": sorted(original_i18n_files),
        "created_i18n_files": [],
        "font_bundle_relative": str(font_relative),
        "font_info_present": font_info.is_file(),
    })
    return backup


def record_created_i18n_files(backup: Path, patch_dir: Path) -> list[str]:
    manifest_path = backup / "backup_manifest.json"
    manifest = read_json(manifest_path)
    original = set(manifest.get("original_i18n_files", []))
    patch_i18n = patch_dir / "LuaScripts" / "Data" / "I18N"
    patch_files = {file.name for file in patch_i18n.glob("*.*") if file.is_file()}
    created = sorted(patch_files - original)
    manifest["created_i18n_files"] = created
    write_json(manifest_path, manifest)
    return created


def build_patch(paths: GamePaths, target_langs: list[str], force: bool) -> tuple[Path, dict]:
    patch_dir = USER_WORK_DIR / "patches" / time.strftime("%Y%m%d-%H%M%S")
    replacements: dict[str, bytes] = {}
    stats: dict[str, object] = {
        "target_languages": target_langs,
        "game_update": read_game_update(paths.game_dir),
        "languages": {},
    }
    with zipfile.ZipFile(paths.xdf, "r") as zf:
        _, source_records, _ = load_language(zf, "en")
        stats["version_check"] = check_supported(source_records, force)
        for lang in target_langs:
            translations = load_translations(lang)
            _, _, header = load_language(zf, lang)
            map_bytes, bin_bytes, lang_stats = build_map_and_bin(source_records, translations, header)
            replacements[TEXT_MAP.format(lang=lang)] = map_bytes
            replacements[COMPRESS.format(lang=lang)] = bin_bytes
            out_i18n = patch_dir / "LuaScripts" / "Data" / "I18N"
            out_i18n.mkdir(parents=True, exist_ok=True)
            (out_i18n / f"NewTextMap_{lang}.json").write_bytes(map_bytes)
            (out_i18n / f"Compress_{lang}.bin").write_bytes(bin_bytes)
            stats["languages"][lang] = lang_stats
        if "en" in target_langs:
            fallback_keys = recovered_english_fallback_keys()
            translated_items, added = mark_english_fallbacks_as_translated(
                zf.read(AI_TRANSLATED_EN), fallback_keys
            )
            replacements[AI_TRANSLATED_EN] = translated_items
            stats["english_runtime_fallbacks"] = {
                "recovered_keys": len(fallback_keys),
                "allow_list_entries_added": added,
            }
            date_script, date_changed = patch_dynamic_date_order(zf.read(DATE_SCRIPT))
            replacements[DATE_SCRIPT] = date_script
            localized_date_script, localized_date_changed = patch_localized_date_order(
                zf.read(LOCALIZED_DATE_SCRIPT)
            )
            replacements[LOCALIZED_DATE_SCRIPT] = localized_date_script
            stats["dynamic_date"] = {
                "format": "DD/MM/YYYY",
                "changed_now": date_changed or localized_date_changed,
                "chapter_changed_now": date_changed,
                "localized_ui_changed_now": localized_date_changed,
                "verified": dynamic_date_is_italian(date_script)
                and localized_date_is_italian(localized_date_script),
                "chapter_script_sha256": hashlib.sha256(date_script).hexdigest(),
                "localized_ui_script_sha256": hashlib.sha256(
                    localized_date_script
                ).hexdigest(),
            }
    repack_xdf(paths.xdf, paths.xdt, replacements, patch_dir / XDF_NAME, patch_dir / XDT_NAME)
    stats["font"] = patch_font_bundle(
        find_font_bundle(paths.game_dir), patch_dir / FONT_PATCH_DIR / "cdata.uab"
    )
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
    patched_font = patch_dir / FONT_PATCH_DIR / "cdata.uab"
    if patched_font.is_file():
        shutil.copy2(patched_font, find_font_bundle(paths.game_dir))
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
    version_info = read_game_version_info(paths.game_dir)
    print("Versione gioco rilevata:", version_info["update"] or "non disponibile")
    print("Revisione hot update:", version_info["revision"] or "non disponibile")
    print("Versioni gioco dichiarate compatibili:", ", ".join(supported_game_updates(local_manifest())) or "non specificate")
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
    official_info = game_info_before_install(paths)
    target_langs = ["en"]
    print("Cartella gioco:", paths.game_dir)
    print("Creo backup...")
    backup = backup_live(paths)
    print("Backup:", backup)
    print("Genero patch italiana...")
    patch_dir, stats = build_patch(paths, target_langs, args.force)
    record_created_i18n_files(backup, patch_dir)
    copy_patch_into_game(paths, patch_dir)
    record_installed_state(paths, official_info)
    print("Patch installata.")
    print("Lingua da selezionare in gioco: Inglese")
    print("Font accentato: ✓ English usa il font vietnamita incluso in Aniimo")
    print("Statistiche:", json.dumps(stats.get("languages", {}), ensure_ascii=False))
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    status = check_for_updates()
    if status.get("update_available"):
        try:
            return UPDATE_SCHEDULED if schedule_self_update(status) else 1
        except Exception as exc:
            print("Aggiornamento automatico non riuscito:", exc)
            print("Puoi scaricarlo manualmente da:", status.get("releases_url", ""))
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
    manifest_path = backup / "backup_manifest.json"
    manifest = read_json(manifest_path) if manifest_path.exists() else {}
    if live_i18n.exists():
        for name in manifest.get("created_i18n_files", []):
            if Path(name).name != name:
                raise ValueError(f"Nome file I18N non valido nel backup: {name}")
            target = live_i18n / name
            if target.is_file():
                target.unlink()
    if backup_i18n.exists():
        live_i18n.mkdir(parents=True, exist_ok=True)
        for file in backup_i18n.glob("*.*"):
            shutil.copy2(file, live_i18n / file.name)
    font_relative = str(manifest.get("font_bundle_relative") or "")
    backup_font = backup / FONT_PATCH_DIR / "cdata.uab"
    if font_relative and backup_font.is_file():
        font_target = (paths.game_dir / Path(font_relative)).resolve()
        game_root = paths.game_dir.resolve()
        if game_root not in font_target.parents:
            raise ValueError("Percorso font non valido nel backup.")
        font_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup_font, font_target)
        backup_info = backup / FONT_PATCH_DIR / "cinfo.bin"
        if manifest.get("font_info_present") and backup_info.is_file():
            shutil.copy2(backup_info, font_target.with_name("cinfo.bin"))
    for name in ["md5list.txt", "verlist.txt"]:
        src = backup / name
        if src.exists():
            shutil.copy2(src, paths.game_dir / name)
    clear_installed_state(paths.game_dir)
    print("Backup ripristinato:", backup)
    return 0


def color_text(text: str, color: str, enabled: bool) -> str:
    return f"{color}{text}{ConsoleColor.RESET}" if enabled else text


def enable_console_colors() -> bool:
    if not sys.stdout.isatty():
        return False
    if os.name != "nt":
        return True
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        return bool(kernel32.SetConsoleMode(handle, mode.value | 0x0004))
    except Exception:
        return False


def collect_startup_status() -> dict:
    manifest = local_manifest()
    result: dict[str, object] = {
        "manifest": manifest,
        "game_dir": None,
        "game_path_source": None,
        "detected_game_update": None,
        "detected_game_revision": None,
        "translation_installed": None,
        "translation_match_ratio": None,
        "translation_matches_installer": None,
        "installed_translation_version": None,
        "dynamic_date_italian": None,
        "translation_slot": None,
        "text_resources_supported": None,
        "update": check_for_updates(silent=True),
    }
    try:
        game_dir, source = resolve_game_dir_with_source(None)
        result["game_dir"] = game_dir
        result["game_path_source"] = source
        version_info = read_game_version_info(game_dir)
        result["detected_game_update"] = version_info["update"]
        result["detected_game_revision"] = version_info["revision"]
    except (FileNotFoundError, OSError):
        return result
    try:
        translation = detect_translation_installation(game_dir)
        result["translation_installed"] = translation["installed"]
        result["translation_match_ratio"] = translation["ratio"]
        result["translation_matches_installer"] = translation["matches_current"]
        result["dynamic_date_italian"] = translation.get("date_italian")
        if translation["installed"]:
            result["installed_translation_version"] = recorded_translation_version(game_dir)
        result["translation_slot"] = translation.get("detected_slot")
        result["text_resources_supported"] = translation["texts_supported"]
        result["detected_game_revision"] = effective_game_revision(
            game_dir, result["detected_game_revision"], translation["installed"]
        )
    except (FileNotFoundError, OSError, ValueError, KeyError, zipfile.BadZipFile, json.JSONDecodeError):
        pass
    return result


def print_status_panel(status: dict, colors: bool) -> None:
    manifest = status["manifest"]
    update = status["update"]
    supported = supported_game_updates(manifest)
    supported_revisions = supported_game_revisions(manifest)
    supported_label = ", ".join(supported) or "Non specificata"
    detected = status.get("detected_game_update")
    revision = status.get("detected_game_revision")
    texts_supported = status.get("text_resources_supported")
    game_dir = status.get("game_dir")
    path_source = status.get("game_path_source")
    installed = status.get("translation_installed")
    matches_installer = status.get("translation_matches_installer")
    installed_translation_version = status.get("installed_translation_version")
    dynamic_date_italian = status.get("dynamic_date_italian")
    proposed_translation_version = str(manifest.get("translation_version") or update.get("current") or "0.0.0").lstrip("v")
    current = f"v{str(update.get('current', '0.0.0')).lstrip('v')}"
    latest = str(update.get("latest") or current)

    if detected and str(detected) in supported:
        detected_label = color_text(str(detected), ConsoleColor.CYAN, colors)
    elif detected:
        detected_label = color_text(f"{detected}  ⚠ NON ANCORA VERIFICATA", ConsoleColor.YELLOW, colors)
    else:
        detected_label = color_text("Non rilevata", ConsoleColor.YELLOW, colors)

    if update.get("error"):
        latest_label = color_text("Controllo non disponibile (offline)", ConsoleColor.YELLOW, colors)
    elif update.get("update_available"):
        latest_label = color_text(f"{latest}  ← NUOVA", ConsoleColor.GREEN, colors)
    else:
        latest_label = color_text("Nessuna  ✓ AGGIORNATO", ConsoleColor.GREEN, colors)

    if revision and str(revision).lower() in supported_revisions:
        revision_label = color_text(f"{str(revision)[:12]}…  ✓ VERIFICATA", ConsoleColor.GREEN, colors)
    elif revision:
        revision_label = color_text(f"{str(revision)[:12]}…  ⚠ NUOVA", ConsoleColor.YELLOW, colors)
    else:
        revision_label = color_text("Non rilevata", ConsoleColor.YELLOW, colors)

    if texts_supported is True:
        compatibility_label = color_text("✓ COMPATIBILE", ConsoleColor.GREEN, colors)
    elif texts_supported is False:
        compatibility_label = color_text("✗ NON SUPPORTATA", ConsoleColor.RED, colors)
    else:
        compatibility_label = color_text("? NON VERIFICABILE", ConsoleColor.YELLOW, colors)

    if game_dir:
        if path_source == "automatico":
            path_label = color_text("✓ TROVATO AUTOMATICAMENTE", ConsoleColor.GREEN, colors)
        else:
            path_label = color_text("✓ TROVATO (PERCORSO SALVATO)", ConsoleColor.GREEN, colors)
    else:
        path_label = color_text("✗ NON TROVATO", ConsoleColor.RED, colors)

    if installed is True:
        installed_label = color_text("✓ INSTALLATA (English + accenti)", ConsoleColor.GREEN, colors)
        if installed_translation_version:
            installed_version_label = color_text(
                f"v{str(installed_translation_version).lstrip('v')}", ConsoleColor.CYAN, colors
            )
        else:
            installed_version_label = color_text("Non registrata", ConsoleColor.YELLOW, colors)
        if matches_installer is True:
            content_match_label = color_text(
                "✓ IDENTICI — nessun aggiornamento necessario", ConsoleColor.GREEN, colors
            )
        else:
            content_match_label = color_text(
                "⚠ DIVERSI — AGGIORNAMENTO CONSIGLIATO", ConsoleColor.YELLOW, colors
            )
    elif installed is False:
        installed_label = color_text("✗ NON INSTALLATA", ConsoleColor.YELLOW, colors)
        installed_version_label = color_text("—", ConsoleColor.YELLOW, colors)
        content_match_label = color_text("—", ConsoleColor.YELLOW, colors)
    else:
        installed_label = color_text("? NON VERIFICABILE", ConsoleColor.YELLOW, colors)
        installed_version_label = color_text("? NON VERIFICABILE", ConsoleColor.YELLOW, colors)
        content_match_label = color_text("? NON VERIFICABILE", ConsoleColor.YELLOW, colors)

    proposed_version_label = color_text(f"v{proposed_translation_version}", ConsoleColor.CYAN, colors)
    if dynamic_date_italian is True:
        date_format_label = color_text("✓ ITALIANO (GG/MM/AAAA)", ConsoleColor.GREEN, colors)
    elif dynamic_date_italian is False:
        date_format_label = color_text("⚠ DA AGGIORNARE", ConsoleColor.YELLOW, colors)
    else:
        date_format_label = color_text("? NON VERIFICABILE", ConsoleColor.YELLOW, colors)

    print(color_text("Aniimo - Traduzione Italiana", ConsoleColor.BOLD + ConsoleColor.CYAN, colors))
    print("=" * 58)
    print(f"Percorso del gioco         : {path_label}")
    print(f"Traduzione italiana        : {installed_label}")
    print(f"Versione trad. installata  : {installed_version_label}")
    print(f"Versione trad. proposta    : {proposed_version_label}")
    print(f"Confronto contenuti        : {content_match_label}")
    print(f"Formato date dinamiche     : {date_format_label}")
    print(f"Versione gioco supportata  : {color_text(supported_label, ConsoleColor.CYAN, colors)}")
    print(f"Versione gioco rilevata    : {detected_label}")
    print(f"Revisione hot update       : {revision_label}")
    print(f"Compatibilità testi        : {compatibility_label}")
    print(f"Versione installer attuale : {color_text(current, ConsoleColor.CYAN, colors)}")
    print(f"Nuova versione disponibile : {latest_label}")
    print("=" * 58)
    print("GitHub: https://github.com/Sici29/Aniimo-Italian-Translation")


def show_credits() -> int:
    manifest = local_manifest()
    github_url = str(manifest.get("github_project_url") or "https://github.com/Sici29/Aniimo-Italian-Translation")
    issues_url = str(manifest.get("github_issues_url") or github_url + "/issues")
    support_url = str(manifest.get("support_url") or "https://buymeacoffee.com/sici29")
    print("Aniimo - Traduzione Italiana")
    print("=" * 58)
    print("Progetto e traduzione : Sici29")
    print("GitHub                :", github_url)
    print("Segnala un problema   :", issues_url)
    print("Sostieni il progetto  :", support_url)
    print("=" * 58)
    answer = input("Vuoi aprire la pagina GitHub nel browser? [S/n]: ").strip().lower()
    if answer in {"", "s", "si", "sì", "y", "yes"}:
        webbrowser.open(github_url)
    return 0


def run_menu() -> int:
    colors = enable_console_colors()
    startup = collect_startup_status()
    print_status_panel(startup, colors)
    if not startup.get("game_dir"):
        print()
        print("Aniimo non è stato trovato automaticamente.")
        answer = input("Vuoi indicare adesso la cartella del gioco? [S/n]: ").strip().lower()
        if answer in {"", "s", "si", "sì", "y", "yes"} and configure_game_dir():
            print()
            startup = collect_startup_status()
            print_status_panel(startup, colors)
    update = startup["update"]
    if update.get("update_available"):
        print()
        answer = input("Vuoi aggiornare automaticamente ora? [S/n]: ").strip().lower()
        if answer in {"", "s", "si", "sì", "y", "yes"}:
            class UpdateArgs:
                pass
            result = cmd_update(UpdateArgs())
            if result == UPDATE_SCHEDULED:
                return result
            print()
            print("Puoi continuare con la versione attuale oppure scaricare manualmente la nuova release.")
    print()
    print("1. Installa o aggiorna la traduzione (consigliato)")
    print("2. Ripristina i file originali")
    print("3. Controlla se esiste una nuova versione")
    print("4. Indica o modifica la cartella di Aniimo")
    print("5. Crediti, GitHub e sostieni il progetto")
    print("0. Esci")
    print()
    choice = input("Scelta [Invio = installa]: ").strip() or "1"
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
    if choice == "4":
        return run_menu() if configure_game_dir() else 1
    if choice == "5":
        return show_credits()
    if choice != "1":
        print("Scelta non valida. Riapri l'installer e digita 1, 2, 3, 4, 5 oppure 0.")
        return 1
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


def print_update_complete(previous_version: str | None) -> None:
    colors = enable_console_colors()
    current = str(local_manifest().get("translation_version", "versione nuova"))
    print(color_text("✓ AGGIORNAMENTO COMPLETATO", ConsoleColor.BOLD + ConsoleColor.GREEN, colors))
    if previous_version:
        print(f"Versione precedente : v{previous_version.lstrip('v')}")
    print(f"Versione attuale    : v{current.lstrip('v')}")
    print("L'installer è stato riavviato automaticamente.")
    print()


def main() -> int:
    menu_mode = len(sys.argv) == 1
    if menu_mode:
        if not acquire_installer_instance_lock():
            print("L'installer è già aperto in un'altra finestra.")
            print("Chiudi l'altra finestra prima di riaprirlo.")
            pause_if_needed(True)
            return 4
        cleanup_update_cache()
        code = run_menu()
        if code == UPDATE_SCHEDULED:
            return 0
        pause_if_needed(True)
        return code

    if sys.argv[1] == UPDATE_COMPLETE_COMMAND:
        if not acquire_installer_instance_lock():
            print("Aggiornamento completato, ma un'altra finestra dell'installer è ancora aperta.")
            print("Chiudila e riapri normalmente l'installer aggiornato.")
            pause_if_needed(True)
            return 4
        cleanup_update_cache()
        previous_version = sys.argv[2] if len(sys.argv) > 2 else None
        print_update_complete(previous_version)
        code = run_menu()
        if code == UPDATE_SCHEDULED:
            return 0
        pause_if_needed(True)
        return code

    if sys.argv[1] == UPDATE_APPLY_COMMAND:
        internal = argparse.ArgumentParser(add_help=False)
        internal.add_argument(UPDATE_APPLY_COMMAND)
        internal.add_argument("--target-exe", required=True)
        internal.add_argument("--previous-version", default="")
        try:
            return cmd_apply_update(internal.parse_args())
        except Exception:
            return 1

    parser = argparse.ArgumentParser(description="Aniimo Italian Translation installer")
    sub = parser.add_subparsers(dest="command", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--game-dir", help="Aniimo game folder")
    common.add_argument("--force", action="store_true", help="Install even if the game text version is unknown")
    common.add_argument("--no-update-check", action="store_true", help="Skip GitHub update check")
    check = sub.add_parser("check", parents=[common], help="Check compatibility")
    check.set_defaults(func=cmd_check)
    install = sub.add_parser("install", parents=[common], help="Install Italian translation")
    install.add_argument("--target", default="en", choices=["en"], help="Language slot used by the Italian translation")
    install.add_argument("--also-english", action="store_true", help=argparse.SUPPRESS)
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
        print("Errore:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
