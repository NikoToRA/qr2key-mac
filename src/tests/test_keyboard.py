"""
Unit tests for QR2Key keyboard functionality
"""

import unittest
import sys
import os
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from keyboard_mac import KeyboardController

class TestKeyboard(unittest.TestCase):
    """Test cases for the KeyboardController class."""
    
    def test_type_string(self):
        """Test typing a string."""
        with patch('keyboard_mac.Controller') as mock_controller_class:
            mock_controller = MagicMock()
            mock_controller_class.return_value = mock_controller
            
            keyboard = KeyboardController()
            
            test_string = "Hello, World!"
            keyboard.type_string(test_string)
            
            mock_controller.type.assert_called_once_with(test_string)
    
    def test_press_key(self):
        """Test pressing a key."""
        with patch('keyboard_mac.Controller') as mock_controller_class:
            mock_controller = MagicMock()
            mock_controller_class.return_value = mock_controller
            
            keyboard = KeyboardController()
            
            test_key = 'a'
            keyboard.press_key(test_key)
            
            mock_controller.press.assert_called_once_with(test_key)
            mock_controller.release.assert_called_once_with(test_key)
    
    def test_press_enter(self):
        """Test pressing the Enter key."""
        with patch('keyboard_mac.Controller') as mock_controller_class, \
             patch('keyboard_mac.Key') as mock_key:
            mock_controller = MagicMock()
            mock_controller_class.return_value = mock_controller
            
            mock_key.enter = 'mock_enter'
            
            keyboard = KeyboardController()
            
            keyboard.press_enter()
            
            mock_controller.press.assert_called_once_with(mock_key.enter)
            mock_controller.release.assert_called_once_with(mock_key.enter)
    
    def test_type_with_delay(self):
        """Test typing with a delay."""
        with patch('keyboard_mac.Controller') as mock_controller_class, \
             patch('time.sleep') as mock_sleep:
            mock_controller = MagicMock()
            mock_controller_class.return_value = mock_controller
            
            keyboard = KeyboardController()
            
            test_string = "Hello"
            test_delay = 0.1
            keyboard.type_with_delay(test_string, test_delay)
            
            self.assertEqual(mock_controller.type.call_count, len(test_string))
            
            self.assertEqual(mock_sleep.call_count, len(test_string))
            for call in mock_sleep.call_args_list:
                self.assertEqual(call[0][0], test_delay)

if __name__ == '__main__':
    unittest.main()
