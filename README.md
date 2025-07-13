# Secure Database Application

A desktop application built with PyQt6 and SQLCipher for secure data management with user authentication.

## Features

- **Secure Database**: Uses SQLCipher for encrypted database storage
- **User Authentication**: Username/password authentication with bcrypt hashing
- **Person Management**: Add, edit, delete, and search persons with name and CNP
- **Password Management**: Change user passwords securely
- **Modern UI**: Clean and intuitive PyQt6 interface
- **Search Functionality**: Real-time search through person records
- **Data Validation**: CNP format validation for Romanian identification numbers

## Requirements

- Python 3.8 or higher
- Windows OS (for the packaged installer)

## Installation

### Method 1: Running from Source

1. Clone or download the source code
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```

### Method 2: Using the Installer (Recommended)

1. Download the MSI installer from the releases
2. Run the installer and follow the setup wizard
3. Launch the application from the Start Menu or Desktop shortcut

## First Time Setup

When you first run the application:

1. Click on the "Initial Setup" tab in the login dialog
2. Create a database password (at least 6 characters)
3. Create your username and password (at least 6 characters)
4. Click "Create Database & User"
5. Switch to the "Login" tab and log in with your credentials

## Usage

### Logging In

1. Enter your database password
2. Enter your username and password
3. Click "Login"

### Managing Persons

- **Add Person**: Click "Add Person" button or use Ctrl+N
- **Edit Person**: Select a person and click "Edit Person" or double-click the row
- **Delete Person**: Select a person and click "Delete Person"
- **Search**: Use the search box to filter by name or CNP

### Changing Password

1. Go to Account → Change Password in the menu
2. Enter your current password
3. Enter and confirm your new password
4. Click "Change Password"

## CNP Validation

The application validates Romanian CNP (Cod Numeric Personal) format:
- Must be exactly 13 digits
- First digit must be 1-8 (indicating century and gender)
- Only numeric characters allowed

## Security Features

- **Database Encryption**: SQLCipher provides transparent 256-bit AES encryption
- **Password Hashing**: User passwords are hashed using bcrypt with salt
- **Input Validation**: All inputs are validated before database operations
- **Session Management**: Database connections are properly managed and closed

## Building from Source

### Using cx-Freeze (Recommended for installers)

```bash
# Build executable
python setup.py build

# Create MSI installer
python setup.py bdist_msi
```

Or use the batch file:
```bash
build_cx_freeze.bat
```

### Using PyInstaller

```bash
pyinstaller SecureApp.spec
```

Or use the batch file:
```bash
build_pyinstaller.bat
```

## File Structure

```
SecureApp/
├── main.py                    # Application entry point
├── database.py               # Database management class
├── login_dialog.py           # Login and setup dialog
├── main_window.py            # Main application window
├── person_dialog.py          # Add/edit person dialog
├── change_password_dialog.py # Change password dialog
├── setup.py                  # cx-Freeze build configuration
├── SecureApp.spec            # PyInstaller build configuration
├── requirements.txt          # Python dependencies
├── build_cx_freeze.bat       # Build script for cx-Freeze
├── build_pyinstaller.bat     # Build script for PyInstaller
└── README.md                 # This file
```

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `password_hash`: bcrypt hashed password
- `created_at`: Creation timestamp

### Persons Table
- `id`: Primary key
- `name`: Full name
- `cnp`: Romanian CNP (unique)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Troubleshooting

### Common Issues

1. **Database connection failed**: Check if the database password is correct
2. **CNP validation error**: Ensure CNP is exactly 13 digits and starts with 1-8
3. **Application won't start**: Check if all dependencies are installed

### Support

For technical support or bug reports, please contact the development team.

## License

This application is proprietary software. All rights reserved.

## Version History

- **v1.0.0**: Initial release with core functionality
  - SQLCipher database integration
  - User authentication system
  - Person management CRUD operations
  - Modern PyQt6 interface
  - Windows installer support
