from cx_Freeze import setup, Executable
import sys
import os

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["PyQt6", "bcrypt", "cryptography", "sqlite3"],
    "excludes": ["tkinter", "unittest", "email", "http", "urllib", "xml"],
    "include_files": [
        # Add any additional files that need to be included
        ("app_icon.ico", "app_icon.ico"),
    ],
    "zip_include_packages": ["PyQt6", "encodings", "importlib"],
    "optimize": 2,
}

# MSI options for Windows installer
bdist_msi_options = {
    "upgrade_code": "{12345678-1234-1234-1234-123456789012}",
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\SecureApp",
    "install_icon": "app_icon.ico",  # Icon for the installer
}

# Base for Windows GUI application
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Target executable
target = Executable(
    script="main.py",
    base=base,
    target_name="SecureApp.exe",
    icon="app_icon.ico",  # Icon for the executable
    shortcut_name="Secure Database Application",
    shortcut_dir="DesktopFolder",
)

setup(
    name="SecureApp",
    version="1.0.0",
    description="Secure Database Application with SQLCipher",
    author="SecureApp Corp",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=[target],
)
