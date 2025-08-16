@echo off
echo Building NSIS Installer for Psychological Records Management System v1.0.0
echo.

REM Check if NSIS is installed
where makensis >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: NSIS (Nullsoft Scriptable Install System) is not installed or not in PATH.
    echo.
    echo Please install NSIS from: https://nsis.sourceforge.io/Download
    echo Make sure to add NSIS to your system PATH or run this from NSIS directory.
    echo.
    pause
    exit /b 1
)

echo NSIS found. Compiling installer...
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Compile the installer
makensis /V2 PsychologicalRecords_Setup.nsi

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS: Installer created successfully!
    echo ========================================
    echo.
    echo Output file: PsychologicalRecords-v1.0.0-Setup.exe
    echo.
    if exist "PsychologicalRecords-v1.0.0-Setup.exe" (
        for %%A in ("PsychologicalRecords-v1.0.0-Setup.exe") do (
            echo File size: %%~zA bytes
        )
    )
    echo.
    echo The installer is ready for distribution.
) else (
    echo.
    echo ========================================
    echo ERROR: Failed to create installer!
    echo ========================================
    echo.
    echo Please check the error messages above and fix any issues.
)

echo.
pause
