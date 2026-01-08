# Screen Saver Settings Checker
# Check Windows screensaver configuration

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Windows Screen Saver Settings Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get registry settings
$scrnsaveKey = Get-ItemProperty -Path "HKCU:\Control Panel\Desktop" -ErrorAction SilentlyContinue

# 1. Check if screensaver is enabled
Write-Host "[1. Screensaver Status]" -ForegroundColor Yellow
Write-Host ""

if ($scrnsaveKey.SCRNSAVE.EXE) {
    Write-Host "Screensaver: Enabled" -ForegroundColor Green
    Write-Host "Current screensaver:"
    Write-Host $scrnsaveKey.SCRNSAVE.EXE -ForegroundColor White
}
else {
    Write-Host "Screensaver: Not enabled" -ForegroundColor Red
}

Write-Host ""

# 2. Check timeout setting
Write-Host "[2. Timeout Setting]" -ForegroundColor Yellow
Write-Host ""

if ($scrnsaveKey.ScreenSaveTimeOut) {
    $minutes = [int]$scrnsaveKey.ScreenSaveTimeOut / 60
    Write-Host "Timeout: $minutes minutes" -ForegroundColor Cyan
}
else {
    Write-Host "No timeout set" -ForegroundColor Yellow
}

Write-Host ""

# 3. Check secure setting
Write-Host "[3. Security Setting]" -ForegroundColor Yellow
Write-Host ""

if ($scrnsaveKey.ScreenSaverIsSecure) {
    $secureValue = $scrnsaveKey.ScreenSaverIsSecure
    if ($secureValue -eq "1") {
        Write-Host "Require password on wakeup: Yes" -ForegroundColor Green
    }
    else {
        Write-Host "Require password on wakeup: No" -ForegroundColor Yellow
    }
}
else {
    Write-Host "Security option not set" -ForegroundColor Yellow
}

Write-Host ""

# 4. Check policy restrictions
Write-Host "[4. Policy Check]" -ForegroundColor Yellow
Write-Host ""

try {
    $noScrnsaveKey = Get-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\Windows\Control Panel\Desktop" -ErrorAction SilentlyContinue
    if ($noScrnsaveKey.ScreenSaverIsPublic -eq 1 -or $noScrnsaveKey.NoScreenSaver) {
        Write-Host "Screensaver disabled by group policy" -ForegroundColor Red
    }
    else {
        Write-Host "Screensaver not restricted by policy" -ForegroundColor Green
    }
}
catch {
    Write-Host "Screensaver not restricted by policy" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Check completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tips:" -ForegroundColor Gray
Write-Host "  - To change screensaver: control desk.cpl,screensaver,@screensaver" -ForegroundColor Gray
Write-Host "  - Or go to Settings -> Personalization -> Lock screen -> Screen saver" -ForegroundColor Gray
Write-Host ""
