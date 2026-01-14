$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [Environment]::GetFolderPath('Desktop')

# Create shortcut for fixing launcher
$Shortcut = $WshShell.CreateShortcut($Desktop + '\🔧 修复工作区启动器.lnk')
$Shortcut.TargetPath = 'c:\Users\flyskyson\Office_Agent_Workspace\重新创建快捷方式.bat'
$Shortcut.WorkingDirectory = 'c:\Users\flyskyson\Office_Agent_Workspace'
$Shortcut.Description = '修复工作区启动器问题'
$Shortcut.Save()

Write-Host "✅ 已在桌面创建: 🔧 修复工作区启动器.lnk" -ForegroundColor Green
