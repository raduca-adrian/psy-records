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
pyinstaller SecureApp.spec

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
