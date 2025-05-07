"""
Unit tests for QR2Key port detection functionality
"""

import unittest
import sys
import os
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from port_detector import PortDetector

class TestPortDetector(unittest.TestCase):
    """Test cases for the PortDetector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = PortDetector()
    
    @patch('serial.tools.list_ports.comports')
    def test_list_ports(self, mock_comports):
        """Test listing available ports."""
        mock_port1 = MagicMock()
        mock_port1.device = '/dev/ttyUSB0'
        mock_port1.description = 'USB Serial Device'
        mock_port1.vid = 0x0403  # FTDI
        mock_port1.pid = 0x6001
        
        mock_port2 = MagicMock()
        mock_port2.device = '/dev/ttyUSB1'
        mock_port2.description = 'CH340 Serial Device'
        mock_port2.vid = 0x1A86  # CH340
        mock_port2.pid = 0x7523
        
        mock_comports.return_value = [mock_port1, mock_port2]
        
        ports = self.detector.list_ports()
        
        self.assertEqual(len(ports), 2)
        self.assertEqual(ports[0].device, '/dev/ttyUSB0')
        self.assertEqual(ports[1].device, '/dev/ttyUSB1')
    
    @patch('serial.tools.list_ports.comports')
    def test_find_ports_with_no_filters(self, mock_comports):
        """Test finding ports with no filters."""
        mock_port1 = MagicMock()
        mock_port1.device = '/dev/ttyUSB0'
        mock_port1.description = 'USB Serial Device'
        mock_port1.vid = 0x0403  # FTDI
        mock_port1.pid = 0x6001
        
        mock_comports.return_value = [mock_port1]
        
        detector = PortDetector(vendor_ids=[], product_ids=[], descriptions=[])
        
        ports = detector.find_ports()
        
        self.assertEqual(len(ports), 1)
        self.assertEqual(ports[0].device, '/dev/ttyUSB0')
    
    @patch('serial.tools.list_ports.comports')
    def test_find_ports_with_vendor_id_filter(self, mock_comports):
        """Test finding ports with vendor ID filter."""
        mock_port1 = MagicMock()
        mock_port1.device = '/dev/ttyUSB0'
        mock_port1.description = 'USB Serial Device'
        mock_port1.vid = 0x0403  # FTDI
        mock_port1.pid = 0x6001
        
        mock_port2 = MagicMock()
        mock_port2.device = '/dev/ttyUSB1'
        mock_port2.description = 'CH340 Serial Device'
        mock_port2.vid = 0x1A86  # CH340
        mock_port2.pid = 0x7523
        
        mock_comports.return_value = [mock_port1, mock_port2]
        
        detector = PortDetector(vendor_ids=["0403"], product_ids=[], descriptions=[])
        
        ports = detector.find_ports()
        
        self.assertEqual(len(ports), 1)
        self.assertEqual(ports[0].device, '/dev/ttyUSB0')
    
    @patch('serial.tools.list_ports.comports')
    def test_find_ports_with_description_filter(self, mock_comports):
        """Test finding ports with description filter."""
        mock_port1 = MagicMock()
        mock_port1.device = '/dev/ttyUSB0'
        mock_port1.description = 'USB Serial Device'
        mock_port1.vid = 0x0403  # FTDI
        mock_port1.pid = 0x6001
        
        mock_port2 = MagicMock()
        mock_port2.device = '/dev/ttyUSB1'
        mock_port2.description = 'CH340 Serial Device'
        mock_port2.vid = 0x1A86  # CH340
        mock_port2.pid = 0x7523
        
        mock_comports.return_value = [mock_port1, mock_port2]
        
        detector = PortDetector(vendor_ids=[], product_ids=[], descriptions=["CH340"])
        
        ports = detector.find_ports()
        
        self.assertEqual(len(ports), 1)
        self.assertEqual(ports[0].device, '/dev/ttyUSB1')
    
    @patch('serial.tools.list_ports.comports')
    def test_auto_detect_port(self, mock_comports):
        """Test auto-detecting a port."""
        mock_port1 = MagicMock()
        mock_port1.device = '/dev/ttyUSB0'
        mock_port1.description = 'USB Serial Device'
        mock_port1.vid = 0x0403  # FTDI
        mock_port1.pid = 0x6001
        
        mock_comports.return_value = [mock_port1]
        
        port = self.detector.auto_detect_port()
        
        self.assertEqual(port, '/dev/ttyUSB0')
    
    @patch('serial.tools.list_ports.comports')
    def test_auto_detect_port_with_multiple_matches(self, mock_comports):
        """Test auto-detecting a port with multiple matches."""
        mock_port1 = MagicMock()
        mock_port1.device = '/dev/ttyUSB0'
        mock_port1.description = 'USB Serial Device'
        mock_port1.vid = 0x0403  # FTDI
        mock_port1.pid = 0x6001
        
        mock_port2 = MagicMock()
        mock_port2.device = '/dev/ttyUSB1'
        mock_port2.description = 'CH340 Serial Device'
        mock_port2.vid = 0x1A86  # CH340
        mock_port2.pid = 0x7523
        
        mock_comports.return_value = [mock_port1, mock_port2]
        
        port = self.detector.auto_detect_port()
        
        self.assertEqual(port, '/dev/ttyUSB0')
    
    @patch('serial.tools.list_ports.comports')
    def test_auto_detect_port_with_no_matches(self, mock_comports):
        """Test auto-detecting a port with no matches."""
        mock_comports.return_value = []
        
        port = self.detector.auto_detect_port()
        
        self.assertIsNone(port)

if __name__ == '__main__':
    unittest.main()
