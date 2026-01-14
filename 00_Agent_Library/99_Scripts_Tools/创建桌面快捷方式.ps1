# 创建工作区工具桌面快捷方式
# PowerShell脚本

$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [Environment]::GetFolderPath("Desktop")
$Workspace = "C:\Users\flyskyson\Office_Agent_Workspace"

# 创建快捷方式函数
function Create-Shortcut($Name, $TargetPath, $Description) {
    $Shortcut = $WshShell.CreateShortcut("$Desktop\$Name.lnk")
    $Shortcut.TargetPath = $TargetPath
    $Shortcut.WorkingDirectory = $Workspace
    $Shortcut.Description = $Description
    $Shortcut.Save()
    Write-Host "✓ 创建快捷方式: $Name" -ForegroundColor Green
}

Write-Host "`n====================================" -ForegroundColor Cyan
Write-Host "  创建工作区工具桌面快捷方式" -ForegroundColor Cyan
Write-Host "====================================`n" -ForegroundColor Cyan

# 1. 今日启动器快捷方式
$LauncherBat = @"
@echo off
chcp 65001 > nul
cd /d $Workspace
python daily_launcher.py
pause
"@

$LauncherBatPath = "$Workspace\启动今日启动器.bat"
$LauncherBat | Out-File -FilePath $LauncherBatPath -Encoding ASCII
Create-Shortcut "今日启动器" $LauncherBatPath "每天开始工作的第一站"

# 2. 文件管理中心快捷方式
$FileManagerBat = @"
@echo off
chcp 65001 > nul
cd /d $Workspace
python file_manager_center.py
pause
"@

$FileManagerBatPath = "$Workspace\启动文件管理中心.bat"
$FileManagerBat | Out-File -FilePath $FileManagerBatPath -Encoding ASCII
Create-Shortcut "文件管理中心" $FileManagerBatPath "统一管理所有文件"

# 3. 市场监管智能体快捷方式
$MarketAgentBat = @"
@echo off
chcp 65001 > nul
cd /d $Workspace\01_Active_Projects\market_supervision_agent
python 新版申请书填充工具.py
pause
"@

$MarketAgentBatPath = "$Workspace\启动市场监管智能体.bat"
$MarketAgentBat | Out-File -FilePath $MarketAgentBatPath -Encoding ASCII
Create-Shortcut "市场监管智能体" $MarketAgentBatPath "个体工商户证照办理自动化"

# 4. 工作区文件夹快捷方式
Create-Shortcut "工作区文件夹" $Workspace "访问工作区所有文件"

# 5. 快速指南快捷方式
Create-Shortcut "工具使用指南" "$Workspace\三大工具快速指南.md" "工作区工具使用说明"

Write-Host "`n====================================" -ForegroundColor Cyan
Write-Host "  ✓ 快捷方式创建完成！" -ForegroundColor Green
Write-Host "====================================`n" -ForegroundColor Cyan

Write-Host "已创建的桌面快捷方式：" -ForegroundColor Yellow
Write-Host "  1. 今日启动器.lnk" -ForegroundColor White
Write-Host "  2. 文件管理中心.lnk" -ForegroundColor White
Write-Host "  3. 市场监管智能体.lnk" -ForegroundColor White
Write-Host "  4. 工作区文件夹.lnk" -ForegroundColor White
Write-Host "  5. 工具使用指南.lnk" -ForegroundColor White

Write-Host "`n提示: 快捷方式已创建到桌面" -ForegroundColor Cyan
Write-Host "      可以直接双击使用！`n" -ForegroundColor Cyan

# 暂停
Read-Host "按回车键退出"