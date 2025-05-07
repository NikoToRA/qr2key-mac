"""
QR2Key - py2app setup script
"""

from setuptools import setup

APP = ['src/main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleName': 'QR2Key',
        'CFBundleDisplayName': 'QR2Key',
        'CFBundleIdentifier': 'com.qr2key.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2025',
        'LSUIElement': True,  # Run as agent (no dock icon)
        'LSBackgroundOnly': False,
    },
    'packages': ['PyQt5', 'serial', 'loguru'],
    'includes': ['sip'],
    'excludes': ['tkinter', 'matplotlib', 'numpy'],
}

setup(
    name='QR2Key',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
