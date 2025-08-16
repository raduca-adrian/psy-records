# NSIS Installer Verification Script
# Checks if all required files are present for building the installer

Write-Host "NSIS Installer Build Verification" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Required files for installer build
$requiredFiles = @(
    "PsychologicalRecords_Setup.nsi",
    "LICENSE.txt",
    "README.md",
    "RELEASE_NOTES.md",
    "SHA256SUMS.txt",
    "dist\PsychologicalRecords\PsychologicalRecords.exe"
)

$missingFiles = @()
$presentFiles = @()

Write-Host "Checking required files..." -ForegroundColor Yellow
Write-Host ""

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        $sizeKB = [math]::Round($size / 1KB, 2)
        Write-Host "✅ $file ($sizeKB KB)" -ForegroundColor Green
        $presentFiles += $file
    }
    else {
        Write-Host "❌ $file (MISSING)" -ForegroundColor Red
        $missingFiles += $file
    }
}

Write-Host ""
Write-Host "Checking application directory structure..." -ForegroundColor Yellow
Write-Host ""

$appDir = "dist\PsychologicalRecords"
if (Test-Path $appDir) {
    $internalDir = "$appDir\_internal"
    if (Test-Path $internalDir) {
        $fileCount = (Get-ChildItem $internalDir -Recurse -File).Count
        $totalSize = (Get-ChildItem $internalDir -Recurse -File | Measure-Object Length -Sum).Sum
        $totalSizeMB = [math]::Round($totalSize / 1MB, 2)
        Write-Host "✅ Application _internal directory ($fileCount files, $totalSizeMB MB)" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Application _internal directory (MISSING)" -ForegroundColor Red
        $missingFiles += "$appDir\_internal"
    }
}

Write-Host ""
Write-Host "Checking NSIS availability..." -ForegroundColor Yellow
Write-Host ""

try {
    $nsisPath = Get-Command makensis -ErrorAction Stop
    Write-Host "✅ NSIS found at: $($nsisPath.Source)" -ForegroundColor Green
    
    # Get NSIS version
    $nsisVersion = & makensis /VERSION 2>$null
    if ($nsisVersion) {
        Write-Host "   Version: $nsisVersion" -ForegroundColor Gray
    }
}
catch {
    Write-Host "❌ NSIS not found in PATH" -ForegroundColor Red
    Write-Host "   Install from: https://nsis.sourceforge.io/Download" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan

if ($missingFiles.Count -eq 0) {
    Write-Host "🎉 BUILD READY: All required files are present!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To build the installer:" -ForegroundColor White
    Write-Host "  • Run: .\build_installer.ps1" -ForegroundColor Gray
    Write-Host "  • Or:  .\build_installer.bat" -ForegroundColor Gray
    Write-Host "  • Or:  makensis /V2 PsychologicalRecords_Setup.nsi" -ForegroundColor Gray
}
else {
    Write-Host "⚠️  BUILD NOT READY: Missing files detected!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Missing files:" -ForegroundColor Yellow
    foreach ($file in $missingFiles) {
        Write-Host "  • $file" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Summary:" -ForegroundColor White
Write-Host "  • Present files: $($presentFiles.Count)" -ForegroundColor Green
Write-Host "  • Missing files: $($missingFiles.Count)" -ForegroundColor Red

if ($missingFiles.Count -eq 0 -and (Get-Command makensis -ErrorAction SilentlyContinue)) {
    Write-Host "  • Status: ✅ Ready to build" -ForegroundColor Green
}
else {
    Write-Host "  • Status: ❌ Not ready" -ForegroundColor Red
}

Write-Host ""
