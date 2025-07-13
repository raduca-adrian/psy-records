# Installation Guide

## Option 1: Running from Source (Development)

1. **Prerequisites:**
   - Python 3.8 or higher
   - Windows OS

2. **Setup:**
   ```bash
   # Navigate to the project directory
   cd d:\Code\testpy
   
   # Create virtual environment (if not already created)
   python -m venv .venv
   
   # Activate virtual environment
   .venv\Scripts\activate.bat
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```
   
   Or simply double-click `run_app.bat`

## Option 2: Building Executable (Production)

### Using cx-Freeze (Recommended for MSI installer)

1. **Build executable:**
   ```bash
   build_cx_freeze.bat
   ```
   
   Or manually:
   ```bash
   python setup.py build
   python setup.py bdist_msi
   ```

2. **Outputs:**
   - Executable: `build\exe.win-amd64-3.13\SecureApp.exe`
   - MSI Installer: `dist\SecureApp-1.0.0-amd64.msi`

### Using PyInstaller (Alternative)

1. **Build executable:**
   ```bash
   build_pyinstaller.bat
   ```
   
   Or manually:
   ```bash
   pyinstaller SecureApp.spec
   ```

2. **Output:**
   - Executable folder: `dist\SecureApp\`
   - Main executable: `dist\SecureApp\SecureApp.exe`

## Option 3: Installing via MSI (End Users)

1. Download the MSI installer (`SecureApp-1.0.0-amd64.msi`)
2. Double-click the MSI file
3. Follow the installation wizard
4. Launch from Start Menu: "Secure Database Application"

## First Time Usage

1. **Initial Setup:**
   - Run the application
   - Click "Initial Setup" tab
   - Create database password (min 6 characters)
   - Create username and password (min 6 characters)
   - Click "Create Database & User"

2. **Login:**
   - Switch to "Login" tab
   - Enter database password
   - Enter username and password
   - Click "Login"

3. **Start using:**
   - Add persons with name and CNP
   - Search and filter records
   - Edit or delete existing records
   - Change password from Account menu

## Troubleshooting

### Common Issues:

1. **"ModuleNotFoundError"**: Install missing dependencies with `pip install -r requirements.txt`

2. **"Database connection failed"**: Check database password and ensure database file isn't corrupted

3. **"CNP validation error"**: Ensure CNP is exactly 13 digits starting with 1-8

4. **Application won't start**: Check Python installation and dependencies

### Build Issues:

1. **cx-Freeze build fails**: Ensure all dependencies are installed and virtual environment is activated

2. **PyInstaller build fails**: Clear build cache with `pyinstaller --clean SecureApp.spec`

3. **Missing icon in build**: Ensure `app_icon.ico` exists in the project directory

## Support

For technical support, check the README.md file for detailed documentation.

## Security Notes

- Database files are encrypted using Fernet (symmetric encryption)
- User passwords are hashed with bcrypt
- Keep your database password safe - it cannot be recovered if lost
- Regular backups of the encrypted database file (.enc) are recommended
