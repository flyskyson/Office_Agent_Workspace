# Simple Task Creation - Copy and Run in PowerShell as Administrator
# 简单任务创建 - 在管理员 PowerShell 中复制粘贴运行

Write-Host "Creating Workspace Maintenance Scheduled Task..." -ForegroundColor Cyan
Write-Host ""

# Get current workspace path
$WorkspacePath = "C:\Users\flyskyson\Office_Agent_Workspace"
$PythonExe = "python"
$ScriptPath = Join-Path $WorkspacePath "workspace_maintenance.py"

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Workspace: $WorkspacePath"
Write-Host "  Script: $ScriptPath"
Write-Host "  Schedule: Every Sunday at 2:00 AM"
Write-Host ""

# Check if script exists
if (-not (Test-Path $ScriptPath)) {
    Write-Host "ERROR: Script not found at $ScriptPath" -ForegroundColor Red
    exit 1
}

try {
    # Remove old task if exists
    $existingTask = Get-ScheduledTask -TaskName "Office_Workspace_Weekly_Maintenance" -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "Removing old task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName "Office_Workspace_Weekly_Maintenance" -Confirm:$false
    }

    # Create action
    $action = New-ScheduledTaskAction `
        -Execute $PythonExe `
        -Argument "`"$ScriptPath`" --health-report" `
        -WorkingDirectory $WorkspacePath

    # Create trigger
    $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 2am

    # Create settings
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RunOnlyIfNetworkAvailable

    # Register task
    Register-ScheduledTask `
        -TaskName "Office_Workspace_Weekly_Maintenance" `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description "Office Agent Workspace Automatic Maintenance" `
        -User "SYSTEM" | Out-Null

    Write-Host "SUCCESS! Task created." -ForegroundColor Green
    Write-Host ""
    Write-Host "To verify, run:" -ForegroundColor Cyan
    Write-Host "  Get-ScheduledTask -TaskName 'Office_Workspace_Weekly_Maintenance'"
    Write-Host ""
    Write-Host "To test immediately, run:" -ForegroundColor Cyan
    Write-Host "  Start-ScheduledTask -TaskName 'Office_Workspace_Weekly_Maintenance'"
}
catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
    exit 1
}
