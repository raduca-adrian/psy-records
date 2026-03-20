@echo off
REM Test script for built Psychological Records Application

echo ============================================
echo Psychological Records - Application Tester
echo ============================================
echo.

set "TEST_PASSED=0"
set "TEST_FAILED=0"

echo Testing available builds...
echo.

REM Test PyInstaller build
echo [1/3] Testing PyInstaller build...
if exist "dist\PsychologicalRecords\PsychologicalRecords.exe" (
    echo   ✓ PyInstaller executable found
    
    REM Test if application starts (run for 3 seconds then close)
    echo   Testing application startup...
    timeout /t 1 >nul
    start "" "dist\PsychologicalRecords\PsychologicalRecords.exe"
    timeout /t 3 >nul
    taskkill /im "PsychologicalRecords.exe" /f >nul 2>nul
    echo   ✓ Application starts successfully
    set /a TEST_PASSED+=1
) else (
    echo   ✗ PyInstaller build not found
    set /a TEST_FAILED+=1
)

echo.

REM Test cx_Freeze build
echo [2/3] Testing cx_Freeze build...
if exist "build\exe.win-amd64-3.14\PsychologicalRecords.exe" (
    echo   ✓ cx_Freeze executable found
    
    REM Test if application starts
    echo   Testing application startup...
    timeout /t 1 >nul
    start "" "build\exe.win-amd64-3.14\PsychologicalRecords.exe"
    timeout /t 3 >nul
    taskkill /im "PsychologicalRecords.exe" /f >nul 2>nul
    echo   ✓ Application starts successfully
    set /a TEST_PASSED+=1
) else (
    echo   ✗ cx_Freeze build not found
    set /a TEST_FAILED+=1
)

echo.

REM Test MSI installer
echo [3/3] Testing MSI installer...
if exist "dist\*.msi" (
    echo   ✓ MSI installer package found
    for %%f in (dist\*.msi) do echo   File: %%f
    set /a TEST_PASSED+=1
) else (
    echo   ✗ MSI installer not found
    set /a TEST_FAILED+=1
)

echo.

REM Test NSIS installer
echo [Bonus] Testing NSIS installer...
if exist "PsychologicalRecords-Setup-1.0.0.exe" (
    echo   ✓ NSIS installer found
    echo   File: PsychologicalRecords-Setup-1.0.0.exe
) else (
    echo   ✗ NSIS installer not found
)

echo.
echo ============================================
echo TEST RESULTS
echo ============================================
echo Tests passed: %TEST_PASSED%
echo Tests failed: %TEST_FAILED%
echo.

if %TEST_FAILED% equ 0 (
    echo ✓ All builds are working correctly!
    echo Ready for distribution.
) else (
    echo ⚠ Some builds failed or are missing.
    echo Run the appropriate build scripts to create missing packages.
)

echo.
echo Distribution readiness:
if exist "dist\PsychologicalRecords\PsychologicalRecords.exe" (
    echo   ✓ Portable version ready
)
if exist "dist\*.msi" (
    echo   ✓ MSI installer ready
)
if exist "PsychologicalRecords-Setup-1.0.0.exe" (
    echo   ✓ NSIS installer ready
)

echo.
pause
