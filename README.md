# QR2Key

QR2Key is a macOS application that reads QR codes from a serial device and outputs the content as keyboard input.

## Milestone M3: macOS GUI + App Packaging

This milestone implements a GUI interface, app packaging, and auto-start functionality.

### Features

- Serial port detection and connection
- Shift_JIS character encoding support
- Keyboard input simulation for macOS
- Configuration file management
- Logging with rotation
- System tray with Pause/Resume and Exit options
- Automatic port detection and monitoring
- Simple GUI interface
- macOS app packaging (.app format)
- DMG installer
- Auto-start functionality

### Requirements

- macOS 10.13 or higher
- Dependencies (automatically included in the app package):
  - pyserial: Serial port communication
  - pynput: Keyboard input simulation
  - loguru: Advanced logging
  - PyQt5: GUI framework
  - py2app: macOS app packaging

### Installation

#### Option 1: DMG Installer

1. Download the `QR2Key_Installer.dmg` file
2. Open the DMG file
3. Drag the QR2Key app to the Applications folder
4. Launch QR2Key from the Applications folder

#### Option 2: From Source

1. Clone the repository:
   ```
   git clone https://github.com/NikoToRA/qr2key-mac.git
   cd qr2key-mac
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

4. (Optional) Build the app package:
   ```
   python setup.py py2app
   ```

5. (Optional) Build the DMG installer:
   ```
   python make_dmg.py
   ```

### Usage

The application provides a simple GUI interface with the following features:

- **Status Tab**: Shows the current connection status and controls
  - Port information
  - Pause/Resume button
  - Exit button

- **Settings Tab**: Displays the current configuration settings

- **About Tab**: Information about the application

The application also runs in the system tray with the following options:
- **Show/Hide**: Toggle the main window visibility
- **Pause/Resume**: Toggle between pausing and resuming QR code processing
- **Exit**: Close the application

### Automatic Port Detection

The application can automatically detect and connect to compatible serial ports:
- Detects common USB-Serial adapters (FTDI, CP210x, CH340, PL2303)
- Monitors for new ports and automatically connects when detected
- Configurable through the `config.json` file

### Auto-Start Functionality

The application can be configured to start automatically when you log in:
- Uses macOS LaunchAgents for reliable startup
- Can be enabled/disabled in the configuration file

### Testing Results

The application has been successfully tested on macOS:
- QR code scanning with USB serial device (/dev/cu.usbserial-1140)
- Japanese (Shift-JIS) character input works correctly
- Automatic port detection and reconnection functions as expected
- GUI and system tray integration work properly
- Auto-start functionality verified

### Configuration

The application uses a JSON configuration file (`config.json`) with the following structure:

```json
{
    "serial": {
        "port": "/dev/cu.usbserial-1140",
        "baud_rate": 9600,
        "timeout": 1,
        "auto_detect": true,
        "monitor_ports": true
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

### Building the Application

To build the macOS application package (.app):

```
python setup.py py2app
```

This will create a standalone application in the `dist` directory.

To create a DMG installer:

```
python make_dmg.py
```

This will create a DMG installer in the `dist` directory.

### Screenshots

![QR2Key GUI](resources/gui_screenshot.png)

*QR2Key GUI showing the status tab with connection information and controls*
