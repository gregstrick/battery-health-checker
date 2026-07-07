@echo off
setlocal
cd /d "%~dp0"
cd ..

echo === Battery Health Checker - Windows ARM64 Build ===
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python not found on PATH. Install the ARM64 build from https://www.python.org/downloads/windows
    echo (look for "Windows arm64" under the latest release^) and check "Add python.exe to PATH".
    pause
    exit /b 1
)

python -c "import platform; exit(0 if platform.machine().lower() in ('arm64','aarch64') else 1)"
if errorlevel 1 (
    echo WARNING: This Python does not report as ARM64 ^(it may be the x64 build running under emulation^).
    echo For a native ARM64 .exe, install the ARM64 Python build from python.org.
    echo Continuing anyway...
)

if not exist ".venv-windows-arm64" (
    echo Creating virtual environment...
    python -m venv .venv-windows-arm64
)

call .venv-windows-arm64\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip >nul
pip install -r windows-arm64\requirements.txt
if errorlevel 1 (
    echo ERROR: pip install failed. See errors above.
    pause
    exit /b 1
)

echo.
echo Building standalone .exe...
pyinstaller --noconfirm --windowed --onefile ^
    --name "Battery Health Checker" ^
    --icon "windows-arm64\AppIcon.ico" ^
    --add-data "windows-arm64\bin;bin" ^
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
