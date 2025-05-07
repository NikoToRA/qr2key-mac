"""
QR2Key - QR Code Reader to Keyboard Input
Milestone M2: tray + auto port detect
"""

import sys
import os
import serial
import serial.tools.list_ports
import time
import threading
from loguru import logger

from config import Config
from logger import setup_logger
from keyboard_mac import KeyboardController
from port_detector import PortDetector
from tray import SystemTray

config = None
keyboard = None
serial_connection = None
is_running = True
is_paused = False

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

def connect_to_serial(port, baud_rate=9600, timeout=1):
    """Connect to a serial port."""
    global serial_connection
    
    try:
        if serial_connection and serial_connection.is_open:
            serial_connection.close()
            logger.info(f"Closed previous connection")
        
        serial_connection = serial.Serial(port, baud_rate, timeout=timeout)
        logger.info(f"Connected to {port} at {baud_rate} baud")
        return serial_connection
    except serial.SerialException as e:
        logger.error(f"Error connecting to {port}: {e}")
        return None

def read_serial_data(ser):
    """Read data from serial port and decode it."""
    if not ser or not ser.is_open:
        return None
        
    if ser.in_waiting:
        data = ser.read(ser.in_waiting)
        if data:
            decoded = decode_shift_jis(data)
            logger.info(f"Received: {decoded}")
            return decoded
    return None

def process_qr_data(data):
    """Process QR code data and simulate keyboard input."""
    if not data or is_paused:
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

def handle_new_port(port):
    """Handle a newly detected port."""
    logger.info(f"New port detected: {port}")
    
    if config and config.get("serial", "auto_detect", False):
        baud_rate = config.get("serial", "baud_rate", 9600)
        timeout = config.get("serial", "timeout", 1)
        connect_to_serial(port, baud_rate, timeout)

def exit_application():
    """Clean up and exit the application."""
    global is_running
    
    logger.info("Exiting application...")
    is_running = False
    
    if serial_connection and serial_connection.is_open:
        serial_connection.close()
        logger.info("Serial connection closed")
    
    sys.exit(0)

def pause_application():
    """Pause the application."""
    global is_paused
    
    is_paused = True
    logger.info("Application paused")

def resume_application():
    """Resume the application."""
    global is_paused
    
    is_paused = False
    logger.info("Application resumed")

def serial_reader_thread():
    """Thread function to read from serial port."""
    global is_running, serial_connection
    
    logger.info("Serial reader thread started")
    
    while is_running:
        if serial_connection and not is_paused:
            data = read_serial_data(serial_connection)
            if data:
                process_qr_data(data)
        time.sleep(0.1)  # Small delay to prevent CPU hogging
    
    logger.info("Serial reader thread stopped")

def port_monitor_thread():
    """Thread function to monitor for new ports."""
    global is_running, config
    
    logger.info("Port monitor thread started")
    
    vendor_ids = config.get("serial", "vendor_ids", [])
    product_ids = config.get("serial", "product_ids", [])
    descriptions = config.get("serial", "descriptions", [])
    
    detector = PortDetector(vendor_ids, product_ids, descriptions)
    
    if config.get("serial", "auto_detect", False):
        port = detector.auto_detect_port()
        if port:
            baud_rate = config.get("serial", "baud_rate", 9600)
            timeout = config.get("serial", "timeout", 1)
            connect_to_serial(port, baud_rate, timeout)
    
    if config.get("serial", "monitor_ports", False):
        interval = config.get("serial", "monitor_interval", 2.0)
        
        while is_running:
            try:
                current_ports = detector.find_ports()
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Error in port monitoring: {e}")
                time.sleep(interval)
    
    logger.info("Port monitor thread stopped")

def main():
    """Main function to run the QR2Key application."""
    global config, keyboard, is_running
    
    log_level = os.environ.get("QR2KEY_LOG_LEVEL", "INFO")
    setup_logger(log_level=log_level, log_dir="logs")
    logger.info("QR2Key - QR Code Reader to Keyboard Input (Milestone M2)")
    
    config = Config("config.json")
    
    if "auto_detect" not in config.config["serial"]:
        config.config["serial"]["auto_detect"] = True
        config.config["serial"]["monitor_ports"] = True
        config.config["serial"]["monitor_interval"] = 2.0
        config.config["serial"]["vendor_ids"] = ["0403", "10C4", "1A86", "067B"]  # Common USB-Serial adapters
        config.save_config()
        logger.info("Updated configuration with auto-detection settings")
    
    keyboard = KeyboardController()
    
    reader_thread = threading.Thread(target=serial_reader_thread, daemon=True)
    reader_thread.start()
    
    monitor_thread = threading.Thread(target=port_monitor_thread, daemon=True)
    monitor_thread.start()
    
    tray = SystemTray(app_name="QR2Key")
    tray.setup(
        exit_callback=exit_application,
        pause_callback=pause_application,
        resume_callback=resume_application
    )
    
    try:
        tray.run()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    finally:
        exit_application()

if __name__ == "__main__":
    main()
