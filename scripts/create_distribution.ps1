# PowerShell script for creating distribution packages
# Psychological Records Application Distribution Creator

param(
    [string]$Version = "1.0.0",
    [string]$OutputDir = "releases"
)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Psychological Records - Distribution Creator" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Create output directory
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$releaseDir = Join-Path $OutputDir $timestamp
if (!(Test-Path $releaseDir)) {
    New-Item -ItemType Directory -Path $releaseDir -Force | Out-Null
}

Write-Host "Creating distribution packages..." -ForegroundColor Green
Write-Host "Output directory: $releaseDir" -ForegroundColor Yellow
Write-Host ""

# Create portable ZIP from PyInstaller build
if (Test-Path "dist\PsychologicalRecords") {
    Write-Host "[1/4] Creating portable ZIP package..." -ForegroundColor Green
    $zipPath = Join-Path $releaseDir "PsychologicalRecords-Portable-v$Version.zip"
    Compress-Archive -Path "dist\PsychologicalRecords\*" -DestinationPath $zipPath -Force
    Write-Host "  ✓ Created: $(Split-Path $zipPath -Leaf)" -ForegroundColor Green
} else {
    Write-Host "[1/4] ✗ PyInstaller build not found - skipping portable ZIP" -ForegroundColor Red
}

# Copy MSI installer
if (Test-Path "dist\*.msi") {
    Write-Host "[2/4] Copying MSI installer..." -ForegroundColor Green
    Get-ChildItem "dist\*.msi" | ForEach-Object {
        $newName = "PsychologicalRecords-Installer-v$Version.msi"
        Copy-Item $_.FullName -Destination (Join-Path $releaseDir $newName)
        Write-Host "  ✓ Created: $newName" -ForegroundColor Green
    }
} else {
    Write-Host "[2/4] ✗ MSI installer not found" -ForegroundColor Red
}

# Copy NSIS installer
if (Test-Path "PsychologicalRecords-Setup-$Version.exe") {
    Write-Host "[3/4] Copying NSIS installer..." -ForegroundColor Green
    $nsisPath = Join-Path $releaseDir "PsychologicalRecords-Setup-v$Version.exe"
    Copy-Item "PsychologicalRecords-Setup-$Version.exe" -Destination $nsisPath
    Write-Host "  ✓ Created: $(Split-Path $nsisPath -Leaf)" -ForegroundColor Green
} else {
    Write-Host "[3/4] ✗ NSIS installer not found" -ForegroundColor Red
}

# Create source code archive
Write-Host "[4/4] Creating source code archive..." -ForegroundColor Green
$sourceItems = @(
    "*.py",
    "src\",
    "locales\",
    "*.md",
    "*.txt",
    "*.spec",
    "*.nsi",
    "*.bat",
    "*.ps1",
    "app_icon.*"
)

$sourceZip = Join-Path $releaseDir "PsychologicalRecords-Source-v$Version.zip"
$tempDir = "temp_source"

# Create temporary directory for source files
if (Test-Path $tempDir) {
    Remove-Item $tempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

# Copy source files
foreach ($item in $sourceItems) {
    if (Test-Path $item) {
        if ($item.EndsWith("\")) {
            # Directory
            $dirName = $item.TrimEnd('\')
            Copy-Item $item -Destination (Join-Path $tempDir $dirName) -Recurse -Force
        } else {
            # Files
            Get-ChildItem $item | Copy-Item -Destination $tempDir -Force
        }
    }
}

# Create source archive
Compress-Archive -Path "$tempDir\*" -DestinationPath $sourceZip -Force
Remove-Item $tempDir -Recurse -Force
Write-Host "  ✓ Created: $(Split-Path $sourceZip -Leaf)" -ForegroundColor Green

# Create release notes
Write-Host ""
Write-Host "Creating release notes..." -ForegroundColor Green
$releaseNotes = @"
# Psychological Records v$Version - Release Package

Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## Package Contents

This release includes the following distribution packages:

### For End Users
- **PsychologicalRecords-Setup-v$Version.exe** - Professional Windows installer (recommended)
- **PsychologicalRecords-Installer-v$Version.msi** - MSI package for enterprise deployment
- **PsychologicalRecords-Portable-v$Version.zip** - Portable application (no installation required)

### For Developers
- **PsychologicalRecords-Source-v$Version.zip** - Complete source code and build scripts

## Installation Options

### Option 1: NSIS Installer (Recommended for most users)
1. Run ``PsychologicalRecords-Setup-v$Version.exe``
2. Follow the installation wizard
3. Application will be installed to Program Files with shortcuts

### Option 2: MSI Installer (Enterprise deployment)
1. Run ``PsychologicalRecords-Installer-v$Version.msi``
2. Suitable for Group Policy deployment
3. Integrates with Windows Add/Remove Programs

### Option 3: Portable Application
1. Extract ``PsychologicalRecords-Portable-v$Version.zip``
2. Run ``PsychologicalRecords.exe`` directly
3. No installation required - can run from USB drive

## System Requirements

- Windows 10/11 (64-bit)
- .NET Framework 4.8+ (usually pre-installed)
- Minimum 4GB RAM
- 100MB free disk space

## Features

- Secure encrypted database storage
- Multi-language support (English/Romanian)
- Professional user interface
- Comprehensive psychological records management
- PDF report generation
- User authentication and access control

## Support

For issues or questions, please check the included documentation or contact support.

---
Build Date: $(Get-Date -Format "yyyy-MM-dd")
Version: $Version
"@

$releaseNotesPath = Join-Path $releaseDir "README.txt"
$releaseNotes | Out-File -FilePath $releaseNotesPath -Encoding UTF8
Write-Host "  ✓ Created: README.txt" -ForegroundColor Green

# Summary
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "DISTRIBUTION SUMMARY" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

$createdFiles = Get-ChildItem $releaseDir
Write-Host "Created $($createdFiles.Count) files in: $releaseDir" -ForegroundColor Yellow
Write-Host ""

foreach ($file in $createdFiles) {
    $sizeKB = [math]::Round($file.Length / 1KB, 1)
    Write-Host "  📦 $($file.Name) ($sizeKB KB)" -ForegroundColor White
}

Write-Host ""
Write-Host "✓ Distribution packages ready for release!" -ForegroundColor Green
Write-Host ""
