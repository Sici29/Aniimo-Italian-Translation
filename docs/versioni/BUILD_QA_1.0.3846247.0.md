# QA Report — Aniimo Italian Translation 1.0.3846247.0

- **Game Update**: Steam build 3846247 (patch 1.0.3846247.0) — Autumn Wonderfest & Halloween Update
- **Catalog Size**: 134,277 keys (100.00% translated, 0 fallbacks)
- **Keys SHA-256**: `aaed789b568d71d71e9d952ead414ec5b5a06ddd53cbb92cd04e6eb3fc33fd89`
- **Content SHA-256**: `d9b935cc95e21e410e68881288dac3c9f0bfe3edbef56c5fc0597115e73546f7`
- **Tested Game Revision**: `d6872862df8fe7a4edabad5ab1e3b46f`
- **Tested Archive SHA-256**: `9c0fa7f5547a06b2cbafa7aaf1f588c29874a37e4e0943dd075b6639aed4f91d`
- **Features Tested**:
  - Live installation on Steam build 3846247 (`D:\SteamLibrary\steamapps\common\Aniimo`) with 0 fallbacks across 134,277 keys
  - Target slot selection (13 language slots verified)
  - Native font compatibility and bundle validation
  - Non-Steam / Pawprint explicit warning prompt and status panel detection
  - Patcher sync guard and cache consistency (`LuaCacheVer.txt` synchronized)
  - Backup & restore integrity
- **Unit Tests**: 161/161 passed (OK, skipped=42)
- **Standalone EXE**: Compilato con PyInstaller 6.22.3 (`Aniimo-Italian-Translation.exe`)
