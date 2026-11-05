# QA Report — Aniimo Italian Translation 1.0.3880756.0

- **Game Update**: Steam build 3880756 (patch 1.0.3880756.0)
- **Catalog Size**: 134,297 keys (100.00% translated, 0 fallbacks)
- **Keys SHA-256**: `02aff83605cb15785a23bf3781deb9f8570b3d71ab813c86e00b89fded2063f6`
- **Content SHA-256**: `6d5bf9d7c94be72eaae37b3cfdb588116cf7fc0709922d1df02817ec6c6880a6`
- **Tested Game Revision**: `276d62ee68ca471ed00f50cf909764c1`
- **Tested Archive SHA-256**: `071dcaf126a956963af7d4947a61795c1cbe5d221236f17680964368573510c2`
- **Features Tested**:
  - Live installation on Steam build 3880756 (`D:\SteamLibrary\steamapps\common\Aniimo`) with 0 fallbacks across 134,297 keys
  - Target slot selection (13 language slots verified)
  - Native font compatibility and bundle validation
  - Non-Steam / Pawprint explicit warning prompt and status panel detection
  - Patcher sync guard and cache consistency (`LuaCacheVer.txt` synchronized)
  - Backup & restore integrity
- **Unit Tests**: 161/161 passed (OK, skipped=42)
- **Standalone EXE**: Compilato con PyInstaller 6.22.3 (`Aniimo-Italian-Translation.exe`)
