# AI 新闻追踪器 - PowerShell 任务计划配置

$WorkspaceDir = "C:\Users\flyskyson\Office_Agent_Workspace"
$PythonScript = "$WorkspaceDir\01_Active_Projects\ai_news_tracker\src\news_tracker.py"

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "   AI 新闻追踪器 - 自动任务配置" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# 检查脚本是否存在
if (-not (Test-Path $PythonScript)) {
    Write-Host "[错误] 未找到新闻追踪器脚本！" -ForegroundColor Red
    Write-Host "路径: $PythonScript"
    exit 1
}

# 删除现有任务
Write-Host "[1/4] 删除现有任务计划..." -ForegroundColor Yellow
Unregister-ScheduledTask -TaskName "AI_News_Daily" -ErrorAction SilentlyContinue
Unregister-ScheduledTask -TaskName "AI_News_Weekly" -ErrorAction SilentlyContinue
Write-Host "  ✓ 已清理旧任务`n" -ForegroundColor Green

# 创建任务操作
$Action = New-ScheduledTaskAction -Execute "python" -Argument $PythonScript

# 创建触发器 - 每天 09:00
Write-Host "[2/4] 创建每日新闻任务..." -ForegroundColor Yellow
$DailyTrigger = New-ScheduledTaskTrigger -Daily -At "09:00"
Register-ScheduledTask -TaskName "AI_News_Daily" -Action $Action -Trigger $DailyTrigger -Description "AI 新闻追踪器 - 每日运行" | Out-Null
Write-Host "  ✓ 每日任务创建成功（每天 09:00）`n" -ForegroundColor Green

# 创建触发器 - 每周一 09:00
Write-Host "[3/4] 创建周报任务..." -ForegroundColor Yellow
$WeeklyTrigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "09:00"
Register-ScheduledTask -TaskName "AI_News_Weekly" -Action $Action -Trigger $WeeklyTrigger -Description "AI 新闻追踪器 - 周报" | Out-Null
Write-Host "  ✓ 周报任务创建成功（每周一 09:00）`n" -ForegroundColor Green

# 显示已创建的任务
Write-Host "[4/4] 验证任务配置...`n" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   已创建的自动任务" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

Get-ScheduledTask -TaskName "AI_News_Daily" | Format-List TaskName, State, Description
Get-ScheduledTask -TaskName "AI_News_Weekly" | Format-List TaskName, State, Description

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "   配置完成！" -ForegroundColor Green
Write-Host "============================================`n" -ForegroundColor Cyan

Write-Host "📅 自动任务：" -ForegroundColor Cyan
Write-Host "   - 每日新闻: 每天 09:00" -ForegroundColor White
Write-Host "   - 每周报告: 每周一 09:00`n" -ForegroundColor White

Write-Host "📁 新闻报告保存位置：" -ForegroundColor Cyan
Write-Host "   $WorkspaceDir\01_Active_Projects\ai_news_tracker\data\daily_news_YYYYMMDD.md`n" -ForegroundColor White

Write-Host "💡 手动运行：" -ForegroundColor Cyan
Write-Host "   - 双击: 运行AI新闻追踪.bat" -ForegroundColor White
Write-Host "   - 或运行: python $PythonScript`n" -ForegroundColor White

Write-Host "🗑️  取消自动任务：" -ForegroundColor Cyan
Write-Host "   Unregister-ScheduledTask -TaskName 'AI_News_Daily'`n" -ForegroundColor White

Write-Host "============================================`n" -ForegroundColor Cyan
