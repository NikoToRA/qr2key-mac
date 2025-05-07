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
    
    @patch('pynput.keyboard.Controller')
    def test_type_string(self, mock_controller):
        """Test typing a string."""
        mock_keyboard = MagicMock()
        mock_controller.return_value = mock_keyboard
        
        keyboard = KeyboardController()
        
        test_string = "Hello, World!"
        keyboard.type_string(test_string)
        
        mock_keyboard.type.assert_called_once_with(test_string)
    
    @patch('pynput.keyboard.Controller')
    def test_press_key(self, mock_controller):
        """Test pressing a key."""
        mock_keyboard = MagicMock()
        mock_controller.return_value = mock_keyboard
        
        keyboard = KeyboardController()
        
        test_key = 'a'
        keyboard.press_key(test_key)
        
        mock_keyboard.press.assert_called_once_with(test_key)
        mock_keyboard.release.assert_called_once_with(test_key)
    
    @patch('pynput.keyboard.Controller')
    @patch('pynput.keyboard.Key')
    def test_press_enter(self, mock_key, mock_controller):
        """Test pressing the Enter key."""
        mock_keyboard = MagicMock()
        mock_controller.return_value = mock_keyboard
        
        mock_key.enter = 'enter'
        
        keyboard = KeyboardController()
        
        keyboard.press_enter()
        
        mock_keyboard.press.assert_called_once_with('enter')
        mock_keyboard.release.assert_called_once_with('enter')
    
    @patch('pynput.keyboard.Controller')
    @patch('time.sleep')
    def test_type_with_delay(self, mock_sleep, mock_controller):
        """Test typing with a delay."""
        mock_keyboard = MagicMock()
        mock_controller.return_value = mock_keyboard
        
        keyboard = KeyboardController()
        
        test_string = "Hello"
        test_delay = 0.1
        keyboard.type_with_delay(test_string, test_delay)
        
        self.assertEqual(mock_keyboard.type.call_count, len(test_string))
        
        self.assertEqual(mock_sleep.call_count, len(test_string))
        for call in mock_sleep.call_args_list:
            self.assertEqual(call[0][0], test_delay)

if __name__ == '__main__':
    unittest.main()
