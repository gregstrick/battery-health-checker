# Battery Health Checker

A desktop app for a phone resale/refurb business: plug in an iPhone or iPad over USB and
instantly see its battery health %, cycle count, storage size, serial number, and activation
state — no button to press, no manual lookup. Every test logs automatically to an Excel file
with duplicate detection, plus a manual QC checklist (screen, cameras, speakers, buttons, Wi-Fi)
and a cosmetic grade (A/B/C/D) you can set per device.

Download it: **https://gregstrick.github.io/battery-health-checker/**

## How it works

There's no public Apple API for battery health. This reads the same low-level USB diagnostics
channel that tools like 3uTools use — `idevicediagnostics ioregentry AppleSmartBattery` (or
`AppleARMPMUCharger` on older devices, iPhone 8 and earlier) via the open-source
[libimobiledevice](https://libimobiledevice.org/) project — and computes
`health % = AppleRawMaxCapacity / DesignCapacity`, the same math Apple's own Settings > Battery
Health screen uses. See `src/main.py` for the full implementation.

Supports 121 iPhone/iPad/iPod touch models, 2016 and newer (see `PRODUCT_NAMES` in `src/main.py`).

## Project layout

- `src/main.py` — the whole app (Tkinter GUI + USB diagnostics + Excel/JSON logging)
- `setup.py` — builds the macOS `.app` via py2app
- `windows/`, `windows-arm64/` — bundled libimobiledevice binaries + PyInstaller build scripts
  for Windows x64 and Windows ARM64 (see `WINDOWS_SETUP.md` for manual builds)
- `.github/workflows/build-windows.yml` — builds both Windows variants on GitHub-hosted runners
  and uploads them to a release (no physical Windows hardware needed — see below)
- `docs/` — the download website (GitHub Pages, served from this folder)
- `CHANGELOG.md` — version history

## Building a new release

1. Bump `VERSION` in `src/main.py` and the matching version strings in `setup.py`
2. Add an entry to `CHANGELOG.md`
3. Build the Mac app:
   ```
   rm -rf build dist "Battery Health Checker.app"
   ./.venv/bin/python3 setup.py py2app
   mv "dist/Battery Health Checker.app" "Battery Health Checker.app"
   codesign --force --deep --sign - "Battery Health Checker.app"
   xattr -cr "Battery Health Checker.app"
   ```
4. Zip it (`ditto -c -k --sequesterRsrc "Battery Health Checker.app" BatteryHealthChecker-macOS.zip`)
   and create a GitHub release with that zip attached:
   ```
   gh release create vX.X.X BatteryHealthChecker-macOS.zip --title "vX.X.X" --notes "..."
   ```
5. Trigger the Windows builds (builds both x64 and ARM64 on real GitHub-hosted Windows runners,
   uploads straight to the release — takes about a minute, no Windows machine needed):
   ```
   gh workflow run build-windows.yml -f release_tag=vX.X.X
   ```
6. The download site at `docs/index.html` picks up the new release automatically — nothing to
   edit there.

The app has a built-in update checker (checks GitHub releases on startup) that shows a footer
notice when a newer version is available.

## Local data (not in this repo)

`device_log.json` and `Device Log.xlsx` — the actual customer/device test history — are
deliberately excluded from git (see `.gitignore`) since they contain real business data. They
live only on whichever Mac/PC ran the tests. **Back these up separately** (e.g. Time Machine,
copying to cloud storage) — losing the machine means losing that data, since it was never pushed
anywhere.

## Known limitations

- Activation Lock (Find My) status can't be checked via USB once a device is past Setup
  Assistant — there's no local diagnostics key for it. See commit history / chat context for why.
- Windows and Mac each keep a fully separate log; they don't sync.
- The app is unsigned (no Apple Developer or Windows code-signing certificate), so first launch
  on a new machine shows a one-time Gatekeeper/SmartScreen warning.
