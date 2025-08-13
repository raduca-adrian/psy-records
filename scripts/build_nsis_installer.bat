@echo off
REM Build NSIS installer for Psychological Records Application
REM Requires NSIS to be installed: https://nsis.sourceforge.io/

echo Building NSIS Installer for Psychological Records...
echo.

REM Check if NSIS is installed
where makensis >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: NSIS not found in PATH!
    echo Please install NSIS from: https://nsis.sourceforge.io/
    echo And make sure makensis.exe is in your system PATH.
    echo.
    pause
    exit /b 1
)

REM Check if PyInstaller build exists
if not exist "dist\PsychologicalRecords\PsychologicalRecords.exe" (
    echo ERROR: PyInstaller build not found!
    echo Please run build_pyinstaller.bat first to create the application.
    echo.
    pause
    exit /b 1
)

REM Create the installer
echo Compiling NSIS installer...
makensis config\PsychologicalRecords.nsi

REM Check if installer was created successfully
if exist "PsychologicalRecords-Setup-1.0.0.exe" (
    echo.
    echo ============================================
    echo INSTALLER BUILD SUCCESSFUL!
    echo ============================================
    echo Installer created: PsychologicalRecords-Setup-1.0.0.exe
    echo.
    echo You can now distribute this installer to end users.
    echo The installer will:
    echo - Install the application to Program Files
    echo - Create desktop and start menu shortcuts
    echo - Add uninstall entry to Windows Add/Remove Programs
    echo.
) else (
    echo.
    echo ============================================
    echo INSTALLER BUILD FAILED!
    echo ============================================
    echo Check the output above for error messages.
    echo.
)

pause
