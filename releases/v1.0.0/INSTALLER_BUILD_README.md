# NSIS Installer Build Instructions

## Overview
This directory contains the NSIS (Nullsoft Scriptable Install System) installer script for the Psychological Records Management System v1.0.0.

## Prerequisites

### 1. Install NSIS
Download and install NSIS from: https://nsis.sourceforge.io/Download

**Recommended version**: NSIS 3.09 or later

**Installation options**:
- Choose "Full" installation to include all plugins
- Add NSIS to system PATH during installation

### 2. Verify Installation
Open Command Prompt or PowerShell and run:
```
makensis /?
```
You should see NSIS help information.

## Building the Installer

### Method 1: Using Batch File (Windows)
```batch
build_installer.bat
```

### Method 2: Using PowerShell
```powershell
.\build_installer.ps1
```

### Method 3: Manual Build
```batch
makensis /V2 PsychologicalRecords_Setup.nsi
```

## Output
The build process will create:
- **PsychologicalRecords-v1.0.0-Setup.exe** - The Windows installer

## Installer Features

### 🔧 Professional Installation
- Modern UI with branding
- Administrator privilege checking
- Windows 10+ compatibility verification
- Running application detection
- Component selection

### 📁 Installation Options
- **Core Application**: Main executable and runtime files (required)
- **Documentation**: User guides and release notes
- **Desktop Shortcut**: Quick access from desktop
- **Quick Launch Shortcut**: Taskbar quick launch

### 🛡️ Security Features
- Digital signature ready (requires code signing certificate)
- File integrity verification
- Secure uninstallation process
- User data preservation during uninstall

### 📋 Registry Integration
- Program registration in Windows
- File association for .prms files
- Start menu integration
- Add/Remove Programs entry

### 🗑️ Clean Uninstallation
- Removes all application files
- Cleans registry entries
- Preserves user data and settings
- Removes shortcuts and file associations

## File Structure
```
releases/v1.0.0/
├── PsychologicalRecords_Setup.nsi    # Main NSIS script
├── build_installer.bat               # Windows batch build script
├── build_installer.ps1               # PowerShell build script
├── LICENSE.txt                       # Software license for installer
├── INSTALLER_BUILD_README.md          # This file
├── dist/PsychologicalRecords/         # Application files to package
│   ├── PsychologicalRecords.exe
│   └── _internal/                     # Runtime dependencies
├── README.md                          # User documentation
├── RELEASE_NOTES.md                   # Release information
└── SHA256SUMS.txt                     # Checksums
```

## Installer Specifications

| Property | Value |
|----------|--------|
| **Compression** | LZMA (Solid, 32MB dictionary) |
| **Target Platform** | Windows 10/11 (64-bit) |
| **Installation Size** | ~50 MB |
| **Privileges Required** | Administrator |
| **Uninstaller** | Included |
| **Multi-language** | English (extensible) |

## Customization

### Branding
- Modify icon paths in the NSIS script
- Update company information in VIAddVersionKey sections
- Customize welcome and finish page text

### Components
- Add/remove sections in the installer script
- Modify file associations
- Add custom installation logic

### Signing (Optional)
To digitally sign the installer:
```batch
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com PsychologicalRecords-v1.0.0-Setup.exe
```

## Troubleshooting

### Common Issues

**NSIS not found**
- Ensure NSIS is installed and in system PATH
- Try running from NSIS installation directory

**Build fails with file not found**
- Verify all referenced files exist in correct paths
- Check that dist/PsychologicalRecords/ contains the application

**Permission denied**
- Run Command Prompt/PowerShell as Administrator
- Check file permissions in the build directory

**Large installer size**
- LZMA compression is already enabled for optimal size
- Consider excluding unnecessary files from _internal directory

## Testing the Installer

### Pre-deployment Testing
1. **Clean system test**: Test on clean Windows VM
2. **Upgrade test**: Install over previous version
3. **Uninstall test**: Verify clean removal
4. **Permission test**: Test with different user privileges
5. **Antivirus test**: Scan installer with multiple AV solutions

### Installation Validation
- ✅ Application launches successfully
- ✅ Start menu shortcuts work
- ✅ Desktop shortcut functions
- ✅ File associations work
- ✅ Uninstaller removes everything cleanly
- ✅ User data preserved during uninstall

## Distribution
The created installer is ready for:
- Direct download distribution
- CD/DVD burning
- USB drive deployment
- Network deployment via Group Policy
- Software distribution systems

---
*Last updated: August 13, 2025*
