# 自动加载 DeepSeek API Key
# 此脚本在 VSCode 启动时自动运行

$apiKey = [System.Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY', [System.EnvironmentVariableTarget]::User)

if ($apiKey) {
    $env:DEEPSEEK_API_KEY = $apiKey
    Write-Host "✓ DeepSeek API Key loaded" -ForegroundColor Green
}
