"""
QR2Key - QR Code Reader to Keyboard Input
Milestone M1: macOS typing + config/log
"""

import sys
import os
import serial
import serial.tools.list_ports
import time
from loguru import logger

from config import Config
from logger import setup_logger
from keyboard_mac import KeyboardController

config = None
keyboard = None

def detect_serial_ports():
    """Detect available serial ports."""
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        logger.error("No serial ports found.")
        return []
    
    logger.info("Available serial ports:")
    for i, port in enumerate(ports):
        logger.info(f"{i+1}: {port.device} - {port.description}")
    
    return [port.device for port in ports]

def connect_to_serial(port, baud_rate=9600, timeout=1):
    """Connect to a serial port."""
    try:
        ser = serial.Serial(port, baud_rate, timeout=timeout)
        logger.info(f"Connected to {port} at {baud_rate} baud")
        return ser
    except serial.SerialException as e:
        logger.error(f"Error connecting to {port}: {e}")
        return None

def decode_shift_jis(data):
    """Decode Shift_JIS encoded data."""
    if data.startswith(b'\xe3'):
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            pass
    
    try:
        return data.decode('shift_jis')
    except UnicodeDecodeError:
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            return ' '.join([f'{b:02x}' for b in data])

def read_serial_data(ser):
    """Read data from serial port and decode it."""
    if ser.in_waiting:
        data = ser.read(ser.in_waiting)
        if data:
            decoded = decode_shift_jis(data)
            logger.info(f"Received: {decoded}")
            return decoded
    return None

def process_qr_data(data):
    """Process QR code data and simulate keyboard input."""
    if not data:
        return
    
    if keyboard:
        if config.get("keyboard", "type_delay", 0) > 0:
            keyboard.type_with_delay(data, config.get("keyboard", "type_delay", 0.05))
        else:
            keyboard.type_string(data)
        
        if config.get("keyboard", "press_enter_after", False):
            keyboard.press_enter()
    else:
        logger.warning("Keyboard controller not initialized, cannot type data")

def main():
    """Main function to run the QR2Key application."""
    global config, keyboard
    
    setup_logger(log_level="INFO", log_dir="logs")
    logger.info("QR2Key - QR Code Reader to Keyboard Input (Milestone M1)")
    
    config = Config("config.json")
    
    keyboard = KeyboardController()
    
    ports = detect_serial_ports()
    if not ports:
        logger.error("No serial ports available. Exiting.")
        sys.exit(1)
    
    if len(ports) == 1:
        port = ports[0]
        logger.info(f"Using the only available port: {port}")
    else:
        logger.info("Multiple ports available:")
        for i, p in enumerate(ports):
            print(f"{i+1}: {p}")
        
        try:
            selection = int(input("Select a port (number): "))
            port = ports[selection - 1]
            logger.info(f"Selected port: {port}")
        except (ValueError, IndexError):
            logger.error("Invalid selection. Exiting.")
            sys.exit(1)
    
    baud_rate = config.get("serial", "baud_rate", 9600)
    timeout = config.get("serial", "timeout", 1)
    ser = connect_to_serial(port, baud_rate, timeout)
    if not ser:
        logger.error("Failed to connect to serial port. Exiting.")
        sys.exit(1)
    
    logger.info("Listening for QR code data. Press Ctrl+C to exit.")
    
    try:
        while True:
            data = read_serial_data(ser)
            if data:
                process_qr_data(data)
            time.sleep(0.1)  # Small delay to prevent CPU hogging
    except KeyboardInterrupt:
        logger.info("Received interrupt signal. Exiting...")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()
            logger.info(f"Disconnected from {port}")

if __name__ == "__main__":
    main()
