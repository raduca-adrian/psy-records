from cx_Freeze import setup, Executable
import sys
import os

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["PyQt6", "bcrypt", "cryptography", "sqlite3", "json", "os"],
    "excludes": ["tkinter", "unittest", "email", "http", "urllib", "xml", "numpy", "matplotlib", "pandas"],
    "include_files": [
        # Application resources
        ("assets/app_icon.ico", "app_icon.ico"),
        ("assets/app_icon.png", "app_icon.png"),
        # Translation files
        ("locales/", "locales/"),
        # Source code modules
        ("src/", "src/"),
        # Main application files
        ("main.py", "main.py"),
    ],
    "zip_include_packages": ["PyQt6", "encodings", "importlib"],
    "optimize": 2,
}

# MSI options for Windows installer
bdist_msi_options = {
    "upgrade_code": "{12345678-1234-5678-9ABC-123456789012}",
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\Psychological Records",
    "install_icon": "assets/app_icon.ico",
    "summary_data": {
        "author": "Psychological Records Team",
        "comments": "Secure psychological records management application",
        "keywords": "psychology, records, database, secure",
    },
}

# Base for Windows GUI application
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Target executable
target = Executable(
    script="main.py",
    base=base,
    target_name="PsychologicalRecords.exe",
    icon="assets/app_icon.ico",  # Icon for the executable
    shortcut_name="Psychological Records",
    shortcut_dir="DesktopFolder",
)

setup(
    name="Psychological Records",
    version="1.0.0",
    description="Secure Psychological Records Management Application",
    author="Psychological Records Team",
    author_email="support@psychrecords.com",
    url="https://github.com/yourorg/psychological-records",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=[target],
)
