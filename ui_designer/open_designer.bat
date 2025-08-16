@echo off
echo 🎨 Starting Qt Designer for Psychological Records UI
echo.

cd /d "%~dp0forms"

echo 📁 Working directory: %CD%
echo 🛠️ Starting Qt Designer...
echo.

REM Try PySide6 Designer first (most reliable)
if exist "..\..\.venv\Scripts\pyside6-designer.exe" (
    echo ✅ Using PySide6 Designer
    "..\..\.venv\Scripts\pyside6-designer.exe"
) else if exist "..\..\.venv\Scripts\pyqt6-tools.exe" (
    echo ✅ Using PyQt6 Tools Designer
    "..\..\.venv\Scripts\pyqt6-tools.exe" designer
) else (
    echo ⚠️ Trying system Designer
    designer
)

if errorlevel 1 (
    echo.
    echo ❌ Qt Designer could not be started.
    echo 💡 Install with: pip install PySide6
    echo 💡 Or install Qt Creator from: https://www.qt.io/download
    echo.
    pause
)
