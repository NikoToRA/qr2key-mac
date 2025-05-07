# QR2Key

QR2Key is a macOS application that reads QR codes from a serial device and outputs the content as keyboard input.

## Milestone M2: Tray + Auto Port Detect

This milestone implements system tray functionality and automatic port detection.

### Features

- Serial port detection and connection
- Shift_JIS character encoding support
- Keyboard input simulation for macOS
- Configuration file management
- Logging with rotation
- System tray with Pause/Resume and Exit options
- Automatic port detection and monitoring

### Requirements

- Python 3.6 or higher
- Dependencies:
  - pyserial: Serial port communication
  - pynput: Keyboard input simulation
  - loguru: Advanced logging
  - pystray: System tray functionality
  - pillow: Image processing for tray icon

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
1. Create a default configuration file (`config.json`) if it doesn't exist
2. Set up logging to the `logs` directory with daily rotation
3. Automatically detect and connect to a compatible serial port
4. Create a system tray icon with Pause/Resume and Exit options
5. Listen for QR code data and simulate keyboard input
6. Monitor for new serial ports and automatically connect when detected

### System Tray

The application runs in the system tray with the following options:
- **Pause/Resume**: Toggle between pausing and resuming QR code processing
- **Exit**: Close the application

### Automatic Port Detection

The application can automatically detect and connect to compatible serial ports:
- Detects common USB-Serial adapters (FTDI, CP210x, CH340, PL2303)
- Monitors for new ports and automatically connects when detected
- Configurable through the `config.json` file

### Testing Results

The application has been successfully tested on macOS:
- QR code scanning with USB serial device (/dev/cu.usbserial-1140)
- Japanese (Shift-JIS) character input works correctly
- Automatic port detection and reconnection functions as expected
- System tray integration with pause/resume functionality verified

### Configuration

The application uses a JSON configuration file (`config.json`) with the following structure:

```json
{
    "serial": {
        "port": "/dev/cu.usbserial-1140",
        "baud_rate": 9600,
        "timeout": 1,
        "auto_detect": true,
        "monitor_ports": true,
        "monitor_interval": 2.0,
        "vendor_ids": ["0403", "10C4", "1A86", "067B"]
    },
    "keyboard": {
        "type_delay": 0.05,
        "press_enter_after": false
    },
    "app": {
        "start_minimized": false,
        "auto_start": false,
        "log_level": "INFO"
    }
}
```

### Logging

Logs are stored in the `logs` directory with the following features:
- Daily rotation
- 7-day retention
- Compressed archives of old logs
- Configurable log level

### Testing

Run the unit tests with:

```
python -m unittest discover -s src/tests
```

### Next Steps

Future milestones will add:
- Windows support
- Installer with CH340 driver
