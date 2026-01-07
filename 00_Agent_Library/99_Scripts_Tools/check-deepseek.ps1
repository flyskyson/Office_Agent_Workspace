# DeepSeek Configuration Check

Write-Host ""
Write-Host "=== DeepSeek Configuration Verification ===" -ForegroundColor Cyan
Write-Host ""

# Check environment variable
Write-Host "1. Checking Environment Variable" -ForegroundColor Yellow
$envKey = [System.Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY', [System.EnvironmentVariableTarget]::User)
if ($envKey) {
    Write-Host "   [OK] DEEPSEEK_API_KEY is set" -ForegroundColor Green
    Write-Host "   Key: $($envKey.Substring(0, 12))..." -ForegroundColor Gray
} else {
    Write-Host "   [ERROR] DEEPSEEK_API_KEY not set" -ForegroundColor Red
}

# Check current session
Write-Host ""
Write-Host "2. Checking Current Session" -ForegroundColor Yellow
if ($env:DEEPSEEK_API_KEY) {
    Write-Host "   [OK] API Key loaded in current session" -ForegroundColor Green
} else {
    Write-Host "   [WARN] API Key not loaded (restart VSCode required)" -ForegroundColor Yellow
}

# Check config file
Write-Host ""
Write-Host "3. Checking Configuration File" -ForegroundColor Yellow
if (Test-Path ".claude\settings.local.json") {
    Write-Host "   [OK] Configuration file exists" -ForegroundColor Green
    $config = Get-Content ".claude\settings.local.json" | ConvertFrom-Json
    Write-Host "   Model: $($config.model)" -ForegroundColor Gray
    Write-Host "   API: $($config.api.base_url)" -ForegroundColor Gray
} else {
    Write-Host "   [ERROR] Configuration file not found" -ForegroundColor Red
}

# Summary
Write-Host ""
Write-Host "=== Verification Summary ===" -ForegroundColor Cyan
Write-Host ""

if ($envKey -and (Test-Path ".claude\settings.local.json")) {
    Write-Host "[SUCCESS] DeepSeek configuration complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "  1. Restart VSCode" -ForegroundColor White
    Write-Host "  2. Or test with a question in Claude Code" -ForegroundColor White
    Write-Host ""
    Write-Host "Test Questions:" -ForegroundColor Gray
    Write-Host "  - Hello, please introduce yourself" -ForegroundColor Gray
    Write-Host "  - Write a Python Hello World" -ForegroundColor Gray
} else {
    Write-Host "[ERROR] Configuration incomplete, please check above" -ForegroundColor Red
}

Write-Host ""
