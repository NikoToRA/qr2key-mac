"""
Unit tests for QR2Key system tray functionality
"""

import unittest
import sys
import os
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tray import SystemTray

class TestSystemTray(unittest.TestCase):
    """Test cases for the SystemTray class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tray = SystemTray(app_name="TestQR2Key")
    
    def test_init(self):
        """Test initialization of the SystemTray."""
        self.assertEqual(self.tray.app_name, "TestQR2Key")
        self.assertEqual(self.tray.icon_size, (64, 64))
        self.assertFalse(self.tray.is_paused)
        self.assertIsNone(self.tray.icon)
        self.assertIsNone(self.tray.exit_callback)
        self.assertIsNone(self.tray.pause_callback)
        self.assertIsNone(self.tray.resume_callback)
    
    @patch('tray.Image')
    @patch('tray.ImageDraw')
    def test_create_icon_image(self, mock_image_draw, mock_image):
        """Test creating the icon image."""
        mock_image_instance = MagicMock()
        mock_image.new.return_value = mock_image_instance
        
        mock_draw = MagicMock()
        mock_image_draw.Draw.return_value = mock_draw
        
        result = self.tray.create_icon_image()
        
        self.assertEqual(result, mock_image_instance)
        mock_image.new.assert_called_once_with('RGB', (64, 64), color=(53, 153, 219))
        mock_image_draw.Draw.assert_called_once_with(mock_image_instance)
        mock_draw.rectangle.assert_called_once()
        mock_draw.text.assert_called_once()
    
    @patch('tray.Icon')
    @patch('tray.Menu')
    @patch('tray.MenuItem')
    def test_setup(self, mock_menu_item, mock_menu, mock_icon):
        """Test setting up the system tray icon."""
        mock_exit_callback = MagicMock()
        mock_pause_callback = MagicMock()
        mock_resume_callback = MagicMock()
        
        mock_toggle_item = MagicMock()
        mock_exit_item = MagicMock()
        mock_menu_item.side_effect = [mock_toggle_item, mock_exit_item]
        
        mock_menu_instance = MagicMock()
        mock_menu.return_value = mock_menu_instance
        
        mock_icon_instance = MagicMock()
        mock_icon.return_value = mock_icon_instance
        
        with patch.object(self.tray, 'create_icon_image') as mock_create_icon:
            mock_icon_image = MagicMock()
            mock_create_icon.return_value = mock_icon_image
            
            self.tray.setup(
                exit_callback=mock_exit_callback,
                pause_callback=mock_pause_callback,
                resume_callback=mock_resume_callback
            )
            
            self.assertEqual(self.tray.exit_callback, mock_exit_callback)
            self.assertEqual(self.tray.pause_callback, mock_pause_callback)
            self.assertEqual(self.tray.resume_callback, mock_resume_callback)
            
            mock_create_icon.assert_called_once()
            mock_menu.assert_called_once()
            self.assertEqual(mock_menu_item.call_count, 2)
            
            mock_icon.assert_called_once_with(
                name="TestQR2Key",
                icon=mock_icon_image,
                title="TestQR2Key",
                menu=mock_menu_instance
            )
            
            self.assertEqual(self.tray.icon, mock_icon_instance)
    
    def test_toggle_pause_when_paused(self):
        """Test toggling pause when already paused."""
        self.tray.is_paused = True
        mock_resume_callback = MagicMock()
        self.tray.resume_callback = mock_resume_callback
        
        mock_icon = MagicMock()
        mock_item = MagicMock()
        
        self.tray._toggle_pause(mock_icon, mock_item)
        
        self.assertFalse(self.tray.is_paused)
        mock_resume_callback.assert_called_once()
    
    def test_toggle_pause_when_not_paused(self):
        """Test toggling pause when not paused."""
        self.tray.is_paused = False
        mock_pause_callback = MagicMock()
        self.tray.pause_callback = mock_pause_callback
        
        mock_icon = MagicMock()
        mock_item = MagicMock()
        
        self.tray._toggle_pause(mock_icon, mock_item)
        
        self.assertTrue(self.tray.is_paused)
        mock_pause_callback.assert_called_once()
    
    def test_exit(self):
        """Test exiting the application."""
        mock_exit_callback = MagicMock()
        self.tray.exit_callback = mock_exit_callback
        
        mock_icon = MagicMock()
        mock_item = MagicMock()
        
        self.tray._exit(mock_icon, mock_item)
        
        mock_icon.stop.assert_called_once()
        mock_exit_callback.assert_called_once()
    
    @patch('tray.logger')
    def test_run_when_icon_not_initialized(self, mock_logger):
        """Test running the system tray when icon is not initialized."""
        self.tray.icon = None
        
        self.tray.run()
        
        mock_logger.error.assert_called_once()
    
    def test_update_status(self):
        """Test updating the pause/resume status."""
        self.tray.is_paused = False
        
        self.tray.update_status(True)
        
        self.assertTrue(self.tray.is_paused)

if __name__ == '__main__':
    unittest.main()
