$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [Environment]::GetFolderPath('Desktop')

# Create shortcut for Butler Mode
$Shortcut1 = $WshShell.CreateShortcut($Desktop + '\Workspace Butler.lnk')
$Shortcut1.TargetPath = 'c:\Users\flyskyson\Office_Agent_Workspace\butler_mode.bat'
$Shortcut1.WorkingDirectory = 'c:\Users\flyskyson\Office_Agent_Workspace'
$Shortcut1.Description = 'Office Agent Workspace - Butler Mode'
$Shortcut1.Save()

# Create shortcut for File Manager Center
$Shortcut2 = $WshShell.CreateShortcut($Desktop + '\File Manager Center.lnk')
$Shortcut2.TargetPath = 'c:\Users\flyskyson\Office_Agent_Workspace\00_Agent_Library\99_Scripts_Tools\run_file_manager_center.bat'
$Shortcut2.WorkingDirectory = 'c:\Users\flyskyson\Office_Agent_Workspace'
$Shortcut2.Description = 'Office Agent Workspace - File Manager Center'
$Shortcut2.Save()

# Create shortcut for New Session
$Shortcut3 = $WshShell.CreateShortcut($Desktop + '\New Session Launcher.lnk')
$Shortcut3.TargetPath = 'c:\Users\flyskyson\Office_Agent_Workspace\start_new_session.bat'
$Shortcut3.WorkingDirectory = 'c:\Users\flyskyson\Office_Agent_Workspace'
$Shortcut3.Description = 'Office Agent Workspace - New Session Launcher'
$Shortcut3.Save()

Write-Host "Shortcuts created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Created shortcuts:" -ForegroundColor Cyan
Write-Host "  1. Workspace Butler.lnk"
Write-Host "  2. File Manager Center.lnk"
Write-Host "  3. New Session Launcher.lnk"
Write-Host ""
Write-Host "Check your desktop!" -ForegroundColor Yellow
