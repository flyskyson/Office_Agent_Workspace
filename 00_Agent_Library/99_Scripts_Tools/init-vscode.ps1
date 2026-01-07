# VSCode 启动时自动加载环境变量
# 将此路径添加到 VSCode 的 terminal.integrated.profiles.windows 设置中

# 加载 DeepSeek API Key
$apiKey = [System.Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY', [System.EnvironmentVariableTarget]::User)
if ($apiKey) {
    $env:DEEPSEEK_API_KEY = $apiKey
}
