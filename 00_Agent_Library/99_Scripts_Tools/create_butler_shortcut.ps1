$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [Environment]::GetFolderPath('Desktop')

# Create shortcut for Butler Mode
$Shortcut = $WshShell.CreateShortcut($Desktop + '\Workspace Butler.lnk')
$Shortcut.TargetPath = 'c:\Users\flyskyson\Office_Agent_Workspace\00_Agent_Library\99_Scripts_Tools\启动管家模式.bat'
$Shortcut.WorkingDirectory = 'c:\Users\flyskyson\Office_Agent_Workspace'
$Shortcut.Description = 'Workspace Butler - Daily Start'
$Shortcut.Save()

Write-Host "✅ Created: Workspace Butler.lnk" -ForegroundColor Green
Write-Host "Location: $Desktop" -ForegroundColor Cyan
