# QA Report — Aniimo Italian Translation 1.0.3887621.0

- **Game Update**: Steam build 3887621 (patch 1.0.3887621.0)
- **Catalog Size**: 134,298 keys (100.00% translated, 0 fallbacks)
- **Keys SHA-256**: `dbae2601ea1d6e0abde970e054817d08090e02b55f449e0b569913492d610a04`
- **Content SHA-256**: `0f3d7e47b74408e1932d4e141caf1377c180128b526ad3d6ccce279e092fcaea`
- **Tested Game Revision**: `cbb043ba22d8341fe16379dd8d311287`
- **Tested Archive SHA-256**: `bb4d397fb46eed94be66bfababbcccbb19759a7ca9a72914d7aba7c9e9580e9a`
- **Features Tested**:
  - Live installation on Steam build 3887621 (`D:\SteamLibrary\steamapps\common\Aniimo`) with 0 fallbacks across 134,298 keys
  - Target slot selection (13 language slots verified)
  - Native font compatibility and bundle validation
  - Non-Steam / Pawprint explicit warning prompt and status panel detection
  - Patcher sync guard and cache consistency (`LuaCacheVer.txt` synchronized)
  - Backup & restore integrity
- **Unit Tests**: 161/161 passed (OK, skipped=42)
- **Standalone EXE**: Compilato con PyInstaller 6.22.3 (`Aniimo-Italian-Translation.exe`)
