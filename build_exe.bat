@echo off
echo Building Psychological Records Application as Executable...
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo.
echo Building executable with PyInstaller...
pyinstaller --clean config\UnifiedApp.spec

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
    echo 2. Copy the entire dist\PsychologicalRecords folder for distribution
    echo 3. Create a zip package of the dist folder
    echo.
    
    REM Show file size
    for %%I in ("dist\PsychologicalRecords\PsychologicalRecords.exe") do echo Executable size: %%~zI bytes
    
) else (
    echo.
    echo ============================================
    echo BUILD FAILED!
    echo ============================================
    echo Check the output above for error messages.
    echo.
)

pause


