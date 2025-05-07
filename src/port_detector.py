"""
QR2Key - Automatic serial port detection
"""

import re
import time
import serial
import serial.tools.list_ports
from loguru import logger

class PortDetector:
    """Class to handle automatic serial port detection."""
    
    def __init__(self, vendor_ids=None, product_ids=None, descriptions=None):
        """Initialize the port detector with optional filters."""
        self.vendor_ids = vendor_ids or []  # List of vendor IDs to filter by
        self.product_ids = product_ids or []  # List of product IDs to filter by
        self.descriptions = descriptions or []  # List of description patterns to filter by
        
        if not self.vendor_ids:
            self.vendor_ids = ["0403", "10C4", "1A86", "067B"]
        
        logger.debug(f"Port detector initialized with filters: vendor_ids={self.vendor_ids}, "
                    f"product_ids={self.product_ids}, descriptions={self.descriptions}")
    
    def list_ports(self):
        """List all available serial ports."""
        ports = list(serial.tools.list_ports.comports())
        logger.debug(f"Found {len(ports)} serial ports")
        return ports
    
    def find_ports(self):
        """Find serial ports matching the filters."""
        all_ports = self.list_ports()
        matched_ports = []
        
        for port in all_ports:
            if self._matches_filters(port):
                matched_ports.append(port)
                logger.debug(f"Port matched filters: {port.device} - {port.description}")
        
        logger.info(f"Found {len(matched_ports)} ports matching filters")
        return matched_ports
    
    def _matches_filters(self, port):
        """Check if a port matches the filters."""
        if not self.vendor_ids and not self.product_ids and not self.descriptions:
            return True
        
        matches = []
        
        if self.vendor_ids and hasattr(port, 'vid') and port.vid:
            vid_str = f"{port.vid:04x}"
            vid_match = vid_str.lower() in [v.lower() for v in self.vendor_ids]
            matches.append((bool(self.vendor_ids), vid_match))
        
        if self.product_ids and hasattr(port, 'pid') and port.pid:
            pid_str = f"{port.pid:04x}"
            pid_match = pid_str.lower() in [p.lower() for p in self.product_ids]
            matches.append((bool(self.product_ids), pid_match))
        
        if self.descriptions and port.description:
            desc_match = False
            for desc in self.descriptions:
                if re.search(desc, port.description, re.IGNORECASE):
                    desc_match = True
                    break
            matches.append((bool(self.descriptions), desc_match))
        
        # If any filter category is active but no matches in that category, return False
        for filter_active, filter_match in matches:
            if filter_active and not filter_match:
                return False
        
        # If we have any matches and all active filters have at least one match, return True
        return len(matches) > 0
    
    def auto_detect_port(self):
        """Automatically detect the most likely QR reader port."""
        matched_ports = self.find_ports()
        
        if not matched_ports:
            logger.warning("No ports matched the filters")
            return None
        
        if len(matched_ports) == 1:
            logger.info(f"Auto-detected single matching port: {matched_ports[0].device}")
            return matched_ports[0].device
        
        logger.warning(f"Multiple ports matched filters, using first one: {matched_ports[0].device}")
        return matched_ports[0].device
    
    def monitor_ports(self, callback, interval=2.0):
        """Monitor for port changes and call the callback when a new port is detected."""
        logger.info(f"Starting port monitoring with interval {interval}s")
        
        known_ports = set(port.device for port in self.find_ports())
        
        try:
            while True:
                current_ports = set(port.device for port in self.find_ports())
                
                new_ports = current_ports - known_ports
                if new_ports:
                    logger.info(f"New ports detected: {new_ports}")
                    for port in new_ports:
                        callback(port)
                
                known_ports = current_ports
                
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Port monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error in port monitoring: {e}")
