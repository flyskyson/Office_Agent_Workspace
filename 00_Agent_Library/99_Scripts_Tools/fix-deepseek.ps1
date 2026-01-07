# DeepSeek Configuration Fix Script

Write-Host ""
Write-Host "=== DeepSeek Configuration Fix ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Verify API Key is permanently set
Write-Host "Step 1: Verifying permanent API Key..." -ForegroundColor Yellow
$permanentKey = [System.Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY', [System.EnvironmentVariableTarget]::User)
if ($permanentKey) {
    Write-Host "   [OK] Permanent API Key found" -ForegroundColor Green
} else {
    Write-Host "   [ERROR] No permanent API Key found" -ForegroundColor Red
    Write-Host "   Please run: [System.Environment]::SetEnvironmentVariable('DEEPSEEK_API_KEY', 'your-key', [System.EnvironmentVariableTarget]::User)" -ForegroundColor Gray
    exit 1
}

# Step 2: Load API Key into current session
Write-Host ""
Write-Host "Step 2: Loading API Key into current session..." -ForegroundColor Yellow
$env:DEEPSEEK_API_KEY = $permanentKey
Write-Host "   [OK] API Key loaded: $($env:DEEPSEEK_API_KEY.Substring(0, 12))..." -ForegroundColor Green

# Step 3: Verify configuration file
Write-Host ""
Write-Host "Step 3: Verifying configuration file..." -ForegroundColor Yellow
if (Test-Path ".claude\settings.local.json") {
    $config = Get-Content ".claude\settings.local.json" | ConvertFrom-Json
    Write-Host "   Current model: $($config.model)" -ForegroundColor Gray

    if ($config.model -eq "deepseek-chat") {
        Write-Host "   [OK] Already set to deepseek-chat" -ForegroundColor Green
    } else {
        Write-Host "   [INFO] Switching to deepseek-chat..." -ForegroundColor Yellow
        Copy-Item ".claude\config-deepseek.json" ".claude\settings.local.json" -Force
        Write-Host "   [OK] Switched to deepseek-chat" -ForegroundColor Green
    }
} else {
    Write-Host "   [ERROR] Configuration file not found" -ForegroundColor Red
    exit 1
}

# Step 4: Test API connection
Write-Host ""
Write-Host "Step 4: Testing DeepSeek API..." -ForegroundColor Yellow
Write-Host "   Attempting to connect to DeepSeek API..." -ForegroundColor Gray

try {
    $headers = @{
        "Authorization" = "Bearer $env:DEEPSEEK_API_KEY"
        "Content-Type" = "application/json"
    }

    $body = @{
        model = "deepseek-chat"
        messages = @(
            @{
                role = "user"
                content = "Say 'API test successful' in JSON"
            }
        )
        max_tokens = 50
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "https://api.deepseek.com/v1/chat/completions" -Method Post -Headers $headers -Body $body -TimeoutSec 10

    if ($response.choices[0].message.content) {
        Write-Host "   [OK] DeepSeek API is working!" -ForegroundColor Green
        Write-Host "   Response: $($response.choices[0].message.content)" -ForegroundColor Gray
    }
} catch {
    Write-Host "   [ERROR] API connection failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Please check your API Key and network connection" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "=== Configuration Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Current Status:" -ForegroundColor Yellow
Write-Host "  - Model: deepseek-chat" -ForegroundColor Green
Write-Host "  - API Key: Loaded in current session" -ForegroundColor Green
Write-Host "  - API URL: https://api.deepseek.com/v1" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Reload this VSCode window (Ctrl+Shift+P > 'Developer: Reload Window')" -ForegroundColor White
Write-Host "  2. Test by asking: '你好,请用一句话介绍你自己'" -ForegroundColor White
Write-Host "  3. You should receive a DeepSeek response" -ForegroundColor White
Write-Host ""
