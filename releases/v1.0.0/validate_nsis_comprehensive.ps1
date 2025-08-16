# Comprehensive NSIS Syntax Checker
# Validates NSIS script structure and common syntax patterns

param(
    [string]$ScriptPath = "PsychologicalRecords_Setup.nsi"
)

Write-Host "🔍 Comprehensive NSIS Syntax Validation" -ForegroundColor Yellow
Write-Host "=======================================" -ForegroundColor Yellow

if (-not (Test-Path $ScriptPath)) {
    Write-Host "❌ Script file not found: $ScriptPath" -ForegroundColor Red
    exit 1
}

$content = Get-Content $ScriptPath
$lineNum = 0
$errorCount = 0
$warningCount = 0
$infoCount = 0

Write-Host "`nAnalyzing $ScriptPath..." -ForegroundColor Cyan

# Track required elements
$hasRequiredIncludes = @{
    "MUI2" = $false
    "FileFunc" = $false
    "LogicLib" = $false
}

$hasRequiredDefines = @{
    "PRODUCT_NAME" = $false
    "PRODUCT_VERSION" = $false
    "MUI_STARTMENUPAGE_DEFAULTFOLDER" = $false
    "MUI_STARTMENUPAGE_REGISTRY_ROOT" = $false
}

$hasRequiredElements = @{
    "StartMenuFolder_Variable" = $false
    "MUI_PAGE_STARTMENU" = $false
    "License_File" = $false
}

foreach ($line in $content) {
    $lineNum++
    $trimmed = $line.Trim()
    
    # Skip comments and empty lines for most checks
    if ($trimmed.StartsWith(";") -or $trimmed -eq "") {
        continue
    }
    
    # Check for required includes
    if ($trimmed -match '!include\s+"([^"]+)"') {
        $include = $matches[1]
        if ($include -eq "MUI2.nsh") {
            $hasRequiredIncludes["MUI2"] = $true
            Write-Host "  Line $lineNum : ✅ MUI2 framework included" -ForegroundColor Green
            $infoCount++
        }
        elseif ($include -eq "FileFunc.nsh") {
            $hasRequiredIncludes["FileFunc"] = $true
            Write-Host "  Line $lineNum : ✅ FileFunc included" -ForegroundColor Green
            $infoCount++
        }
        elseif ($include -eq "LogicLib.nsh") {
            $hasRequiredIncludes["LogicLib"] = $true
            Write-Host "  Line $lineNum : ✅ LogicLib included" -ForegroundColor Green
            $infoCount++
        }
    }
    
    # Check for required defines
    if ($trimmed -match '!define\s+([^\s]+)') {
        $define = $matches[1]
        if ($define -eq "PRODUCT_NAME") {
            $hasRequiredDefines["PRODUCT_NAME"] = $true
            Write-Host "  Line $lineNum : ✅ PRODUCT_NAME defined" -ForegroundColor Green
            $infoCount++
        }
        elseif ($define -eq "PRODUCT_VERSION") {
            $hasRequiredDefines["PRODUCT_VERSION"] = $true
            Write-Host "  Line $lineNum : ✅ PRODUCT_VERSION defined" -ForegroundColor Green
            $infoCount++
        }
        elseif ($define -eq "MUI_STARTMENUPAGE_DEFAULTFOLDER") {
            $hasRequiredDefines["MUI_STARTMENUPAGE_DEFAULTFOLDER"] = $true
            Write-Host "  Line $lineNum : ✅ Start Menu default folder configured" -ForegroundColor Green
            $infoCount++
        }
        elseif ($define -eq "MUI_STARTMENUPAGE_REGISTRY_ROOT") {
            $hasRequiredDefines["MUI_STARTMENUPAGE_REGISTRY_ROOT"] = $true
            Write-Host "  Line $lineNum : ✅ Start Menu registry root configured" -ForegroundColor Green
            $infoCount++
        }
    }
    
    # Check variable declaration
    if ($trimmed -match "Var\s+StartMenuFolder") {
        $hasRequiredElements["StartMenuFolder_Variable"] = $true
        Write-Host "  Line $lineNum : ✅ StartMenuFolder variable declared" -ForegroundColor Green
        $infoCount++
    }
    
    # Check MUI_PAGE_STARTMENU syntax
    if ($trimmed -match '!insertmacro\s+MUI_PAGE_STARTMENU') {
        $hasRequiredElements["MUI_PAGE_STARTMENU"] = $true
        if ($trimmed -match '!insertmacro\s+MUI_PAGE_STARTMENU\s+"[^"]+"\s+\$StartMenuFolder') {
            Write-Host "  Line $lineNum : ✅ MUI_PAGE_STARTMENU syntax correct" -ForegroundColor Green
            $infoCount++
        } else {
            Write-Host "  Line $lineNum : ❌ MUI_PAGE_STARTMENU syntax incorrect" -ForegroundColor Red
            Write-Host "    Expected: !insertmacro MUI_PAGE_STARTMENU `"Application`" `$StartMenuFolder" -ForegroundColor Yellow
            $errorCount++
        }
    }
    
    # Check for license file reference
    if ($trimmed.Contains("LICENSE.txt")) {
        $hasRequiredElements["License_File"] = $true
        Write-Host "  Line $lineNum : ✅ License file referenced" -ForegroundColor Green
        $infoCount++
    }
    
    # Check for deprecated patterns
    if ($trimmed.Contains('$STARTMENU_FOLDER')) {
        Write-Host "  Line $lineNum : ❌ Found deprecated STARTMENU_FOLDER variable" -ForegroundColor Red
        $errorCount++
    }
    
    # Check for unclosed quotes
    $quoteCount = ($trimmed.ToCharArray() | Where-Object { $_ -eq '"' } | Measure-Object).Count
    if ($quoteCount % 2 -ne 0) {
        Write-Host "  Line $lineNum : ⚠️ Possible unclosed quote" -ForegroundColor Yellow
        $warningCount++
    }
    
    # Check for missing asset files (warnings only)
    if ($trimmed.Contains("assets\app_icon.ico")) {
        if (-not (Test-Path "..\..\assets\app_icon.ico")) {
            Write-Host "  Line $lineNum : ⚠️ Asset file may not exist: assets\app_icon.ico" -ForegroundColor Yellow
            $warningCount++
        }
    }
}

Write-Host "`n" + "="*50 -ForegroundColor Yellow
Write-Host "VALIDATION SUMMARY" -ForegroundColor Yellow
Write-Host "="*50 -ForegroundColor Yellow

# Check required elements
Write-Host "`n📋 Required Elements Check:" -ForegroundColor Cyan

$allRequiredMet = $true

foreach ($include in $hasRequiredIncludes.Keys) {
    if ($hasRequiredIncludes[$include]) {
        Write-Host "  ✅ $include include: Present" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $include include: Missing" -ForegroundColor Red
        $allRequiredMet = $false
        $errorCount++
    }
}

foreach ($define in $hasRequiredDefines.Keys) {
    if ($hasRequiredDefines[$define]) {
        Write-Host "  ✅ $define define: Present" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $define define: Missing" -ForegroundColor Red
        $allRequiredMet = $false
        $errorCount++
    }
}

foreach ($element in $hasRequiredElements.Keys) {
    if ($hasRequiredElements[$element]) {
        Write-Host "  ✅ $element : Present" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $element : Missing" -ForegroundColor Red
        $allRequiredMet = $false
        $errorCount++
    }
}

Write-Host "`n📊 Results:" -ForegroundColor Cyan
if ($errorCount -eq 0) {
    Write-Host "  ✅ Syntax Errors: None" -ForegroundColor Green
} else {
    Write-Host "  ❌ Syntax Errors: $errorCount" -ForegroundColor Red
}

if ($warningCount -eq 0) {
    Write-Host "  ✅ Warnings: None" -ForegroundColor Green
} else {
    Write-Host "  ⚠️ Warnings: $warningCount" -ForegroundColor Yellow
}

Write-Host "  ℹ️ Info Messages: $infoCount" -ForegroundColor Cyan

Write-Host "`n🎯 Overall Status:" -ForegroundColor Yellow
if ($errorCount -eq 0 -and $allRequiredMet) {
    Write-Host "  🎉 READY FOR NSIS COMPILATION!" -ForegroundColor Green
    Write-Host "  The script should compile successfully when NSIS is available." -ForegroundColor Green
    exit 0
} else {
    Write-Host "  ❌ SCRIPT NEEDS FIXES BEFORE COMPILATION" -ForegroundColor Red
    Write-Host "  Please address the errors listed above." -ForegroundColor Red
    exit 1
}
