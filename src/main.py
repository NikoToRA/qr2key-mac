"""
QR2Key - QR Code Reader to Keyboard Input
Milestone M3: macOS GUI + App Packaging
"""

import sys
import os
import serial
import serial.tools.list_ports
import time
import threading
from loguru import logger

try:
    from PyQt5.QtWidgets import QApplication
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

from config import Config
from logger import setup_logger
from keyboard_mac import KeyboardController

try:
    from port_detector import PortDetector
    PORT_DETECTOR_AVAILABLE = True
except ImportError:
    PORT_DETECTOR_AVAILABLE = False

try:
    from gui import QR2KeyGUI
    from auto_start import toggle_auto_start, is_auto_start_enabled
    AUTO_START_AVAILABLE = True
except ImportError:
    AUTO_START_AVAILABLE = False

config = None
keyboard = None
serial_connection = None
is_running = True
is_paused = False
app_version = "1.0.0"

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
    global serial_connection
    
    try:
        ser = serial.Serial(port, baud_rate, timeout=timeout)
        logger.info(f"Connected to {port} at {baud_rate} baud")
        serial_connection = ser
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

def serial_reader_thread():
    """Thread function to read from serial port."""
    global serial_connection
    
    while is_running:
        if serial_connection and serial_connection.is_open and not is_paused:
            try:
                data = read_serial_data(serial_connection)
                if data:
                    process_qr_data(data)
            except Exception as e:
                logger.error(f"Error reading serial data: {e}")
        
        time.sleep(0.1)  # Small delay to prevent CPU hogging

def port_monitor_callback(port):
    """Callback function for port monitor."""
    global serial_connection
    
    if serial_connection and serial_connection.is_open:
        logger.info(f"Already connected to {serial_connection.port}, ignoring new port {port}")
        return
    
    logger.info(f"New port detected: {port}, attempting to connect")
    baud_rate = config.get("serial", "baud_rate", 9600)
    timeout = config.get("serial", "timeout", 1)
    connect_to_serial(port, baud_rate, timeout)
    
    if 'gui_window' in globals() and gui_window:
        gui_window.update_port_status(port)

def port_monitor_thread():
    """Thread function to monitor for new serial ports."""
    if not config.get("serial", "monitor_ports", True):
        logger.info("Port monitoring disabled in config")
        return
    
    detector = PortDetector()
    detector.monitor_ports(port_monitor_callback)

def handle_toggle_pause(paused):
    """Handle pause/resume signal from GUI."""
    global is_paused
    is_paused = paused
    logger.info(f"QR2Key {'paused' if is_paused else 'resumed'}")

def handle_exit():
    """Handle exit signal from GUI."""
    global is_running
    is_running = False
    
    if serial_connection and serial_connection.is_open:
        serial_connection.close()
        logger.info(f"Disconnected from {serial_connection.port}")
    
    logger.info("QR2Key exiting")
    sys.exit(0)

def main():
    """Main function to run the QR2Key application."""
    global config, keyboard, serial_connection, gui_window
    
    setup_logger(log_level="INFO", log_dir="logs")
    logger.info(f"QR2Key v{app_version} - Starting application")
    
    config = Config("config.json")
    
    keyboard = KeyboardController()
    
    if 'unittest' in sys.modules or not GUI_AVAILABLE:
        logger.info("Running in test mode or GUI not available")
        
        ports = detect_serial_ports()
        if ports:
            port = ports[0]
            logger.info(f"Using first available port: {port}")
            baud_rate = config.get("serial", "baud_rate", 9600)
            timeout = config.get("serial", "timeout", 1)
            connect_to_serial(port, baud_rate, timeout)
        
        if 'unittest' in sys.modules:
            return
        
        try:
            while True:
                if serial_connection and serial_connection.is_open:
                    data = read_serial_data(serial_connection)
                    if data:
                        process_qr_data(data)
                time.sleep(0.1)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal. Exiting...")
        return
    
    app = QApplication(sys.argv)
    gui_window = QR2KeyGUI(config, app_version)
    gui_window.toggle_signal.connect(handle_toggle_pause)
    gui_window.exit_signal.connect(handle_exit)
    
    if PORT_DETECTOR_AVAILABLE and config.get("serial", "auto_detect", True):
        logger.info("Auto-detecting serial port")
        detector = PortDetector()
        port = detector.auto_detect_port()
        if port:
            logger.info(f"Auto-detected port: {port}")
            baud_rate = config.get("serial", "baud_rate", 9600)
            timeout = config.get("serial", "timeout", 1)
            connect_to_serial(port, baud_rate, timeout)
            gui_window.update_port_status(port)
        else:
            logger.warning("No ports detected automatically")
            gui_window.update_port_status("Not connected")
    else:
        port = config.get("serial", "port", None)
        if port:
            logger.info(f"Using configured port: {port}")
            baud_rate = config.get("serial", "baud_rate", 9600)
            timeout = config.get("serial", "timeout", 1)
            connect_to_serial(port, baud_rate, timeout)
            gui_window.update_port_status(port)
        else:
            logger.warning("No port configured")
            gui_window.update_port_status("Not connected")
    
    serial_thread = threading.Thread(target=serial_reader_thread, daemon=True)
    serial_thread.start()
    
    if PORT_DETECTOR_AVAILABLE and config.get("serial", "monitor_ports", True):
        monitor_thread = threading.Thread(target=port_monitor_thread, daemon=True)
        monitor_thread.start()
    
    if AUTO_START_AVAILABLE and config.get("app", "auto_start", False) != is_auto_start_enabled():
        toggle_auto_start(config.get("app", "auto_start", False))
    
    if not config.get("app", "start_minimized", False):
        gui_window.show()
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
