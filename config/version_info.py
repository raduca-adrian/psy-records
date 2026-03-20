# Psychological Records Application
# Version Information

APP_NAME = "Psychological Records"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Psychological Records Team"
APP_AUTHOR_EMAIL = "support@psychrecords.com"
APP_URL = "https://github.com/yourorg/psychological-records"
APP_DESCRIPTION = "Secure Psychological Records Management Application"
APP_LICENSE = "MIT"

# Build configuration
BUILD_DATE = "2025-08-06"
BUILD_TARGET = "Windows"
PYTHON_VERSION = "3.14.3"

# Dependencies
REQUIRED_PACKAGES = [
    "PyQt6>=6.7.1",
    "cryptography>=45.0.0", 
    "bcrypt>=4.2.1"
]

BUILD_PACKAGES = [
    "pyinstaller>=6.11.1",
    "cx-Freeze>=7.2.4"
]
