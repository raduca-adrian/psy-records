# Build NSIS Installer for Psychological Records Management System v1.0.0
# PowerShell Build Script

Write-Host "Building NSIS Installer for Psychological Records Management System v1.0.0" -ForegroundColor Cyan
Write-Host ""

# Function to check if NSIS is installed
function Test-NSISInstalled {
    try {
        Get-Command makensis -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Check if NSIS is installed
if (-not (Test-NSISInstalled)) {
    Write-Host "ERROR: NSIS (Nullsoft Scriptable Install System) is not installed or not in PATH." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install NSIS from: https://nsis.sourceforge.io/Download" -ForegroundColor Yellow
    Write-Host "Make sure to add NSIS to your system PATH or run this from NSIS directory." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "NSIS found. Compiling installer..." -ForegroundColor Green
Write-Host ""

# Change to the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Compile the installer
try {
    $process = Start-Process -FilePath "makensis" -ArgumentList "/V2", "PsychologicalRecords_Setup.nsi" -Wait -NoNewWindow -PassThru
    
    if ($process.ExitCode -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "SUCCESS: Installer created successfully!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Output file: PsychologicalRecords-v1.0.0-Setup.exe" -ForegroundColor Cyan
        Write-Host ""
        
        if (Test-Path "PsychologicalRecords-v1.0.0-Setup.exe") {
            $fileSize = (Get-Item "PsychologicalRecords-v1.0.0-Setup.exe").Length
            $fileSizeMB = [math]::Round($fileSize / 1MB, 2)
            Write-Host "File size: $fileSize bytes ($fileSizeMB MB)" -ForegroundColor White
            
            # Generate checksum
            $hash = Get-FileHash "PsychologicalRecords-v1.0.0-Setup.exe" -Algorithm SHA256
            Write-Host "SHA256: $($hash.Hash)" -ForegroundColor White
        }
        
        Write-Host ""
        Write-Host "The installer is ready for distribution." -ForegroundColor Green
    }
    else {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Red
        Write-Host "ERROR: Failed to create installer!" -ForegroundColor Red
        Write-Host "========================================" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please check the error messages above and fix any issues." -ForegroundColor Yellow
    }
}
catch {
    Write-Host "ERROR: Failed to run makensis: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"
