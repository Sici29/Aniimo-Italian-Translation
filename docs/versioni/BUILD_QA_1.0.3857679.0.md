# QA Report — Aniimo Italian Translation 1.0.3857679.0

- **Game Update**: Steam build 3857679 (patch 1.0.3857679.0)
- **Catalog Size**: 134,274 keys (100.00% translated, 0 fallbacks)
- **Keys SHA-256**: `54d6e40c8ee1b127a9ea27518a4b4c065e58b5fa60c21e02af4395c2389de05f`
- **Content SHA-256**: `017c1ba4285b736e6eeb24f2b1d75c873ef4d122e1e075be8df2bf6ef8fef56f`
- **Tested Game Revision**: `1aee0f9e145c04155f700465d7a53a19`
- **Tested Archive SHA-256**: `519416b2603bd5b6e8836a81fb6aa32e458fb8482025c47602bb8bc2ea5f250c`
- **Features Tested**:
  - Live installation on Steam build 3857679 (`D:\SteamLibrary\steamapps\common\Aniimo`) with 0 fallbacks across 134,274 keys
  - Target slot selection (13 language slots verified)
  - Native font compatibility and bundle validation
  - Non-Steam / Pawprint explicit warning prompt and status panel detection
  - Patcher sync guard and cache consistency (`LuaCacheVer.txt` synchronized)
  - Backup & restore integrity
- **Unit Tests**: 161/161 passed (OK, skipped=42)
- **Standalone EXE**: Compilato con PyInstaller 6.22.3 (`Aniimo-Italian-Translation.exe`)
