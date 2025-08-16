@echo off
echo 🔄 Converting UI files to Python
echo.

cd /d "%~dp0"

echo 📁 Working directory: %CD%
echo 🛠️ Running conversion...
echo.

REM Use Python from virtual environment
if exist "..\.venv\Scripts\python.exe" (
    "..\.venv\Scripts\python.exe" ui_tools.py convert
) else (
    REM Fallback to system Python
    python ui_tools.py convert
)

echo.
echo ✅ Conversion completed!
echo 💡 Generated Python files are in the forms/ directory
echo.
pause
