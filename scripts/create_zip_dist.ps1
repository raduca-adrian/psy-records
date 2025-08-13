# PowerShell script to create a ZIP distribution
$AppName = "SecureApp"
$Version = "1.0.0"
$BuildDir = "build\exe.win-amd64-3.13"
$DistDir = "dist"

Write-Host "Creating ZIP distribution for $AppName v$Version..."

# Create dist directory if it doesn't exist
if (!(Test-Path $DistDir)) {
    New-Item -ItemType Directory -Path $DistDir
}

# Create the ZIP file name
$ZipFileName = "$DistDir\${AppName}_v${Version}_Windows.zip"

# Remove existing ZIP if it exists
if (Test-Path $ZipFileName) {
    Remove-Item $ZipFileName
    Write-Host "Removed existing ZIP file"
}

# Create ZIP archive
try {
    Write-Host "Compressing files..."
    Compress-Archive -Path "$BuildDir\*" -DestinationPath $ZipFileName -CompressionLevel Optimal
    
    # Get file size
    $ZipSize = (Get-Item $ZipFileName).Length / 1MB
    
    Write-Host "ZIP distribution created successfully!"
    Write-Host "File: $ZipFileName"
    Write-Host "Size: $([math]::Round($ZipSize, 2)) MB"
    Write-Host ""
    Write-Host "Installation Instructions:"
    Write-Host "1. Extract the ZIP file to a folder"
    Write-Host "2. Run SecureApp.exe to start the application"
    Write-Host "3. Create a desktop shortcut if desired"
}
catch {
    Write-Error "Failed to create ZIP distribution"
    exit 1
}
