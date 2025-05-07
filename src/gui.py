"""
QR2Key - Simple macOS GUI
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGroupBox, QCheckBox, QSystemTrayIcon,
    QMenu, QAction, QStyle, QTabWidget, QTextEdit, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont

from loguru import logger
from config import Config

class QR2KeyGUI(QMainWindow):
    """Main GUI window for QR2Key application."""
    
    toggle_signal = pyqtSignal(bool)  # Signal for pause/resume
    exit_signal = pyqtSignal()  # Signal for exit
    
    def __init__(self, config, version="1.0.0"):
        """Initialize the GUI window."""
        super().__init__()
        
        self.config = config
        self.version = version
        self.is_paused = False
        
        self.setWindowTitle(f"QR2Key v{version}")
        self.setMinimumSize(500, 400)
        
        self.init_ui()
        self.setup_tray()
        
        if self.config.get("app", "start_minimized", False):
            self.hide()
        
        logger.info("GUI initialized")
    
    def init_ui(self):
        """Initialize the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        header_layout = QHBoxLayout()
        logo_label = QLabel()
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.blue)
        logo_label.setPixmap(pixmap)
        header_layout.addWidget(logo_label)
        
        title_label = QLabel(f"QR2Key v{self.version}")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
        tab_widget = QTabWidget()
        
        status_tab = QWidget()
        status_layout = QVBoxLayout(status_tab)
        
        status_group = QGroupBox("Status")
        status_group_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("Ready")
        status_group_layout.addWidget(self.status_label)
        
        self.port_label = QLabel(f"Port: {self.config.get('serial', 'port', 'Not connected')}")
        status_group_layout.addWidget(self.port_label)
        
        self.auto_detect_checkbox = QCheckBox("Auto-detect ports")
        self.auto_detect_checkbox.setChecked(self.config.get("serial", "auto_detect", True))
        self.auto_detect_checkbox.setEnabled(False)  # Read-only display
        status_group_layout.addWidget(self.auto_detect_checkbox)
        
        self.monitor_ports_checkbox = QCheckBox("Monitor for new ports")
        self.monitor_ports_checkbox.setChecked(self.config.get("serial", "monitor_ports", True))
        self.monitor_ports_checkbox.setEnabled(False)  # Read-only display
        status_group_layout.addWidget(self.monitor_ports_checkbox)
        
        status_layout.addWidget(status_group)
        
        controls_group = QGroupBox("Controls")
        controls_layout = QHBoxLayout(controls_group)
        
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.toggle_pause)
        controls_layout.addWidget(self.pause_button)
        
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        controls_layout.addWidget(exit_button)
        
        status_layout.addWidget(controls_group)
        status_layout.addStretch()
        
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        
        settings_text = QTextEdit()
        settings_text.setReadOnly(True)
        
        config_text = "# QR2Key Configuration\n\n"
        
        config_text += "## Serial Settings\n"
        for key, value in self.config.config["serial"].items():
            config_text += f"- {key}: {value}\n"
        
        config_text += "\n## Keyboard Settings\n"
        for key, value in self.config.config["keyboard"].items():
            config_text += f"- {key}: {value}\n"
        
        config_text += "\n## Application Settings\n"
        for key, value in self.config.config["app"].items():
            config_text += f"- {key}: {value}\n"
        
        settings_text.setMarkdown(config_text)
        settings_layout.addWidget(settings_text)
        
        about_tab = QWidget()
        about_layout = QVBoxLayout(about_tab)
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setMarkdown("""
        
        QR2Key is a macOS application that reads QR codes from a serial device and outputs the content as keyboard input.
        
        
        - Serial port detection and connection
        - Shift_JIS character encoding support
        - Keyboard input simulation for macOS
        - Configuration file management
        - Logging with rotation
        - System tray with Pause/Resume and Exit options
        - Automatic port detection and monitoring
        
        
        Copyright © 2025
        """)
        about_layout.addWidget(about_text)
        
        tab_widget.addTab(status_tab, "Status")
        tab_widget.addTab(settings_tab, "Settings")
        tab_widget.addTab(about_tab, "About")
        
        main_layout.addWidget(tab_widget)
    
    def setup_tray(self):
        """Set up the system tray icon and menu."""
        self.tray_icon = QSystemTrayIcon(self)
        
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        tray_menu = QMenu()
        
        self.show_action = QAction("Show", self)
        self.show_action.triggered.connect(self.show)
        tray_menu.addAction(self.show_action)
        
        self.pause_action = QAction("Pause", self)
        self.pause_action.triggered.connect(self.toggle_pause)
        tray_menu.addAction(self.pause_action)
        
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_activated)
        
        self.tray_icon.show()
    
    def tray_activated(self, reason):
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.activateWindow()
    
    def toggle_pause(self):
        """Toggle between pause and resume states."""
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self.pause_button.setText("Resume")
            self.pause_action.setText("Resume")
            self.status_label.setText("Paused")
        else:
            self.pause_button.setText("Pause")
            self.pause_action.setText("Pause")
            self.status_label.setText("Running")
        
        self.toggle_signal.emit(self.is_paused)
        logger.info(f"QR2Key {'paused' if self.is_paused else 'resumed'}")
    
    def update_port_status(self, port):
        """Update the port status display."""
        self.port_label.setText(f"Port: {port}")
    
    def closeEvent(self, event):
        """Handle window close event."""
        event.ignore()
        self.hide()
        
        if event.spontaneous():
            return
        
        self.tray_icon.hide()
        self.exit_signal.emit()
        QApplication.quit()

def run_gui(config):
    """Run the GUI application."""
    app = QApplication(sys.argv)
    window = QR2KeyGUI(config)
    
    if not config.get("app", "start_minimized", False):
        window.show()
    
    return app, window

if __name__ == "__main__":
    config = Config("config.json")
    app, window = run_gui(config)
    sys.exit(app.exec_())
