"""
QR2Key - Configuration management
"""

import os
import json
from loguru import logger

DEFAULT_CONFIG = {
    "serial": {
        "port": "/dev/cu.usbserial-1140",
        "baud_rate": 9600,
        "timeout": 1,
        "auto_detect": True,
        "monitor_ports": True
    },
    "keyboard": {
        "type_delay": 0.05,
        "press_enter_after": False
    },
    "app": {
        "start_minimized": False,
        "auto_start": False,
        "log_level": "INFO"
    }
}

class Config:
    """Configuration manager for QR2Key."""
    
    def __init__(self, config_path="config.json"):
        """Initialize configuration with default values or from file."""
        self.config_path = config_path
        self.config = DEFAULT_CONFIG.copy()
        
        if not os.path.exists(config_path):
            logger.info(f"Creating default configuration file at {config_path}")
            self.save_config()
        else:
            self.load_config()
    
    def load_config(self):
        """Load configuration from file."""
        try:
            with open(self.config_path, 'r') as f:
                loaded_config = json.load(f)
                
            for section in DEFAULT_CONFIG:
                if section in loaded_config:
                    for key in DEFAULT_CONFIG[section]:
                        if key in loaded_config[section]:
                            self.config[section][key] = loaded_config[section][key]
                            
            logger.info(f"Configuration loaded from {self.config_path}")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            logger.info("Using default configuration")
    
    def save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def get(self, section, key, default=None):
        """Get a configuration value."""
        try:
            return self.config[section][key]
        except KeyError:
            logger.warning(f"Configuration key {section}.{key} not found, using default: {default}")
            return default
    
    def set(self, section, key, value):
        """Set a configuration value."""
        try:
            self.config[section][key] = value
            logger.debug(f"Configuration updated: {section}.{key} = {value}")
            return True
        except KeyError:
            logger.error(f"Invalid configuration section or key: {section}.{key}")
            return False
    
    def get_all(self):
        """Get the entire configuration."""
        return self.config
