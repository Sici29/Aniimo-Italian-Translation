# QA Report — Aniimo Italian Translation 1.0.3629693.0

- **Game Update**: Steam build 3629693 (patch 1.0.3629693.0)
- **Catalog Size**: 112,263 keys (100.00% translated, 0 fallbacks)
- **Keys SHA-256**: `08b42c1b88f0d0fc1c56a54336057405eccf59f5edbeef18eb30d400b81438c8`
- **Content SHA-256**: `e2fe7ca089c8b3771f239e8d6d6cefdc66bb27c51085b73ba8ae8b4ec6bf2083`
- **Tested Game Revision**: `cf5ae0c5b1f8eca44ce5b4471ff26e7c`
- **Tested Archive SHA-256**: `8bd720edcabe307b282c096745764bfa2643f9bc9a172980b5b8e3d04786ea3f`
- **Features Tested**:
  - Live installation on Steam build 3629693 (`D:\SteamLibrary\steamapps\common\Aniimo`)
  - Target slot selection (13 language slots verified)
  - Non-Steam / Pawprint explicit warning prompt and status panel detection
  - Patcher sync guard fix (resolved false positive lock when primary cvs cache is current)
  - Interactive force option for pending cvs updates
  - Backup & restore integrity
- **Unit Tests**: 161/161 passed (OK, skipped=42)
- **Standalone EXE**: Compilato con PyInstaller 6.22.3 (`Aniimo-Italian-Translation.exe`)
