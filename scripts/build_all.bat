@echo off
REM Complete build script for Psychological Records Application
REM This script builds the application using multiple packaging methods

echo ============================================
echo Psychological Records - Complete Build
echo ============================================
echo.

REM Set build timestamp
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"

echo Build started at: %timestamp%
echo.

REM Check Python environment
python --version >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python and add it to your PATH.
    pause
    exit /b 1
)

REM Check if virtual environment exists and activate it
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    echo Virtual environment activated.
    echo.
)

REM Install/upgrade required packages
echo Installing required packages...
pip install -r requirements.txt
echo.

REM Create build output directory
if not exist "releases" (
    mkdir "releases"
)
set "RELEASE_DIR=releases\%timestamp%"
mkdir "%RELEASE_DIR%"

echo ============================================
echo 1. Building with PyInstaller...
echo ============================================

REM Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM Build with PyInstaller
pyinstaller --clean config\PsychologicalRecords.spec

if exist "dist\PsychologicalRecords\PsychologicalRecords.exe" (
    echo PyInstaller build: SUCCESS
    
    REM Copy PyInstaller build to releases
    xcopy "dist\PsychologicalRecords" "%RELEASE_DIR%\PyInstaller\" /E /I /Q
    
    REM Create zip archive
    powershell -command "Compress-Archive -Path 'dist\PsychologicalRecords\*' -DestinationPath '%RELEASE_DIR%\PsychologicalRecords-Portable-%timestamp%.zip'"
    echo Portable ZIP created: %RELEASE_DIR%\PsychologicalRecords-Portable-%timestamp%.zip
) else (
    echo PyInstaller build: FAILED
)

echo.
echo ============================================
echo 2. Building with cx_Freeze...
echo ============================================

REM Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM Build with cx_Freeze
python config\setup.py build
python config\setup.py bdist_msi

if exist "build\exe.win-amd64-3.14\PsychologicalRecords.exe" (
    echo cx_Freeze build: SUCCESS
    
    REM Copy cx_Freeze build to releases
    xcopy "build\exe.win-amd64-3.14" "%RELEASE_DIR%\cx_Freeze\" /E /I /Q
    
    REM Copy MSI installer
    if exist "dist\*.msi" (
        copy "dist\*.msi" "%RELEASE_DIR%\"
        echo MSI installer copied to releases directory
    )
) else (
    echo cx_Freeze build: FAILED
)

echo.
echo ============================================
echo 3. Building NSIS Installer...
echo ============================================

REM Check if NSIS is available
where makensis >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo NSIS not found - skipping installer creation
    echo Download NSIS from: https://nsis.sourceforge.io/
) else (
    REM Use PyInstaller build for NSIS installer
    if exist "dist\PsychologicalRecords\PsychologicalRecords.exe" (
        makensis config\PsychologicalRecords.nsi
        
        if exist "PsychologicalRecords-Setup-1.0.0.exe" (
            echo NSIS installer: SUCCESS
            move "PsychologicalRecords-Setup-1.0.0.exe" "%RELEASE_DIR%\"
        ) else (
            echo NSIS installer: FAILED
        )
    ) else (
        echo NSIS installer: SKIPPED (no PyInstaller build available)
    )
)

echo.
echo ============================================
echo BUILD SUMMARY
echo ============================================
echo Build completed at: %timestamp%
echo.
echo Release directory: %RELEASE_DIR%
echo.

if exist "%RELEASE_DIR%\PyInstaller\" (
    echo ✓ PyInstaller build available
)
if exist "%RELEASE_DIR%\cx_Freeze\" (
    echo ✓ cx_Freeze build available
)
if exist "%RELEASE_DIR%\*.msi" (
    echo ✓ MSI installer available
)
if exist "%RELEASE_DIR%\PsychologicalRecords-Setup-1.0.0.exe" (
    echo ✓ NSIS installer available
)
if exist "%RELEASE_DIR%\*.zip" (
    echo ✓ Portable ZIP available
)

echo.
echo Distribution options:
echo 1. Use the NSIS installer for end-user installation
echo 2. Use the MSI installer for enterprise deployment
echo 3. Use the portable ZIP for no-install usage
echo 4. Use the PyInstaller or cx_Freeze folders for manual distribution
echo.

pause
