@echo off
echo Building Secure Database Application with PyInstaller...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo Building executable...
@echo off
REM Build script for Psychological Records Application using PyInstaller
REM Make sure you have PyInstaller installed: pip install pyinstaller

echo Building Psychological Records Application with PyInstaller...
echo.

REM Clean previous builds
if exist "build" (
    echo Cleaning previous build directory...
    rmdir /s /q "build"
)
if exist "dist" (
    echo Cleaning previous dist directory...
    rmdir /s /q "dist"
)

REM Build the application
echo Starting PyInstaller build...
pyinstaller --clean config\PsychologicalRecords.spec

REM Check if build was successful
if exist "dist\PsychologicalRecords\PsychologicalRecords.exe" (
    echo.
    echo ============================================
    echo BUILD SUCCESSFUL!
    echo ============================================
    echo Application built in: dist\PsychologicalRecords\
    echo Executable: PsychologicalRecords.exe
    echo.
    echo You can now:
    echo 1. Run the application directly from dist\PsychologicalRecords\
    echo 2. Create an installer using the NSIS script
    echo 3. Zip the dist\PsychologicalRecords folder for distribution
    echo.
) else (
    echo.
    echo ============================================
    echo BUILD FAILED!
    echo ============================================
    echo Check the output above for error messages.
    echo.
)

pause

if %ERRORLEVEL% neq 0 (
    echo Error occurred during build process!
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo.
echo Executable can be found in: dist\SecureApp\
echo.
pause
