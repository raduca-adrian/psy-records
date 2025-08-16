#!/usr/bin/env python3
"""
Psychological Records Application

Secure application for managing psychological records.
Ensures only encrypted databases are used for security.
"""

import os
import sys
from typing import Optional

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QColor, QIcon, QPainter, QPixmap, QPolygon
from PyQt6.QtWidgets import QApplication, QMessageBox

from src.core.database import DatabaseManager
from src.ui.login_dialog import LoginDialog
from src.ui.main_window import MainWindow


def ensure_encrypted_database_only() -> None:
    """Ensure only encrypted database files are used for security."""
    # Remove any unencrypted database files for security
    unencrypted_files = [
        "secure_app.db",
        "database.db",
        "app.db",
        "psychological_records.db",
        "data/secure_app.db",  # Also check data directory
    ]

    for file in unencrypted_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"Security: Removed unencrypted database file: {file}")
            except Exception as e:
                print(f"Warning: Could not remove unencrypted file {file}: {e}")


class SecureApplication:
    """Main application class for the Psychological Records system."""

    def __init__(self) -> None:
        """Initialize the secure application."""
        # Security: Ensure only encrypted databases are used
        ensure_encrypted_database_only()

        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Psychological Records Application")
        self.app.setApplicationVersion("1.2.0")
        self.app.setOrganizationName("Psychological Practice Management")

        # Set application icon (create a simple programmatic icon)
        self.create_app_icon()

        # Set global style
        self.set_global_style()

        self.db_manager: Optional[DatabaseManager] = None
        self.main_window: Optional[MainWindow] = None

    def create_app_icon(self) -> None:
        """Create a simple application icon programmatically."""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw a security shield icon
        painter.setBrush(QColor(52, 152, 219))  # Blue color
        painter.setPen(QColor(41, 128, 185))

        # Shield shape
        points = [
            (32, 5),  # Top center
            (50, 15),  # Top right
            (50, 40),  # Middle right
            (32, 58),  # Bottom center
            (14, 40),  # Middle left
            (14, 15),  # Top left
        ]

        polygon = QPolygon([QPoint(x, y) for x, y in points])
        painter.drawPolygon(polygon)

        # Add a lock symbol
        painter.setBrush(Qt.GlobalColor.white)
        painter.setPen(Qt.GlobalColor.white)
        painter.drawEllipse(26, 22, 12, 12)
        painter.setBrush(QColor(52, 152, 219))
        painter.drawEllipse(28, 24, 8, 8)
        painter.setBrush(Qt.GlobalColor.white)
        painter.drawRect(24, 30, 16, 12)
        painter.setBrush(QColor(52, 152, 219))
        painter.drawRect(30, 34, 4, 4)

        painter.end()

        icon = QIcon(pixmap)
        self.app.setWindowIcon(icon)

    def set_global_style(self) -> None:
        """Set global application style."""
        style = """
        QApplication {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
        }
        
        QMessageBox {
            background-color: #ecf0f1;
            color: #2c3e50;
        }
        
        QMessageBox QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 3px;
            font-weight: bold;
            min-width: 80px;
        }
        
        QMessageBox QPushButton:hover {
            background-color: #2980b9;
        }
        
        QMessageBox QPushButton:pressed {
            background-color: #21618c;
        }
        """
        self.app.setStyleSheet(style)

    def run(self) -> int:
        """Run the application."""
        try:
            # Show login dialog
            login_dialog = LoginDialog()

            def on_login_success(username: str) -> None:
                """Handle successful login."""
                self.db_manager = login_dialog.get_database_manager()
                self.main_window = MainWindow(self.db_manager, username)
                self.main_window.show()

            login_dialog.login_successful.connect(on_login_success)

            if login_dialog.exec() == LoginDialog.DialogCode.Accepted:
                # Main window is already shown via signal
                return self.app.exec()
            else:
                return 0

        except Exception as e:
            QMessageBox.critical(
                None, "Application Error", f"An unexpected error occurred:\n{str(e)}"
            )
            return 1


def main() -> int:
    """Main entry point."""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Set environment variable for better scaling on Windows
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = SecureApplication()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
