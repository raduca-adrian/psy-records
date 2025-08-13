@echo off
REM Build script for Psychological Records Application using cx_Freeze
REM Make sure you have cx_Freeze installed: pip install cx_Freeze

echo Building Psychological Records Application with cx_Freeze...
echo.

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Clean previous builds
if exist "build" (
    echo Cleaning previous build directory...
    rmdir /s /q "build"
)
if exist "dist" (
    echo Cleaning previous dist directory...
    rmdir /s /q "dist"
)

echo Building with cx-Freeze...
echo Creating executable...
python config\setup.py build

if %ERRORLEVEL% neq 0 (
    echo Error occurred during build process!
    pause
    exit /b 1
)

echo.
echo Creating MSI installer...
python config\setup.py bdist_msi

if %ERRORLEVEL% neq 0 (
    echo Error occurred during MSI creation!
    pause
    exit /b 1
)

echo.
echo ============================================
echo BUILD SUCCESSFUL!
echo ============================================
echo Executable can be found in: build\exe.win-amd64-3.13\
echo MSI installer can be found in: dist\
echo.
echo You can now:
echo 1. Run the executable from the build directory
echo 2. Install using the MSI package from dist\
echo 3. Distribute the MSI file to end users
echo.
pause
