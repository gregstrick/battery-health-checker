from setuptools import setup

APP = ["src/main.py"]
OPTIONS = {
    "argv_emulation": False,
    "iconfile": "AppIcon.icns",
    "plist": {
        "CFBundleName": "Battery Health Checker",
        "CFBundleDisplayName": "Battery Health Checker",
        "CFBundleIdentifier": "com.gstrick.batteryhealthchecker",
        "CFBundleShortVersionString": "1.2.0",
        "CFBundleVersion": "1.2.0",
        "LSMinimumSystemVersion": "11.0",
        "NSHighResolutionCapable": False,
        "LSMultipleInstancesProhibited": True,
    },
    "packages": ["openpyxl"],
}

setup(
    app=APP,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
