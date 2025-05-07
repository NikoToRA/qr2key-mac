"""
QR2Key - Auto-start functionality for macOS
"""

import os
import sys
import plistlib
from pathlib import Path
from loguru import logger

def get_app_path():
    """Get the path to the application bundle."""
    if getattr(sys, 'frozen', False):
        app_path = os.path.abspath(os.path.dirname(os.path.dirname(sys.executable)))
        return app_path
    else:
        return None

def create_launch_agent(enable=True):
    """Create a launch agent plist file for auto-start."""
    app_path = get_app_path()
    if not app_path:
        logger.error("Cannot create launch agent: not running as a bundled app")
        return False
    
    launch_agents_dir = os.path.expanduser("~/Library/LaunchAgents")
    os.makedirs(launch_agents_dir, exist_ok=True)
    
    plist_path = os.path.join(launch_agents_dir, "com.qr2key.app.plist")
    
    plist_content = {
        'Label': 'com.qr2key.app',
        'ProgramArguments': [f"{app_path}/Contents/MacOS/QR2Key"],
        'RunAtLoad': True,
        'KeepAlive': False,
    }
    
    try:
        with open(plist_path, 'wb') as f:
            plistlib.dump(plist_content, f)
        
        logger.info(f"Created launch agent at {plist_path}")
        
        if enable:
            os.system(f"launchctl load {plist_path}")
            logger.info("Enabled auto-start via launchd")
        
        return True
    except Exception as e:
        logger.error(f"Error creating launch agent: {e}")
        return False

def remove_launch_agent():
    """Remove the launch agent plist file."""
    plist_path = os.path.expanduser("~/Library/LaunchAgents/com.qr2key.app.plist")
    
    if os.path.exists(plist_path):
        try:
            os.system(f"launchctl unload {plist_path}")
            
            os.remove(plist_path)
            
            logger.info(f"Removed launch agent at {plist_path}")
            return True
        except Exception as e:
            logger.error(f"Error removing launch agent: {e}")
            return False
    else:
        logger.info("No launch agent found to remove")
        return True

def is_auto_start_enabled():
    """Check if auto-start is enabled."""
    plist_path = os.path.expanduser("~/Library/LaunchAgents/com.qr2key.app.plist")
    return os.path.exists(plist_path)

def toggle_auto_start(enable):
    """Toggle auto-start on or off."""
    if enable:
        return create_launch_agent(True)
    else:
        return remove_launch_agent()
