"""
QR2Key - System tray functionality
"""

import os
import sys
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem
from loguru import logger

class SystemTray:
    """System tray icon and menu for QR2Key."""
    
    def __init__(self, app_name="QR2Key", icon_size=(64, 64)):
        """Initialize the system tray icon."""
        self.app_name = app_name
        self.icon_size = icon_size
        self.is_paused = False
        self.icon = None
        self.exit_callback = None
        self.pause_callback = None
        self.resume_callback = None
        
    def create_icon_image(self):
        """Create a simple icon image for the tray."""
        image = Image.new('RGB', self.icon_size, color=(53, 153, 219))
        draw = ImageDraw.Draw(image)
        
        draw.rectangle(
            [(0, 0), (self.icon_size[0] - 1, self.icon_size[1] - 1)],
            outline=(41, 128, 185),
            width=2
        )
        
        draw.text(
            (self.icon_size[0] // 4, self.icon_size[1] // 4),
            'QR',
            fill=(255, 255, 255)
        )
        
        return image
    
    def setup(self, exit_callback, pause_callback, resume_callback):
        """Set up the system tray icon with menu items."""
        self.exit_callback = exit_callback
        self.pause_callback = pause_callback
        self.resume_callback = resume_callback
        
        icon_image = self.create_icon_image()
        
        menu = Menu(
            MenuItem(
                lambda item: "Resume" if self.is_paused else "Pause",
                self._toggle_pause
            ),
            MenuItem("Exit", self._exit)
        )
        
        self.icon = Icon(
            name=self.app_name,
            icon=icon_image,
            title=self.app_name,
            menu=menu
        )
        
        logger.info("System tray icon initialized")
        
    def _toggle_pause(self, icon, item):
        """Toggle between pause and resume states."""
        if self.is_paused:
            logger.info("Resuming QR2Key")
            self.is_paused = False
            if self.resume_callback:
                self.resume_callback()
        else:
            logger.info("Pausing QR2Key")
            self.is_paused = True
            if self.pause_callback:
                self.pause_callback()
    
    def _exit(self, icon, item):
        """Exit the application."""
        logger.info("Exiting QR2Key from system tray")
        icon.stop()
        if self.exit_callback:
            self.exit_callback()
    
    def run(self):
        """Run the system tray icon."""
        if self.icon:
            logger.info(f"Starting {self.app_name} system tray icon")
            self.icon.run()
        else:
            logger.error("System tray icon not initialized. Call setup() first.")
    
    def update_status(self, is_paused):
        """Update the pause/resume status."""
        self.is_paused = is_paused
