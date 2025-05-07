# QR2Key

QR2Key is a macOS application that reads QR codes from a serial device and outputs the content as keyboard input.

## Milestone M1: macOS Typing + Config/Log

This milestone implements keyboard typing functionality, configuration file support, and logging capabilities.

### Features

- Serial port detection and connection
- Shift_JIS character encoding support
- Keyboard input simulation for macOS
- Configuration file management
- Logging with rotation

### Requirements

- Python 3.6 or higher
- Dependencies:
  - pyserial: Serial port communication
  - pynput: Keyboard input simulation
  - loguru: Advanced logging

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
3. Detect available serial ports
4. Prompt you to select a port if multiple are available
5. Connect to the selected port
6. Listen for QR code data and simulate keyboard input

### Configuration

The application uses a JSON configuration file (`config.json`) with the following structure:

```json
{
    "serial": {
        "baud_rate": 9600,
        "timeout": 1,
        "auto_detect": false
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
- System tray integration
- Automatic port detection
- Windows support
