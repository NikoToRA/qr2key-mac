"""
Unit tests for QR2Key configuration functionality
"""

import unittest
import sys
import os
import json
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config, DEFAULT_CONFIG

class TestConfig(unittest.TestCase):
    """Test cases for the Config class."""
    
    def setUp(self):
        """Set up a temporary directory for test config files."""
        self.test_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.test_dir, "test_config.json")
    
    def tearDown(self):
        """Clean up temporary directory after tests."""
        shutil.rmtree(self.test_dir)
    
    def test_default_config_creation(self):
        """Test that a default config file is created if it doesn't exist."""
        config = Config(self.config_path)
        
        self.assertTrue(os.path.exists(self.config_path))
        
        with open(self.config_path, 'r') as f:
            loaded_config = json.load(f)
        
        self.assertEqual(loaded_config, DEFAULT_CONFIG)
    
    def test_load_existing_config(self):
        """Test loading an existing config file."""
        custom_config = {
            "serial": {
                "port": "/dev/cu.usbserial-1140",
                "baud_rate": 115200,
                "timeout": 2,
                "auto_detect": True,
                "monitor_ports": True
            },
            "keyboard": {
                "type_delay": 0.1,
                "press_enter_after": True
            },
            "app": {
                "start_minimized": True,
                "auto_start": True,
                "log_level": "DEBUG"
            }
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(custom_config, f)
        
        config = Config(self.config_path)
        
        self.assertEqual(config.get_all(), custom_config)
    
    def test_get_config_value(self):
        """Test getting a config value."""
        config = Config(self.config_path)
        
        self.assertEqual(config.get("serial", "baud_rate"), 9600)
        self.assertEqual(config.get("keyboard", "press_enter_after"), False)
        
        self.assertEqual(config.get("nonexistent", "key", "default"), "default")
    
    def test_set_config_value(self):
        """Test setting a config value."""
        config = Config(self.config_path)
        
        config.set("serial", "baud_rate", 115200)
        
        self.assertEqual(config.get("serial", "baud_rate"), 115200)
        
        config.save_config()
        new_config = Config(self.config_path)
        self.assertEqual(new_config.get("serial", "baud_rate"), 115200)
        
        self.assertFalse(config.set("nonexistent", "key", "value"))

if __name__ == '__main__':
    unittest.main()
