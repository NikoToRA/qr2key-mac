"""
Unit tests for QR2Key Shift_JIS decoding functionality
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import decode_shift_jis

class TestDecode(unittest.TestCase):
    """Test cases for the decode_shift_jis function."""
    
    def test_shift_jis_decode(self):
        """Test decoding Shift_JIS encoded text."""
        shift_jis_bytes = b'\x82\xb1\x82\xf1\x82\xc9\x82\xbf\x82\xcd'
        result = decode_shift_jis(shift_jis_bytes)
        self.assertEqual(result, "こんにちは")
        
    def test_utf8_fallback(self):
        """Test fallback to UTF-8 when Shift_JIS fails."""
        utf8_bytes = b'\xe3\x81\x93\xe3\x82\x93\xe3\x81\xab\xe3\x81\xa1\xe3\x81\xaf'
        result = decode_shift_jis(utf8_bytes)
        self.assertEqual(result, "こんにちは")
        
    def test_invalid_encoding(self):
        """Test handling of invalid encoding."""
        invalid_bytes = b'\xFF\xFE\xFD\xFC'
        result = decode_shift_jis(invalid_bytes)
        self.assertEqual(result, "ff fe fd fc")

if __name__ == '__main__':
    unittest.main()
