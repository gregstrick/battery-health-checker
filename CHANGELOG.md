# Changelog

## v1.2.0
- Reliability: log writes are now crash-safe (atomic write-then-rename for both the JSON and Excel files)
- Reliability: if Device Log.xlsx is open in Excel when a test completes, the app no longer fails silently — the test still saves correctly to the JSON source of truth, and the footer shows a clear red warning to close Excel
- Reliability: if the USB diagnostics tools are missing or broken, the app now shows a clear "SETUP ERROR" state instead of silently hanging on "Waiting for iPad" forever
- Reliability: plugging in two devices at once now shows an explicit "connect one at a time" message instead of arbitrarily picking one
- QoL: audible chime when a device is detected, so you don't have to watch the screen during rapid back-to-back testing

## v1.1.0
- In-app update checker: checks GitHub releases on startup, shows a clickable notice in the footer when a newer version is available
- Website redesign: proper platform icons (replacing emoji), features section, auto-highlights your detected platform, Open Graph tags for link previews
- Version number now shown in the app footer

## v1.0.0
- Initial release
- Instant battery health %, cycle count, capacity, serial number, and storage size on USB connect
- Support for 121 iPhone/iPad/iPod touch models (2016 and newer)
- Manual QC checklist (screen, cameras, speakers, microphone, buttons, Wi-Fi) saved per device
- Excel + JSON logging with automatic duplicate detection ("already tested" badge)
- Cosmetic grade selector (A/B/C/D)
- Standalone Mac app (custom icon, Dock-ready)
- Windows x64 and Windows ARM64 build tooling (bundled libimobiledevice binaries + PyInstaller scripts)
