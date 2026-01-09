@echo off
chcp 65001 >nul
echo ========================================================================
echo 创建工作区管家桌面快捷方式
echo ========================================================================
echo.

set SCRIPT_DIR=%~dp0
set TARGET=%SCRIPT_DIR:~0,-1%\启动管家模式.bat
set TARGET=%TARGET:\\=\%

echo 正在创建桌面快捷方式...
echo.
echo 目标: %TARGET%
echo.

powershell -Command ^
"$WshShell = New-Object -ComObject WScript.Shell; ^
$Desktop = [Environment]::GetFolderPath('Desktop'); ^
$Shortcut = $WshShell.CreateShortcut($Desktop + '\Workspace Butler.lnk'); ^
$Shortcut.TargetPath = '%TARGET%'; ^
$Shortcut.WorkingDirectory = 'c:\Users\flyskyson\Office_Agent_Workspace'; ^
$Shortcut.Description = 'Workspace Butler - Daily Start'; ^
$Shortcut.Save(); ^
Write-Host '✅ 成功创建桌面快捷方式!' -ForegroundColor Green; ^
Write-Host '位置: $Desktop\Workspace Butler.lnk' -ForegroundColor Cyan"

echo.
echo ========================================================================
echo 完成！
echo ========================================================================
echo.
echo 现在可以在桌面上看到 'Workspace Butler.lnk' 图标
echo 双击即可启动工作区管家
echo.
pause
