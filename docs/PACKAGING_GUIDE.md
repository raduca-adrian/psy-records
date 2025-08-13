# Psychological Records Application - Packaging & Distribution Guide

This guide explains how to package and distribute the Psychological Records application using multiple methods.

## 📋 Prerequisites

Before building the application, ensure you have:

1. **Python 3.11+** installed and added to PATH
2. **Required Python packages** (automatically installed by build scripts):
   ```
   PyQt6==6.7.1
   cryptography==45.0.0
   bcrypt==4.2.1
   pyinstaller==6.11.1
   cx-Freeze==7.2.4
   ```

3. **Optional tools for advanced packaging**:
   - [NSIS (Nullsoft Scriptable Install System)](https://nsis.sourceforge.io/) for Windows installers
   - Git for version control

## 🚀 Quick Start - Build Everything

The easiest way to create all distribution packages:

```batch
build_all.bat
```

This script will:
- ✅ Install required dependencies
- ✅ Build with PyInstaller (portable executable)
- ✅ Build with cx_Freeze (MSI installer)
- ✅ Create NSIS installer (professional installer)
- ✅ Generate ZIP archives
- ✅ Organize everything in timestamped release folders

## 📦 Individual Build Methods

### Method 1: PyInstaller (Recommended)

**Best for**: Portable applications, single-folder distribution

```batch
build_pyinstaller.bat
```

**Output**: `dist\PsychologicalRecords\` folder containing:
- `PsychologicalRecords.exe` - Main executable
- All required libraries and dependencies
- Application resources (icons, translations)

**Advantages**:
- ✅ Single folder contains everything
- ✅ No installation required
- ✅ Works on any Windows system
- ✅ Easy to distribute via ZIP

### Method 2: cx_Freeze

**Best for**: Professional MSI installers, enterprise deployment

```batch
build_cx_freeze.bat
```

**Output**:
- `build\exe.win-amd64-3.13\` - Executable folder
- `dist\*.msi` - Windows MSI installer package

**Advantages**:
- ✅ Professional MSI installer
- ✅ Integrates with Windows Add/Remove Programs
- ✅ Registry-based installation tracking
- ✅ Enterprise deployment friendly

### Method 3: NSIS Installer

**Best for**: Professional installation experience, custom installer features

```batch
build_nsis_installer.bat
```

**Prerequisites**: NSIS must be installed and in PATH

**Output**: `PsychologicalRecords-Setup-1.0.0.exe`

**Features**:
- ✅ Professional installer wizard
- ✅ Custom installation options
- ✅ Desktop and Start Menu shortcuts
- ✅ Proper uninstaller
- ✅ Version information and branding

## 📁 Build Output Structure

After running `build_all.bat`, you'll find organized releases:

```
releases/
└── YYYY-MM-DD_HH-MM-SS/
    ├── PyInstaller/              # Portable application folder
    ├── cx_Freeze/                # cx_Freeze build folder
    ├── *.msi                     # MSI installer package
    ├── PsychologicalRecords-Setup-1.0.0.exe  # NSIS installer
    └── PsychologicalRecords-Portable-*.zip   # Portable ZIP archive
```

## 🎯 Distribution Recommendations

### For End Users (Non-Technical)
**Use**: NSIS Installer (`PsychologicalRecords-Setup-1.0.0.exe`)
- Professional installation experience
- Automatic shortcuts and uninstaller
- Familiar Windows installer interface

### For Enterprise/IT Departments
**Use**: MSI Package (`*.msi`)
- Group Policy deployment support
- Silent installation options
- Enterprise management tools compatibility

### For Portable/USB Usage
**Use**: Portable ZIP (`PsychologicalRecords-Portable-*.zip`)
- No installation required
- Run from any location
- USB drive friendly

### For Developers/Testing
**Use**: PyInstaller folder (`PyInstaller/`)
- Direct access to all files
- Easy debugging and inspection
- Development environment friendly

## 🔧 Configuration Files

### PyInstaller Configuration
- **File**: `PsychologicalRecords.spec`
- **Purpose**: Defines what to include in the PyInstaller build
- **Key sections**: File paths, hidden imports, exclusions

### cx_Freeze Configuration
- **File**: `setup.py`
- **Purpose**: Controls cx_Freeze build and MSI creation
- **Key sections**: Package dependencies, MSI options, executable settings

### NSIS Configuration
- **File**: `PsychologicalRecords.nsi`
- **Purpose**: NSIS installer script with UI and installation logic
- **Key sections**: Installation components, shortcuts, registry entries

## 🐛 Troubleshooting

### Common Issues

**PyInstaller: "Module not found" errors**
- Solution: Add missing modules to `hiddenimports` in the .spec file

**cx_Freeze: MSI creation fails**
- Solution: Ensure you have administrator privileges
- Check that Visual C++ Redistributable is installed

**NSIS: "makensis not found"**
- Solution: Install NSIS and add to PATH
- Alternative: Use the MSI installer instead

**Missing translations or resources**
- Solution: Verify `include_files` and `datas` sections include all necessary folders

### Build Script Debugging

All build scripts include detailed output and error checking:
- Check console output for specific error messages
- Verify all prerequisites are installed
- Ensure virtual environment is properly activated

## 📝 Customization

### Changing Application Information

1. **Update version and metadata** in:
   - `setup.py` (cx_Freeze)
   - `PsychologicalRecords.nsi` (NSIS)
   - `PsychologicalRecords.spec` (PyInstaller)

2. **Add new files/resources**:
   - Add to `include_files` in `setup.py`
   - Add to `datas` in `PsychologicalRecords.spec`
   - Update NSIS script file copying section

3. **Modify installer behavior**:
   - Edit `PsychologicalRecords.nsi` for NSIS customization
   - Edit `bdist_msi_options` in `setup.py` for MSI customization

## 🔒 Security Notes

- The application includes encrypted database functionality
- All builds preserve encryption capabilities
- Distribute only through trusted channels
- Consider code signing for production releases

## 📞 Support

For build issues or questions:
1. Check the troubleshooting section above
2. Review build script output for specific errors
3. Verify all prerequisites are installed correctly
4. Test builds in a clean environment if problems persist

---

**Last Updated**: August 2025  
**Compatible With**: Windows 10/11, Python 3.11+
