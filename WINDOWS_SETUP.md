# Battery Health Checker — Windows Setup

Everything needed to build the Windows version is already in this folder — `windows/bin` (Intel/AMD
64-bit PCs) and `windows-arm64/bin` (Windows-on-ARM, e.g. Surface Pro X, Snapdragon laptops) both
have the USB diagnostics tools already bundled, pulled from the official MSYS2 build of
libimobiledevice — same library the Mac version uses, just compiled for Windows. You just need to
run the build once, on each machine type.

## 1. Install Apple's USB driver

Windows needs Apple's driver to talk to an iPad over USB at all. Install **iTunes** from
https://www.apple.com/itunes/download/win64 (the classic installer, not the Microsoft Store
version) — this installs "Apple Mobile Device Support" in the background, which is the actual
piece that matters. You don't need to ever open iTunes itself afterward.

## 2. Install Python

Download Python from https://www.python.org/downloads/windows.
- **On a regular Intel/AMD PC:** get the standard 64-bit installer.
- **On Windows-on-ARM:** look for the "Windows arm64" installer under the latest release, so you
  get a genuinely native ARM64 build instead of running under x64 emulation.

**During install, check the box "Add python.exe to PATH"** — this is important, the build script
depends on it.

## 3. Copy this whole "Battery Health Checker" folder to the Windows machine

USB drive, cloud sync, email — however's easiest. Keep the folder structure intact (`src/`,
`windows/`, `windows-arm64/`, etc. all need to stay together).

## 4. Run the build

- **Regular Windows PC:** open the `windows` folder and double-click **build.bat**.
- **Windows-on-ARM:** open the `windows-arm64` folder and double-click **build.bat** instead.

A black command-prompt window will open and do everything automatically: create a Python
environment, install dependencies (openpyxl, PyInstaller), and compile the app into a single
`.exe`. This takes a couple minutes.

If it succeeds, you'll see:
```
Build complete!
Your app is at: dist\Battery Health Checker.exe
```

## 5. Move and use the app

Move `dist\Battery Health Checker.exe` wherever you want it to live long-term (Desktop, a
dedicated folder, etc.) — its log files (`Device Log.xlsx`, `device_log.json`) will be created
right next to it the first time you run it, so pick a permanent spot before you start logging
real devices. Pin it to the taskbar for quick access.

## 6. First-time device trust

Exactly like on the Mac: the first time you plug in each physical iPhone/iPad, it'll ask you to
tap **Trust** on the device's screen and enter its passcode. After that one-time step, that same
device connects instantly on this PC with no prompts.

## Important: every machine keeps its own separate log

The Mac app, the Windows x64 build, and the Windows ARM64 build each keep their own
`Device Log.xlsx` / `device_log.json` — none of them sync with each other. That means:
- Device IDs (001, 002, 003...) are numbered independently on each machine.
- If the same physical device gets tested on two different machines, it'll show up as "new" on
  whichever one hasn't seen it before, potentially with a different Device ID on each.

If you regularly switch between machines and want one single combined log, let me know — it's
doable (e.g., by pointing all machines at a synced folder like Dropbox/OneDrive) but it's a real
design change, not something to bolt on silently.

## If something breaks

Most likely culprits, in order:
1. **"No devices found" / app doesn't detect the device** — Apple Mobile Device Support isn't
   installed or the service isn't running. Reinstall iTunes, then restart the PC.
2. **build.bat fails at the "pip install" step** — Python wasn't added to PATH. Reinstall Python
   and check that box, or run `python -m pip --version` in Command Prompt to confirm it works.
3. **On ARM64, the build.bat warns your Python isn't ARM64** — you likely installed the regular
   x64 Python installer. Uninstall it and get the "Windows arm64" installer from python.org instead.
4. **Windows SmartScreen blocks the .exe on first run** — click "More info" then "Run anyway".
   This happens because the app isn't code-signed with a paid Microsoft certificate (normal for
   an internal tool like this).

Send me whatever error text shows up and I can help from there, even without being on the machine
myself.
