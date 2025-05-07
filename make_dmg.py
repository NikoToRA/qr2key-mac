"""
QR2Key - Script to build DMG installer
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_resources():
    """Create necessary resources for the app."""
    if not os.path.exists('resources'):
        os.makedirs('resources')
    
    try:
        subprocess.run(['convert', '-size', '640x480', 'gradient:blue-navy', 
                        'resources/dmg_background.png'])
    except Exception as e:
        print(f"Error creating background: {e}")
        Path('resources/dmg_background.png').touch()

def build_app():
    """Build the macOS app using py2app."""
    print("Building macOS app with py2app...")
    
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    result = subprocess.run(['python', 'setup.py', 'py2app'], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error building app:")
        print(result.stderr)
        return False
    
    print("App built successfully")
    return True

def build_dmg():
    """Build the DMG installer."""
    print("Building DMG installer...")
    
    result = subprocess.run(['dmgbuild', '-s', 'dmgbuild_settings.py', 
                            'QR2Key', 'dist/QR2Key_Installer.dmg'], 
                            capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error building DMG:")
        print(result.stderr)
        return False
    
    print("DMG built successfully at dist/QR2Key_Installer.dmg")
    return True

def main():
    """Main function to build the app and DMG."""
    create_resources()
    
    if build_app():
        build_dmg()
    else:
        print("Failed to build app, cannot create DMG")
        sys.exit(1)

if __name__ == "__main__":
    main()
