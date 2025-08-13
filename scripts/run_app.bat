@echo off
echo Starting Secure Database Application...
echo.

REM Change to the application directory
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    python main.py
) else (
    REM Try to run with system Python
    python main.py
)

if %ERRORLEVEL% neq 0 (
    echo.
    echo Error: Application failed to start!
    echo Please ensure Python and all dependencies are installed.
    echo.
    pause
)
