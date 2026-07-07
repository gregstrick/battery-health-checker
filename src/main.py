#!/usr/bin/env python3
import json
import plistlib
import shutil
import subprocess
import sys
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import font as tkfont

from openpyxl import Workbook

IS_WINDOWS = sys.platform == "win32"


def frozen_exe_dir():
    """Directory holding the actual double-clicked executable (or this script)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def bundled_bin_dir():
    """Directory holding bundled idevice_id/ideviceinfo/idevicediagnostics binaries."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "bin"
    return frozen_exe_dir() / "bin"


def find_binary(name):
    exe_name = f"{name}.exe" if IS_WINDOWS else name
    bundled = bundled_bin_dir() / exe_name
    if bundled.exists():
        return str(bundled)
    found = shutil.which(exe_name)
    if found:
        return found
    if not IS_WINDOWS:
        return f"/opt/homebrew/bin/{name}"
    return exe_name


IDEVICE_ID = find_binary("idevice_id")
IDEVICEINFO = find_binary("ideviceinfo")
IDEVICEDIAGNOSTICS = find_binary("idevicediagnostics")

POLL_MS = 1500

PRODUCT_NAMES = {
    # iPhone (2016 and newer)
    "iPhone8,4": "iPhone SE (1st generation)",
    "iPhone9,1": "iPhone 7",
    "iPhone9,2": "iPhone 7 Plus",
    "iPhone9,3": "iPhone 7",
    "iPhone9,4": "iPhone 7 Plus",
    "iPhone10,1": "iPhone 8",
    "iPhone10,2": "iPhone 8 Plus",
    "iPhone10,3": "iPhone X",
    "iPhone10,4": "iPhone 8",
    "iPhone10,5": "iPhone 8 Plus",
    "iPhone10,6": "iPhone X",
    "iPhone11,2": "iPhone XS",
    "iPhone11,4": "iPhone XS Max",
    "iPhone11,6": "iPhone XS Max",
    "iPhone11,8": "iPhone XR",
    "iPhone12,1": "iPhone 11",
    "iPhone12,3": "iPhone 11 Pro",
    "iPhone12,5": "iPhone 11 Pro Max",
    "iPhone12,8": "iPhone SE (2nd generation)",
    "iPhone13,1": "iPhone 12 Mini",
    "iPhone13,2": "iPhone 12",
    "iPhone13,3": "iPhone 12 Pro",
    "iPhone13,4": "iPhone 12 Pro Max",
    "iPhone14,2": "iPhone 13 Pro",
    "iPhone14,3": "iPhone 13 Pro Max",
    "iPhone14,4": "iPhone 13 Mini",
    "iPhone14,5": "iPhone 13",
    "iPhone14,6": "iPhone SE (3rd generation)",
    "iPhone14,7": "iPhone 14",
    "iPhone14,8": "iPhone 14 Plus",
    "iPhone15,2": "iPhone 14 Pro",
    "iPhone15,3": "iPhone 14 Pro Max",
    "iPhone15,4": "iPhone 15",
    "iPhone15,5": "iPhone 15 Plus",
    "iPhone16,1": "iPhone 15 Pro",
    "iPhone16,2": "iPhone 15 Pro Max",
    "iPhone17,1": "iPhone 16 Pro",
    "iPhone17,2": "iPhone 16 Pro Max",
    "iPhone17,3": "iPhone 16",
    "iPhone17,4": "iPhone 16 Plus",
    "iPhone17,5": "iPhone 16e",
    "iPhone18,1": "iPhone 17 Pro",
    "iPhone18,2": "iPhone 17 Pro Max",
    "iPhone18,3": "iPhone 17",
    "iPhone18,4": "iPhone Air",
    "iPhone18,5": "iPhone 17e",

    # iPod touch (2016 and newer)
    "iPod9,1": "iPod touch (7th generation)",

    # iPad (2016 and newer)
    "iPad6,3": "iPad Pro (9.7-inch), Wi-Fi",
    "iPad6,4": "iPad Pro (9.7-inch), Wi-Fi + Cellular",
    "iPad6,7": "iPad Pro (12.9-inch, 1st generation), Wi-Fi",
    "iPad6,8": "iPad Pro (12.9-inch, 1st generation), Wi-Fi + Cellular",
    "iPad6,11": "iPad (5th generation), Wi-Fi",
    "iPad6,12": "iPad (5th generation), Wi-Fi + Cellular",
    "iPad7,1": "iPad Pro (12.9-inch, 2nd generation), Wi-Fi",
    "iPad7,2": "iPad Pro (12.9-inch, 2nd generation), Wi-Fi + Cellular",
    "iPad7,3": "iPad Pro (10.5-inch), Wi-Fi",
    "iPad7,4": "iPad Pro (10.5-inch), Wi-Fi + Cellular",
    "iPad7,5": "iPad (6th generation), Wi-Fi",
    "iPad7,6": "iPad (6th generation), Wi-Fi + Cellular",
    "iPad7,11": "iPad (7th generation), Wi-Fi",
    "iPad7,12": "iPad (7th generation), Wi-Fi + Cellular",
    "iPad8,1": "iPad Pro (11-inch, 1st generation), Wi-Fi",
    "iPad8,2": "iPad Pro (11-inch, 1st generation, 1TB), Wi-Fi",
    "iPad8,3": "iPad Pro (11-inch, 1st generation), Wi-Fi + Cellular",
    "iPad8,4": "iPad Pro (11-inch, 1st generation, 1TB), Wi-Fi + Cellular",
    "iPad8,5": "iPad Pro (12.9-inch, 3rd generation), Wi-Fi",
    "iPad8,6": "iPad Pro (12.9-inch, 3rd generation, 1TB), Wi-Fi",
    "iPad8,7": "iPad Pro (12.9-inch, 3rd generation), Wi-Fi + Cellular",
    "iPad8,8": "iPad Pro (12.9-inch, 3rd generation, 1TB), Wi-Fi + Cellular",
    "iPad8,9": "iPad Pro (11-inch, 2nd generation), Wi-Fi",
    "iPad8,10": "iPad Pro (11-inch, 2nd generation), Wi-Fi + Cellular",
    "iPad8,11": "iPad Pro (12.9-inch, 4th generation), Wi-Fi",
    "iPad8,12": "iPad Pro (12.9-inch, 4th generation), Wi-Fi + Cellular",
    "iPad11,1": "iPad mini (5th generation), Wi-Fi",
    "iPad11,2": "iPad mini (5th generation), Wi-Fi + Cellular",
    "iPad11,3": "iPad Air (3rd generation), Wi-Fi",
    "iPad11,4": "iPad Air (3rd generation), Wi-Fi + Cellular",
    "iPad11,6": "iPad (8th generation), Wi-Fi",
    "iPad11,7": "iPad (8th generation), Wi-Fi + Cellular",
    "iPad12,1": "iPad (9th generation), Wi-Fi",
    "iPad12,2": "iPad (9th generation), Wi-Fi + Cellular",
    "iPad13,1": "iPad Air (4th generation), Wi-Fi",
    "iPad13,2": "iPad Air (4th generation), Wi-Fi + Cellular",
    "iPad13,4": "iPad Pro (11-inch, 3rd generation), Wi-Fi",
    "iPad13,5": "iPad Pro (11-inch, 3rd generation), Wi-Fi",
    "iPad13,6": "iPad Pro (11-inch, 3rd generation), Wi-Fi + Cellular",
    "iPad13,7": "iPad Pro (11-inch, 3rd generation), Wi-Fi + Cellular",
    "iPad13,8": "iPad Pro (12.9-inch, 5th generation), Wi-Fi",
    "iPad13,9": "iPad Pro (12.9-inch, 5th generation), Wi-Fi",
    "iPad13,10": "iPad Pro (12.9-inch, 5th generation), Wi-Fi + Cellular",
    "iPad13,11": "iPad Pro (12.9-inch, 5th generation), Wi-Fi + Cellular",
    "iPad13,16": "iPad Air (5th generation), Wi-Fi",
    "iPad13,17": "iPad Air (5th generation), Wi-Fi + Cellular",
    "iPad13,18": "iPad (10th generation), Wi-Fi",
    "iPad13,19": "iPad (10th generation), Wi-Fi + Cellular",
    "iPad14,1": "iPad mini (6th generation), Wi-Fi",
    "iPad14,2": "iPad mini (6th generation), Wi-Fi + Cellular",
    "iPad14,3": "iPad Pro (11-inch, 4th generation), Wi-Fi",
    "iPad14,4": "iPad Pro (11-inch, 4th generation), Wi-Fi + Cellular",
    "iPad14,5": "iPad Pro (12.9-inch, 6th generation), Wi-Fi",
    "iPad14,6": "iPad Pro (12.9-inch, 6th generation), Wi-Fi + Cellular",
    "iPad14,8": "iPad Air 11-inch (6th generation), Wi-Fi",
    "iPad14,9": "iPad Air 11-inch (6th generation), Wi-Fi + Cellular",
    "iPad14,10": "iPad Air 13-inch (6th generation), Wi-Fi",
    "iPad14,11": "iPad Air 13-inch (6th generation), Wi-Fi + Cellular",
    "iPad15,3": "iPad Air 11-inch (7th generation), Wi-Fi",
    "iPad15,4": "iPad Air 11-inch (7th generation), Wi-Fi + Cellular",
    "iPad15,5": "iPad Air 13-inch (7th generation), Wi-Fi",
    "iPad15,6": "iPad Air 13-inch (7th generation), Wi-Fi + Cellular",
    "iPad15,7": "iPad (11th generation), Wi-Fi",
    "iPad15,8": "iPad (11th generation), Wi-Fi + Cellular",
    "iPad16,1": "iPad mini (7th generation), Wi-Fi",
    "iPad16,2": "iPad mini (7th generation), Wi-Fi + Cellular",
    "iPad16,3": "iPad Pro (11-inch, 5th generation), Wi-Fi",
    "iPad16,4": "iPad Pro (11-inch, 5th generation), Wi-Fi + Cellular",
    "iPad16,5": "iPad Pro (12.9-inch, 7th generation), Wi-Fi",
    "iPad16,6": "iPad Pro (12.9-inch, 7th generation), Wi-Fi + Cellular",
    "iPad16,8": "iPad Air 11-inch (8th generation), Wi-Fi",
    "iPad16,9": "iPad Air 11-inch (8th generation), Wi-Fi + Cellular",
    "iPad16,10": "iPad Air 13-inch (8th generation), Wi-Fi",
    "iPad16,11": "iPad Air 13-inch (8th generation), Wi-Fi + Cellular",
}

COMMON_STORAGE_SIZES_GB = [16, 32, 64, 128, 256, 512, 1024, 2048]

CHECK_ITEMS = [
    "Touch Screen / Digitizer",
    "Home Button / Touch ID",
    "Volume Buttons",
    "Front Camera",
    "Rear Camera",
    "Speakers",
    "Microphone",
    "Wi-Fi",
]

GRADE_OPTIONS = [
    ("A", "Like New"),
    ("B", "Good"),
    ("C", "Fair"),
    ("D", "Poor"),
]

if IS_WINDOWS:
    DATA_DIR = frozen_exe_dir()
else:
    DATA_DIR = Path("/Users/gstrick/Battery Health Checker")
LOG_JSON = DATA_DIR / "device_log.json"
LOG_XLSX = DATA_DIR / "Device Log.xlsx"

XLSX_HEADERS = [
    "Device ID", "Serial Number", "Model", "Storage", "Activation State", "Battery Health %",
    "Cycle Count", "Design Capacity (mAh)", "Raw Max Capacity (mAh)", "Cosmetic Grade",
    "First Tested", "Last Tested", "All Functions Checked",
] + CHECK_ITEMS

BG = "#1c1c1e"
CARD_BG = "#2c2c2e"
FG_MAIN = "#f2f2f7"
FG_DIM = "#8e8e93"
GREEN = "#30d158"
ORANGE = "#ff9f0a"
RED = "#ff453a"
BLUE = "#0a84ff"


def run(cmd):
    kwargs = {}
    if IS_WINDOWS:
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, **kwargs)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def get_udid():
    _, out, _ = run([IDEVICE_ID, "-l"])
    udids = [line.strip() for line in out.splitlines() if line.strip()]
    return udids[0] if udids else None


def get_device_info(udid):
    code, out, err = run([IDEVICEINFO, "-u", udid])
    info = {}
    for line in out.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            info[key.strip()] = value.strip()
    return info, code, err


def get_storage_gb(udid):
    code, out, err = run([IDEVICEINFO, "-u", udid, "-q", "com.apple.disk_usage"])
    if code != 0:
        return None
    for line in out.splitlines():
        if line.startswith("TotalDiskCapacity:"):
            try:
                total_bytes = int(line.split(":", 1)[1].strip())
            except ValueError:
                return None
            raw_gb = total_bytes / 1_000_000_000
            return min(COMMON_STORAGE_SIZES_GB, key=lambda gb: abs(gb - raw_gb))
    return None


def get_battery_data(udid):
    last_err = ""
    for key in ("AppleSmartBattery", "AppleARMPMUCharger"):
        code, out, err = run([IDEVICEDIAGNOSTICS, "-u", udid, "ioregentry", key])
        last_err = err
        if code == 0 and out.strip():
            try:
                data = plistlib.loads(out.encode())
            except Exception:
                continue
            data = data.get("IORegistry", data) if isinstance(data, dict) else data
            if data:
                return data, None
    return None, last_err


def battery_health_percent(battery):
    design = battery.get("DesignCapacity")
    raw_max = battery.get("AppleRawMaxCapacity")
    if not design or not raw_max:
        return None
    return min(round((raw_max / design) * 100), 100)


class DeviceLog:
    """Local JSON store of every serial ever tested, mirrored out to an Excel file."""

    def __init__(self):
        self.records = {}
        if LOG_JSON.exists():
            try:
                self.records = json.loads(LOG_JSON.read_text())
            except Exception:
                self.records = {}
        self._migrate_device_ids()

    def _migrate_device_ids(self):
        needs_renumber = any(not entry["device_id"].isdigit() for entry in self.records.values())
        if not needs_renumber:
            return
        ordered = sorted(self.records.values(), key=lambda e: e.get("first_tested", ""))
        for i, entry in enumerate(ordered, start=1):
            entry["device_id"] = f"{i:03d}"
        self._save()

    def next_device_id(self):
        return f"{len(self.records) + 1:03d}"

    def record_test(self, serial, model, storage, activation_state, pct, cycle_count, design, raw_max):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        is_new = serial not in self.records
        if is_new:
            entry = {
                "device_id": self.next_device_id(),
                "serial": serial,
                "model": model,
                "storage": storage,
                "activation_state": activation_state,
                "health_pct": pct,
                "cycle_count": cycle_count,
                "design_capacity": design,
                "raw_max_capacity": raw_max,
                "cosmetic_grade": None,
                "first_tested": now,
                "last_tested": now,
                "checks": {item: False for item in CHECK_ITEMS},
            }
            self.records[serial] = entry
        else:
            entry = self.records[serial]
            entry.update(model=model, storage=storage, activation_state=activation_state, health_pct=pct,
                         cycle_count=cycle_count, design_capacity=design, raw_max_capacity=raw_max, last_tested=now)
            entry.setdefault("cosmetic_grade", None)
            entry.setdefault("checks", {item: False for item in CHECK_ITEMS})
            for item in CHECK_ITEMS:
                entry["checks"].setdefault(item, False)
        self._save()
        return entry, is_new

    def set_check(self, serial, item, value):
        entry = self.records.get(serial)
        if not entry:
            return
        entry.setdefault("checks", {})[item] = value
        self._save()

    def set_grade(self, serial, grade):
        entry = self.records.get(serial)
        if not entry:
            return
        entry["cosmetic_grade"] = grade
        self._save()

    def _save(self):
        LOG_JSON.write_text(json.dumps(self.records, indent=2))
        self._write_xlsx()

    def _write_xlsx(self):
        wb = Workbook()
        ws = wb.active
        ws.title = "Devices"
        ws.append(XLSX_HEADERS)
        for entry in sorted(self.records.values(), key=lambda e: e["device_id"]):
            checks = entry.get("checks", {})
            all_checked = all(checks.get(item) for item in CHECK_ITEMS)
            ws.append([
                entry["device_id"], entry["serial"], entry["model"], entry.get("storage") or "?",
                entry.get("activation_state") or "?", entry["health_pct"], entry["cycle_count"],
                entry["design_capacity"], entry["raw_max_capacity"], entry.get("cosmetic_grade") or "",
                entry["first_tested"], entry["last_tested"], "Yes" if all_checked else "No",
            ] + ["Yes" if checks.get(item) else "No" for item in CHECK_ITEMS])
        widths = [12, 22, 30, 10, 16, 16, 12, 20, 20, 14, 18, 18, 20] + [22] * len(CHECK_ITEMS)
        for idx, width in enumerate(widths, start=1):
            ws.column_dimensions[ws.cell(row=1, column=idx).column_letter].width = width
        wb.save(LOG_XLSX)


class Badge(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=BG, highlightthickness=0, height=32, **kwargs)

    def set(self, text, color):
        self.delete("all")
        pad_font = tkfont.Font(size=12, weight="bold")
        text_w = pad_font.measure(text) + 32
        self.configure(width=text_w)
        self.create_rectangle(0, 0, text_w, 32, fill=color, outline="", tags="pill")
        self.create_text(text_w / 2, 16, text=text, fill="#000000", font=pad_font)


class Gauge(tk.Canvas):
    SIZE = 150

    def __init__(self, parent):
        super().__init__(parent, width=self.SIZE, height=self.SIZE, bg=BG, highlightthickness=0)
        self.pct_font = tkfont.Font(size=36, weight="bold")
        self.label_font = tkfont.Font(size=11)

    def set(self, pct, color):
        self.delete("all")
        s = self.SIZE
        pad = 10
        self.create_oval(pad, pad, s - pad, s - pad, outline=CARD_BG, width=14)
        if pct is not None:
            extent = -359.999 * (pct / 100)
            self.create_arc(pad, pad, s - pad, s - pad, start=90, extent=extent,
                             outline=color, width=14, style="arc")
            self.create_text(s / 2, s / 2 - 8, text=f"{pct}%", fill=FG_MAIN, font=self.pct_font)
            self.create_text(s / 2, s / 2 + 22, text="Battery Health", fill=FG_DIM, font=self.label_font)
        else:
            self.create_text(s / 2, s / 2, text="--", fill=FG_DIM, font=self.pct_font)


class CheckRow(tk.Canvas):
    HEIGHT = 30

    def __init__(self, parent, label, on_toggle):
        super().__init__(parent, bg=CARD_BG, highlightthickness=0, height=self.HEIGHT)
        self.label = label
        self.on_toggle = on_toggle
        self.checked = False
        self.label_font = tkfont.Font(size=11)
        self.bind("<Configure>", lambda e: self.redraw())
        self.bind("<Button-1>", self._clicked)

    def _clicked(self, _event):
        self.checked = not self.checked
        self.redraw()
        self.on_toggle(self.label, self.checked)

    def set_checked(self, value, redraw=True):
        self.checked = value
        if redraw:
            self.redraw()

    def redraw(self):
        self.delete("all")
        w = self.winfo_width() or 200
        box, pad = 16, 7
        color = GREEN if self.checked else "#48484a"
        self.create_rectangle(pad, pad, pad + box, pad + box, outline=color, width=2,
                               fill=(GREEN if self.checked else CARD_BG))
        if self.checked:
            self.create_text(pad + box / 2, pad + box / 2, text="✓", fill="#000000",
                              font=tkfont.Font(size=11, weight="bold"))
        self.create_text(pad + box + 10, pad + box / 2, text=self.label, fill=FG_MAIN,
                          font=self.label_font, anchor="w")


class GradeSelector(tk.Canvas):
    HEIGHT = 46

    def __init__(self, parent, on_select):
        super().__init__(parent, bg=BG, highlightthickness=0, height=self.HEIGHT)
        self.on_select = on_select
        self.selected = None
        self.letter_font = tkfont.Font(size=16, weight="bold")
        self.sub_font = tkfont.Font(size=9)
        self._segment_bounds = []
        self.bind("<Configure>", lambda e: self.redraw())
        self.bind("<Button-1>", self._clicked)

    def _clicked(self, event):
        for x0, x1, letter in self._segment_bounds:
            if x0 <= event.x <= x1:
                self.selected = letter
                self.redraw()
                self.on_select(letter)
                return

    def set_selected(self, letter, redraw=True):
        self.selected = letter
        if redraw:
            self.redraw()

    def redraw(self):
        self.delete("all")
        w = self.winfo_width() or 400
        n = len(GRADE_OPTIONS)
        seg_w = w / n
        self._segment_bounds = []
        for i, (letter, desc) in enumerate(GRADE_OPTIONS):
            x0, x1 = i * seg_w, (i + 1) * seg_w
            is_sel = letter == self.selected
            pad = 4
            self.create_rectangle(x0 + pad, 2, x1 - pad, self.HEIGHT - 2,
                                   fill=(BLUE if is_sel else CARD_BG), outline="")
            self.create_text((x0 + x1) / 2, self.HEIGHT / 2 - 8, text=letter,
                              fill=("#000000" if is_sel else FG_MAIN), font=self.letter_font)
            self.create_text((x0 + x1) / 2, self.HEIGHT / 2 + 10, text=desc,
                              fill=("#000000" if is_sel else FG_DIM), font=self.sub_font)
            self._segment_bounds.append((x0, x1, letter))


class App:
    def __init__(self, root):
        self.root = root
        self.log = DeviceLog()
        self.last_udid = None
        self.current_serial = None
        self.check_rows = {}

        root.title("Battery Health Checker")
        root.geometry("460x850")
        root.configure(bg=BG)

        title_font = tkfont.Font(size=20, weight="bold")
        subtitle_font = tkfont.Font(size=13)
        row_label_font = tkfont.Font(size=11)
        row_value_font = tkfont.Font(size=12, weight="bold")
        section_font = tkfont.Font(size=11, weight="bold")

        header = tk.Frame(root, bg=BG)
        header.pack(fill="x", pady=(12, 2))
        tk.Label(header, text="Battery Health Checker", font=title_font, bg=BG, fg=FG_MAIN).pack()
        self.subtitle_var = tk.StringVar(value="Connect an iPad via USB")
        tk.Label(header, textvariable=self.subtitle_var, font=subtitle_font, bg=BG, fg=FG_DIM).pack(pady=(2, 0))

        self.badge = Badge(root)
        self.badge.pack(pady=(6, 2))

        self.gauge = Gauge(root)
        self.gauge.pack(pady=(2, 2))
        self.gauge.set(None, FG_DIM)

        card = tk.Frame(root, bg=CARD_BG)
        card.pack(fill="x", padx=24, pady=(6, 0))

        self.row_vars = {}
        self.row_labels = {}
        for key in ("Serial Number", "Device ID", "Storage", "Activation State", "Cycle Count", "Capacity"):
            row = tk.Frame(card, bg=CARD_BG)
            row.pack(fill="x", padx=16, pady=4)
            tk.Label(row, text=key, font=row_label_font, bg=CARD_BG, fg=FG_DIM, width=14, anchor="w").pack(side="left")
            var = tk.StringVar(value="--")
            lbl = tk.Label(row, textvariable=var, font=row_value_font, bg=CARD_BG, fg=FG_MAIN, anchor="e", justify="right")
            lbl.pack(side="right")
            self.row_vars[key] = var
            self.row_labels[key] = lbl

        tk.Label(root, text="COSMETIC GRADE (OPTIONAL)", font=section_font, bg=BG, fg=FG_DIM).pack(pady=(10, 3))
        self.grade_selector = GradeSelector(root, self.on_grade_select)
        self.grade_selector.pack(fill="x", padx=24)

        tk.Label(root, text="MANUAL FUNCTION CHECKS", font=section_font, bg=BG, fg=FG_DIM).pack(pady=(10, 3))

        checklist_card = tk.Frame(root, bg=CARD_BG)
        checklist_card.pack(fill="x", padx=24)
        cols = [tk.Frame(checklist_card, bg=CARD_BG) for _ in range(2)]
        for i, col in enumerate(cols):
            col.grid(row=0, column=i, sticky="nw", padx=(16 if i == 0 else 8, 8 if i == 0 else 16), pady=8)
        for idx, item in enumerate(CHECK_ITEMS):
            col = cols[idx % 2]
            row = CheckRow(col, item, self.on_check_toggle)
            row.pack(fill="x", pady=2)
            row.configure(width=170)
            self.check_rows[item] = row

        footer = tk.Frame(root, bg=BG)
        footer.pack(side="bottom", fill="x", pady=6)
        btn_style = dict(relief="flat", bg=CARD_BG, fg="white", activebackground="#3a3a3c",
                          activeforeground="white", padx=14, pady=8, bd=0)
        tk.Button(footer, text="Refresh", command=self.poll, **btn_style).pack(side="left", expand=True, padx=(24, 6))
        tk.Button(footer, text="Open Log", command=self.open_log, **btn_style).pack(side="right", expand=True, padx=(6, 24))

        self.count_var = tk.StringVar(value=self._count_text())
        tk.Label(root, textvariable=self.count_var, font=tkfont.Font(size=10), bg=BG, fg=FG_DIM).pack(side="bottom", pady=(0, 4))

        root.update_idletasks()
        root.geometry("460x850")
        root.minsize(460, 850)
        root.resizable(False, False)

        self.poll()

    def _count_text(self):
        n = len(self.log.records)
        return f"{n} device{'s' if n != 1 else ''} logged"

    def open_log(self):
        target = LOG_XLSX if LOG_XLSX.exists() else DATA_DIR
        if IS_WINDOWS:
            import os
            os.startfile(str(target))
        else:
            subprocess.run(["open", str(target)])

    def on_check_toggle(self, item, value):
        if self.current_serial:
            self.log.set_check(self.current_serial, item, value)

    def on_grade_select(self, letter):
        if self.current_serial:
            self.log.set_grade(self.current_serial, letter)

    def set_checklist(self, checks):
        for item, row in self.check_rows.items():
            row.set_checked(bool(checks.get(item, False)))

    def set_waiting(self, message="Waiting for iPad…"):
        self.last_udid = None
        self.current_serial = None
        self.subtitle_var.set(message)
        self.badge.set("WAITING", FG_DIM)
        self.gauge.set(None, FG_DIM)
        for key, var in self.row_vars.items():
            var.set("--")
            self.row_labels[key].configure(fg=FG_MAIN)
        self.set_checklist({})
        self.grade_selector.set_selected(None)

    def poll(self):
        udid = get_udid()
        if not udid:
            self.set_waiting()
        elif udid != self.last_udid:
            self.handle_new_connection(udid)
        self.root.after(POLL_MS, self.poll)

    def handle_new_connection(self, udid):
        info, code, err = get_device_info(udid)
        if code != 0 or not info:
            if "trust" in (err or "").lower() or "pair" in (err or "").lower():
                self.subtitle_var.set("On the iPad, tap “Trust”, then unlock the screen.")
                self.badge.set("TRUST NEEDED", ORANGE)
            else:
                self.subtitle_var.set("Connecting…")
                self.badge.set("CONNECTING", FG_DIM)
            return

        self.last_udid = udid
        serial = info.get("SerialNumber", "Unknown")
        product_type = info.get("ProductType", "Unknown")
        model_name = PRODUCT_NAMES.get(product_type, product_type)
        storage_gb = get_storage_gb(udid)
        storage_str = f"{storage_gb}GB" if storage_gb else "?"
        activation_state = info.get("ActivationState", "?")

        battery, batt_err = get_battery_data(udid)
        if not battery:
            self.subtitle_var.set(model_name)
            self.badge.set("NO BATTERY DATA", RED)
            self.gauge.set(None, FG_DIM)
            self.row_vars["Serial Number"].set(serial)
            self.row_vars["Storage"].set(storage_str)
            self.row_vars["Activation State"].set(activation_state)
            return

        pct = battery_health_percent(battery)
        cycle_count = battery.get("CycleCount", "?")
        design = battery.get("DesignCapacity", "?")
        raw_max = battery.get("AppleRawMaxCapacity", "?")

        entry, is_new = self.log.record_test(serial, model_name, storage_str, activation_state,
                                              pct, cycle_count, design, raw_max)
        self.current_serial = serial

        self.subtitle_var.set(f"{model_name} · {storage_str}")
        color = GREEN if (pct or 0) >= 80 else (ORANGE if (pct or 0) >= 60 else RED)
        self.gauge.set(pct, color)

        if is_new:
            self.badge.set("NEW • LOGGED", BLUE)
        else:
            self.badge.set(f"ALREADY TESTED • {entry['first_tested']}", ORANGE)

        self.row_vars["Serial Number"].set(serial)
        self.row_vars["Device ID"].set(entry["device_id"])
        self.row_vars["Storage"].set(storage_str)
        self.row_vars["Activation State"].set(activation_state)
        self.row_labels["Activation State"].configure(fg=GREEN if activation_state == "Activated" else ORANGE)
        self.row_vars["Cycle Count"].set(str(cycle_count))
        self.row_vars["Capacity"].set(f"{raw_max} / {design} mAh")
        self.set_checklist(entry.get("checks", {}))
        self.grade_selector.set_selected(entry.get("cosmetic_grade"))
        self.count_var.set(self._count_text())


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
