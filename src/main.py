"""
QR2Key - QR Code Reader to Keyboard Input
Milestone M0: macOS serial → print with Shift_JIS decode support
"""

import sys
import serial
import serial.tools.list_ports
import time

def detect_serial_ports():
    """Detect available serial ports."""
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("No serial ports found.")
        return []
    
    print("Available serial ports:")
    for i, port in enumerate(ports):
        print(f"{i+1}: {port.device} - {port.description}")
    
    return [port.device for port in ports]

def connect_to_serial(port, baud_rate=9600):
    """Connect to a serial port."""
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Connected to {port} at {baud_rate} baud")
        return ser
    except serial.SerialException as e:
        print(f"Error connecting to {port}: {e}")
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
            print(f"Received: {decoded}")
            return decoded
    return None

def main():
    """Main function to run the QR2Key application."""
    print("QR2Key - QR Code Reader to Keyboard Input (Milestone M0)")
    
    ports = detect_serial_ports()
    if not ports:
        sys.exit(1)
    
    if len(ports) == 1:
        port = ports[0]
    else:
        try:
            selection = int(input("Select a port (number): "))
            port = ports[selection - 1]
        except (ValueError, IndexError):
            print("Invalid selection. Exiting.")
            sys.exit(1)
    
    ser = connect_to_serial(port)
    if not ser:
        sys.exit(1)
    
    print("Listening for QR code data. Press Ctrl+C to exit.")
    
    try:
        while True:
            read_serial_data(ser)
            time.sleep(0.1)  # Small delay to prevent CPU hogging
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        if ser and ser.is_open:
            ser.close()
            print(f"Disconnected from {port}")

if __name__ == "__main__":
    main()
