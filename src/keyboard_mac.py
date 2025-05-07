"""
QR2Key - Keyboard input simulation for macOS
"""

from pynput.keyboard import Controller, Key
import time
from loguru import logger

class KeyboardController:
    """Class to handle keyboard input simulation on macOS."""
    
    def __init__(self):
        """Initialize the keyboard controller."""
        self.keyboard = Controller()
        logger.debug("Keyboard controller initialized")
        
    def type_string(self, text):
        """Type a string of text."""
        if not text:
            return
            
        logger.debug(f"Typing string: {text}")
        self.keyboard.type(text)
        
    def press_key(self, key):
        """Press a specific key."""
        logger.debug(f"Pressing key: {key}")
        self.keyboard.press(key)
        self.keyboard.release(key)
        
    def press_enter(self):
        """Press the Enter key."""
        logger.debug("Pressing Enter key")
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        
    def press_tab(self):
        """Press the Tab key."""
        logger.debug("Pressing Tab key")
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
        
    def type_with_delay(self, text, delay=0.05):
        """Type text with a delay between each character."""
        if not text:
            return
            
        logger.debug(f"Typing with delay ({delay}s): {text}")
        for char in text:
            self.keyboard.type(char)
            time.sleep(delay)
