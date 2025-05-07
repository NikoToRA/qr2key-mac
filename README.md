# QR2Key

QR2Key is a macOS application that reads QR codes from a serial device and outputs the content as keyboard input.

## Milestone M0: macOS Serial → Print

This milestone implements the basic functionality to read QR code data from a serial port and print it to the console, with support for Shift_JIS decoding.

### Features

- Serial port detection and connection
- Shift_JIS character encoding support
- Basic console output of scanned QR codes

### Requirements

- Python 3.6 or higher
- pyserial library

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/NikoToRA/qr2key-mac.git
   cd qr2key-mac
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Usage

Run the application with:

```
python src/main.py
```

The application will:
1. Detect available serial ports
2. Prompt you to select a port if multiple are available
3. Connect to the selected port
4. Listen for and display QR code data

### Testing

Run the unit tests with:

```
python -m unittest discover -s src/tests
```

### Next Steps

Future milestones will add:
- Keyboard input simulation
- Configuration options
- System tray integration
- Automatic port detection
