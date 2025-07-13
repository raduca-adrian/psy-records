#!/usr/bin/env python3
"""
Psychological Records Application - Main Entry Point
Secure application for managing psychological records with Romanian/English support.
Only uses encrypted databases for security.
"""

import sys
import os
import argparse
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTranslator, QLocale
from PyQt6.QtGui import QIcon

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.translator import set_locale, _
from src.ui.login_dialog import LoginDialog
from src.ui.main_window import MainWindow


class PsychologicalRecordsApp:
    """Main application class for Psychological Records."""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        self.login_dialog = None
        self.locale = 'en'  # Default locale
        
    def setup_application(self):
        """Initialize the Qt application."""
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(_('app.title'))
        self.app.setApplicationVersion(_('app.version'))
        
        # Set application icon if it exists
        icon_path = os.path.join(os.path.dirname(__file__), 'app_icon.ico')
        if os.path.exists(icon_path):
            self.app.setWindowIcon(QIcon(icon_path))
    
    def detect_system_locale(self):
        """Detect system locale and set appropriate language."""
        system_locale = QLocale.system().name()
        
        # Check if Romanian locale
        if system_locale.startswith('ro'):
            self.locale = 'ro'
        else:
            self.locale = 'en'
        
        # Set the global locale
        set_locale(self.locale)
    
    def ensure_encrypted_database_only(self):
        """Ensure only encrypted database files are used."""
        # Remove any unencrypted database files for security
        unencrypted_files = [
            'secure_app.db',
            'database.db',
            'app.db'
        ]
        
        for file in unencrypted_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    print(f"Removed unencrypted database file: {file}")
                except Exception as e:
                    print(f"Warning: Could not remove {file}: {e}")
    
    def show_login(self):
        """Show the login dialog."""
        self.login_dialog = LoginDialog()
        
        def on_login_success(username):
            """Handle successful login."""
            self.show_main_window(username, self.login_dialog.get_database_manager())
            self.login_dialog.close()
        
        self.login_dialog.login_successful.connect(on_login_success)
        
        if self.login_dialog.exec():
            return True
        return False
    
    def show_main_window(self, username, db_manager):
        """Show the main application window."""
        self.main_window = MainWindow(db_manager, username)
        self.main_window.show()
    
    def run(self, locale=None):
        """Run the application."""
        try:
            # Set locale if provided
            if locale:
                self.locale = locale
                set_locale(locale)
            else:
                self.detect_system_locale()
            
            # Setup Qt application
            self.setup_application()
            
            # Security: Ensure only encrypted databases are used
            self.ensure_encrypted_database_only()
            
            # Show login dialog
            if self.show_login():
                # Start the main event loop
                return self.app.exec()
            else:
                return 0
                
        except Exception as e:
            # Show error message if possible
            if self.app:
                QMessageBox.critical(None, _('common.error'), 
                                   f"Application error: {str(e)}")
            else:
                print(f"Critical application error: {e}")
            return 1


def main():
    """Main entry point with command line argument support."""
    parser = argparse.ArgumentParser(
        description=_('app.title'),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--locale', '-l',
        choices=['en', 'ro'],
        help='Set application language (en=English, ro=Romanian)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'Psychological Records Application {_("app.version")}'
    )
    
    args = parser.parse_args()
    
    # Create and run the application
    app = PsychologicalRecordsApp()
    return app.run(locale=args.locale)


if __name__ == '__main__':
    sys.exit(main())
