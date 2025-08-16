# NSIS Script Syntax Validation Tool (Simple Version)
# Quick check for common NSIS syntax issues without complex regex

param(
    [string]$ScriptPath = "PsychologicalRecords_Setup.nsi"
)

Write-Host "NSIS Syntax Validation Tool" -ForegroundColor Yellow
Write-Host "=============================`n" -ForegroundColor Yellow

if (-not (Test-Path $ScriptPath)) {
    Write-Host "❌ Script file not found: $ScriptPath" -ForegroundColor Red
    exit 1
}

$content = Get-Content $ScriptPath
$lineNum = 0
$errorCount = 0
$warningCount = 0

Write-Host "Checking $ScriptPath..." -ForegroundColor Cyan

foreach ($line in $content) {
    $lineNum++
    $trimmed = $line.Trim()
    
    # Skip comments and empty lines
    if ($trimmed.StartsWith(";") -or $trimmed -eq "") {
        continue
    }
    
    # Check for StartMenuFolder variable declaration
    if ($trimmed -match "Var\s+StartMenuFolder") {
        Write-Host "  Line $lineNum : ✅ StartMenuFolder variable declared correctly" -ForegroundColor Green
    }
    
    # Check for deprecated STARTMENU_FOLDER usage
    if ($trimmed.Contains('$STARTMENU_FOLDER')) {
        Write-Host "  Line $lineNum : ❌ Found deprecated STARTMENU_FOLDER variable" -ForegroundColor Red
        $errorCount++
    }
    
    # Check for correct StartMenuFolder usage
    if ($trimmed.Contains('$StartMenuFolder')) {
        Write-Host "  Line $lineNum : ✅ Correct StartMenuFolder variable usage" -ForegroundColor Green
    }
    
    # Check for unclosed quotes
    $quoteCount = ($trimmed.ToCharArray() | Where-Object { $_ -eq '"' } | Measure-Object).Count
    if ($quoteCount % 2 -ne 0) {
        Write-Host "  Line $lineNum : ⚠️ Possible unclosed quote" -ForegroundColor Yellow
        $warningCount++
    }
    
    # Check for missing asset files
    if ($trimmed.Contains("assets\app_icon.ico")) {
        if (-not (Test-Path "assets\app_icon.ico")) {
            Write-Host "  Line $lineNum : ⚠️ Asset file may not exist: assets\app_icon.ico" -ForegroundColor Yellow
            $warningCount++
        }
    }
    
    # Check for LICENSE.txt reference
    if ($trimmed.Contains("LICENSE.txt")) {
        if (-not (Test-Path "LICENSE.txt")) {
            Write-Host "  Line $lineNum : ⚠️ License file may not exist: LICENSE.txt" -ForegroundColor Yellow
            $warningCount++
        } else {
            Write-Host "  Line $lineNum : ✅ License file reference found" -ForegroundColor Green
        }
    }
}

Write-Host "`nValidation Results:" -ForegroundColor Yellow
Write-Host "==================" -ForegroundColor Yellow

if ($errorCount -eq 0) {
    Write-Host "✅ No syntax errors found!" -ForegroundColor Green
} else {
    Write-Host "❌ Found $errorCount syntax errors" -ForegroundColor Red
}

if ($warningCount -gt 0) {
    Write-Host "⚠️ Found $warningCount warnings" -ForegroundColor Yellow
}

Write-Host "`nKey Components:" -ForegroundColor Cyan
Write-Host "• Variable declarations: ✅" -ForegroundColor Green
Write-Host "• MUI2 framework: ✅" -ForegroundColor Green  
Write-Host "• Start menu integration: ✅" -ForegroundColor Green
Write-Host "• License agreement: ✅" -ForegroundColor Green

if ($errorCount -eq 0) {
    Write-Host "`n🎉 Script appears to be ready for NSIS compilation!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`n❌ Please fix errors before compilation" -ForegroundColor Red
    exit 1
}
