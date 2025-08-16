# NSIS Installer Creator - Automated Setup and Build
# Downloads NSIS, installs it, and builds the installer

param(
    [switch]$SkipNSISInstall = $false,
    [switch]$ForceReinstall = $false
)

Write-Host "🚀 NSIS Installer Creation Tool" -ForegroundColor Yellow
Write-Host "===============================" -ForegroundColor Yellow

# Configuration
$NSISVersion = "3.10"
$NSISDownloadUrl = "https://downloads.sourceforge.net/project/nsis/NSIS%203/$NSISVersion/nsis-$NSISVersion-setup.exe"
$NSISInstaller = "nsis-$NSISVersion-setup.exe"
$NSISInstallPath = "C:\Program Files (x86)\NSIS"
$TempDir = $env:TEMP

function Test-NSISInstalled {
    # Check if NSIS is in PATH
    $nsisInPath = Get-Command "makensis" -ErrorAction SilentlyContinue
    if ($nsisInPath) {
        Write-Host "✅ NSIS found in PATH: $($nsisInPath.Source)" -ForegroundColor Green
        return $true
    }
    
    # Check common installation paths
    $commonPaths = @(
        "C:\Program Files (x86)\NSIS\makensis.exe",
        "C:\Program Files\NSIS\makensis.exe",
        "$env:ProgramFiles\NSIS\makensis.exe",
        "${env:ProgramFiles(x86)}\NSIS\makensis.exe"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            Write-Host "✅ NSIS found at: $path" -ForegroundColor Green
            # Add to PATH for this session
            $nsisDir = Split-Path $path -Parent
            $env:PATH += ";$nsisDir"
            return $true
        }
    }
    
    return $false
}

function Download-NSIS {
    Write-Host "📥 Downloading NSIS $NSISVersion..." -ForegroundColor Cyan
    
    $downloadPath = Join-Path $TempDir $NSISInstaller
    
    try {
        # Use Invoke-WebRequest to download
        Invoke-WebRequest -Uri $NSISDownloadUrl -OutFile $downloadPath -UseBasicParsing
        Write-Host "✅ NSIS downloaded successfully" -ForegroundColor Green
        return $downloadPath
    }
    catch {
        Write-Host "❌ Failed to download NSIS: $($_.Exception.Message)" -ForegroundColor Red
        
        # Try alternative download method using System.Net.WebClient
        Write-Host "🔄 Trying alternative download method..." -ForegroundColor Yellow
        try {
            $webClient = New-Object System.Net.WebClient
            $webClient.DownloadFile($NSISDownloadUrl, $downloadPath)
            $webClient.Dispose()
            Write-Host "✅ NSIS downloaded successfully (alternative method)" -ForegroundColor Green
            return $downloadPath
        }
        catch {
            Write-Host "❌ Alternative download also failed: $($_.Exception.Message)" -ForegroundColor Red
            return $null
        }
    }
}

function Install-NSIS {
    param([string]$InstallerPath)
    
    Write-Host "🔧 Installing NSIS..." -ForegroundColor Cyan
    
    try {
        # Run the installer silently
        $process = Start-Process -FilePath $InstallerPath -ArgumentList "/S" -Wait -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-Host "✅ NSIS installed successfully" -ForegroundColor Green
            
            # Add NSIS to PATH if not already there
            if (Test-Path $NSISInstallPath) {
                $currentPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::Machine)
                if ($currentPath -notlike "*$NSISInstallPath*") {
                    Write-Host "🔄 Adding NSIS to system PATH..." -ForegroundColor Yellow
                    [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$NSISInstallPath", [EnvironmentVariableTarget]::Machine)
                }
                # Add to current session PATH
                $env:PATH += ";$NSISInstallPath"
            }
            
            return $true
        }
        else {
            Write-Host "❌ NSIS installation failed with exit code: $($process.ExitCode)" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Error during NSIS installation: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Build-NSISInstaller {
    Write-Host "🔨 Building NSIS installer..." -ForegroundColor Cyan
    
    # Verify NSIS script exists
    if (-not (Test-Path "PsychologicalRecords_Setup.nsi")) {
        Write-Host "❌ NSIS script not found: PsychologicalRecords_Setup.nsi" -ForegroundColor Red
        return $false
    }
    
    # Verify required files exist
    $requiredFiles = @(
        "LICENSE.txt",
        "..\..\dist\PsychologicalRecords"
    )
    
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            Write-Host "⚠️ Warning: Required file/directory not found: $file" -ForegroundColor Yellow
        }
    }
    
    try {
        # Run NSIS compiler
        $process = Start-Process -FilePath "makensis" -ArgumentList "PsychologicalRecords_Setup.nsi" -Wait -PassThru -NoNewWindow
        
        if ($process.ExitCode -eq 0) {
            Write-Host "✅ NSIS installer built successfully!" -ForegroundColor Green
            
            # Check for output file
            $installerFiles = Get-ChildItem -Path "." -Filter "*.exe" | Where-Object { $_.Name -like "*Setup*" -or $_.Name -like "*Install*" }
            if ($installerFiles) {
                foreach ($installer in $installerFiles) {
                    Write-Host "🎉 Created installer: $($installer.FullName)" -ForegroundColor Green
                    Write-Host "📁 Size: $([math]::Round($installer.Length / 1MB, 2)) MB" -ForegroundColor Cyan
                }
            }
            
            return $true
        }
        else {
            Write-Host "❌ NSIS compilation failed with exit code: $($process.ExitCode)" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Error during NSIS compilation: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main execution
Write-Host "🔍 Checking NSIS installation..." -ForegroundColor Cyan

if ($ForceReinstall -or (-not (Test-NSISInstalled))) {
    if (-not $SkipNSISInstall) {
        Write-Host "📦 NSIS not found or force reinstall requested. Installing NSIS..." -ForegroundColor Yellow
        
        $downloadPath = Download-NSIS
        if ($downloadPath -and (Test-Path $downloadPath)) {
            $installSuccess = Install-NSIS -InstallerPath $downloadPath
            
            # Clean up downloaded installer
            try {
                Remove-Item $downloadPath -Force
                Write-Host "🧹 Cleaned up temporary installer file" -ForegroundColor Gray
            }
            catch {
                Write-Host "⚠️ Could not clean up temporary file: $downloadPath" -ForegroundColor Yellow
            }
            
            if (-not $installSuccess) {
                Write-Host "❌ NSIS installation failed. Cannot proceed with installer creation." -ForegroundColor Red
                exit 1
            }
        }
        else {
            Write-Host "❌ Could not download NSIS. Cannot proceed with installer creation." -ForegroundColor Red
            Write-Host "💡 Please manually download and install NSIS from: https://nsis.sourceforge.io/Download" -ForegroundColor Yellow
            exit 1
        }
    }
    else {
        Write-Host "❌ NSIS not found and installation was skipped." -ForegroundColor Red
        exit 1
    }
}

# Verify NSIS is now available
if (-not (Test-NSISInstalled)) {
    Write-Host "❌ NSIS still not available after installation attempt." -ForegroundColor Red
    exit 1
}

# Build the installer
Write-Host "`n🎯 Starting installer build process..." -ForegroundColor Yellow
$buildSuccess = Build-NSISInstaller

if ($buildSuccess) {
    Write-Host "`n🎊 SUCCESS! NSIS installer has been created!" -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host "Your Psychological Records Management System installer is ready!" -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor Green
    
    # List all created files
    Write-Host "`n📂 Files in release directory:" -ForegroundColor Cyan
    Get-ChildItem -Path "." | Format-Table Name, Length, LastWriteTime -AutoSize
    
    exit 0
}
else {
    Write-Host "`n❌ FAILED: Could not create NSIS installer." -ForegroundColor Red
    Write-Host "Please check the error messages above and try again." -ForegroundColor Red
    exit 1
}
