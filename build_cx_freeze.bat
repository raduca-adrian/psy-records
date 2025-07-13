@echo off
echo Building Secure Database Application...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo Building with cx-Freeze...
echo Creating executable...
python setup.py build

if %ERRORLEVEL% neq 0 (
    echo Error occurred during build process!
    pause
    exit /b 1
)

echo.
echo Creating MSI installer...
python setup.py bdist_msi

if %ERRORLEVEL% neq 0 (
    echo Error occurred during MSI creation!
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo.
echo Executable can be found in: build\exe.win-amd64-3.13\
echo MSI installer can be found in: dist\
echo.
pause
