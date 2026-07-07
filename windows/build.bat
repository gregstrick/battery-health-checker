@echo off
setlocal
cd /d "%~dp0"
cd ..

echo === Battery Health Checker - Windows Build ===
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python not found on PATH. Install it from https://www.python.org/downloads/
    echo Make sure to check "Add python.exe to PATH" during install, then re-run this script.
    pause
    exit /b 1
)

if not exist ".venv-windows" (
    echo Creating virtual environment...
    python -m venv .venv-windows
)

call .venv-windows\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip >nul
pip install -r windows\requirements.txt
if errorlevel 1 (
    echo ERROR: pip install failed. See errors above.
    pause
    exit /b 1
)

echo.
echo Building standalone .exe...
pyinstaller --noconfirm --windowed --onefile ^
    --name "Battery Health Checker" ^
    --icon "windows\AppIcon.ico" ^
    --add-data "windows\bin;bin" ^
    src\main.py

if errorlevel 1 (
    echo ERROR: Build failed. See errors above.
    pause
    exit /b 1
)

echo.
echo ===================================================
echo Build complete!
echo Your app is at: dist\Battery Health Checker.exe
echo Move it wherever you like (Desktop, etc.) and pin it
echo to the taskbar. Its log files (Device Log.xlsx,
echo device_log.json) will be created next to it the
echo first time you run it.
echo ===================================================
pause
