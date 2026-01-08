# Setup Workspace Scheduled Maintenance
# This script creates a Windows scheduled task for automatic workspace maintenance
# REQUIRES ADMINISTRATOR PRIVILEGES

# Check for administrator privileges
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "This script requires administrator privileges." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please right-click and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host "Or run PowerShell as Administrator and execute this script." -ForegroundColor Yellow
    Write-Host ""
    $retry = Read-Host "Attempt to restart as Administrator? (Y/N)"
    if ($retry -eq 'Y' -or $retry -eq 'y') {
        Start-Process PowerShell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
        exit
    }
    exit 1
}

$ErrorActionPreference = "Stop"

# Get workspace root directory
$WorkspacePath = $PSScriptRoot
$MaintenanceScript = Join-Path $WorkspacePath "workspace_maintenance.py"

# Check if maintenance script exists
if (-not (Test-Path $MaintenanceScript)) {
    Write-Host "Error: Cannot find workspace_maintenance.py" -ForegroundColor Red
    Write-Host "Please ensure this script is in the workspace root directory" -ForegroundColor Red
    exit 1
}

# Task name
$TaskName = "Office_Workspace_Weekly_Maintenance"

# Get Python path
try {
    $PythonPath = (Get-Command python).Source
    Write-Host "Found Python: $PythonPath" -ForegroundColor Green
}
catch {
    Write-Host "Error: Cannot find Python" -ForegroundColor Red
    Write-Host "Please ensure Python is installed and added to PATH" -ForegroundColor Red
    exit 1
}

# Remove old task if exists
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($ExistingTask) {
    Write-Host "Removing old scheduled task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create task action
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "`"$MaintenanceScript`" --health-report" -WorkingDirectory $WorkspacePath

# Create trigger - Weekly on Sunday at 2 AM
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 2am

# Task settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable -DontStopOnIdleEnd

# Register task
try {
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "Office Agent Workspace Automatic Maintenance - Runs weekly cleanup and health check" -User "SYSTEM" | Out-Null

    Write-Host ""
    Write-Host "Successfully created scheduled task!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  Task Name: $TaskName"
    Write-Host "  Frequency: Weekly every Sunday at 2:00 AM"
    Write-Host "  Workspace: $WorkspacePath"
    Write-Host "  Python: $PythonPath"
    Write-Host ""
    Write-Host "Command:" -ForegroundColor Cyan
    Write-Host "  $PythonPath `"$MaintenanceScript`" --health-report"
    Write-Host ""
    Write-Host "Tips:" -ForegroundColor Yellow
    Write-Host "  - Task runs with SYSTEM privileges"
    Write-Host "  - Maintenance reports will be saved in workspace root"
    Write-Host "  - To run manually: python workspace_maintenance.py"
    Write-Host "  - Or double-click: run_maintenance.bat"
    Write-Host ""
    Write-Host "Manage Task:" -ForegroundColor Cyan
    Write-Host "  - Open Task Scheduler: taskschd.msc"
    Write-Host "  - Run now: Start-ScheduledTask -TaskName `"$TaskName`""
    Write-Host "  - Disable: Disable-ScheduledTask -TaskName `"$TaskName`""
    Write-Host "  - Enable: Enable-ScheduledTask -TaskName `"$TaskName`""
    Write-Host "  - Delete: Unregister-ScheduledTask -TaskName `"$TaskName`" -Confirm:`$false"
}
catch {
    Write-Host ""
    Write-Host "Failed to create task: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host ("="*60) -ForegroundColor DarkGray
Write-Host "Setup Complete! Workspace will be automatically maintained" -ForegroundColor Green
Write-Host ("="*60) -ForegroundColor DarkGray
Write-Host ""
