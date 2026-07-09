@echo off
setlocal
cd /d "%~dp0"

if exist "tools\AniimoItalianInstaller.exe" (
  "tools\AniimoItalianInstaller.exe" restore %*
  pause
  exit /b %ERRORLEVEL%
)

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3 "tools\aniimo_it_installer.py" restore %*
  pause
  exit /b %ERRORLEVEL%
)

where python >nul 2>nul
if %ERRORLEVEL%==0 (
  python "tools\aniimo_it_installer.py" restore %*
  pause
  exit /b %ERRORLEVEL%
)

echo Python non trovato.
echo Scarica la release con eseguibile oppure installa Python 3.
pause
exit /b 1
