# Claude Code 模型切换脚本
# 使用方法: .\switch-model.ps1 sonnet|haiku|opus|deepseek|deepseek-reasoner

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("sonnet", "haiku", "opus", "deepseek", "deepseek-reasoner")]
    [string]$Model
)

$ConfigDir = ".claude"
$SettingsFile = "$ConfigDir\settings.local.json"
$ConfigFile = "$ConfigDir\config-$Model.json"

# 检查配置文件是否存在
if (-not (Test-Path $ConfigFile)) {
    Write-Error "配置文件不存在: $ConfigFile"
    exit 1
}

# 备份当前配置
if (Test-Path $SettingsFile) {
    $Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $BackupFile = "$ConfigDir\settings.backup.$Timestamp.json"
    Copy-Item $SettingsFile $BackupFile
    Write-Host "已备份当前配置到: $BackupFile" -ForegroundColor Cyan
}

# 复制选定的配置
Copy-Item $ConfigFile $SettingsFile -Force

# 显示当前配置
$ModelName = switch ($Model) {
    "sonnet"           { "Sonnet 4.5 (平衡)" }
    "haiku"            { "Haiku 4.5 (快速)" }
    "opus"             { "Opus 4.5 (最强)" }
    "deepseek"         { "DeepSeek Chat (高性价比)" }
    "deepseek-reasoner" { "DeepSeek Reasoner (强化推理)" }
}

Write-Host "`n✓ 已切换到模型: $ModelName" -ForegroundColor Green
Write-Host "配置文件: $SettingsFile" -ForegroundColor Gray

# DeepSeek 特殊提示
if ($Model -like "deepseek*") {
    Write-Host "`n提示: 确保 DEEPSEEK_API_KEY 环境变量已设置" -ForegroundColor Yellow
    Write-Host "      设置命令: `$env:DEEPSEEK_API_KEY='your-api-key'" -ForegroundColor Cyan
} else {
    Write-Host "`n提示: 重启 VSCode 或重新加载 Claude Code 窗口以应用更改" -ForegroundColor Yellow
}
