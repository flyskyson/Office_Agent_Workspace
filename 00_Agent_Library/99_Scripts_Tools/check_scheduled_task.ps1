# Check if Workspace Maintenance Scheduled Task exists

$TaskName = "Office_Workspace_Weekly_Maintenance"

Write-Host "Checking for scheduled task: $TaskName" -ForegroundColor Cyan
Write-Host ""

try {
    $Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction Stop

    Write-Host "Task found!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  Name: $($Task.TaskName)"
    Write-Host "  State: $($Task.State)"
    Write-Host "  Description: $($Task.Description)"

    Write-Host ""
    Write-Host "Triggers:" -ForegroundColor Cyan
    $Task.Triggers | ForEach-Object {
        Write-Host "  - $($_.ToString())"
    }

    Write-Host ""
    Write-Host "Action:" -ForegroundColor Cyan
    Write-Host "  Execute: $($Task.Action.Execute)"
    Write-Host "  Arguments: $($Task.Action.Arguments)"
    Write-Host "  Working Directory: $($Task.Action.WorkingDirectory)"

    Write-Host ""
    Write-Host "Last Run Time:" -ForegroundColor Cyan
    $Info = Get-ScheduledTaskInfo -TaskName $TaskName
    if ($Info.LastRunTime -eq $null) {
        Write-Host "  Never run"
    } else {
        Write-Host "  $($Info.LastRunTime)"
    }
    Write-Host "  Next Run Time: $($Info.NextRunTime)"

    Write-Host ""
    Write-Host "Task is properly configured!" -ForegroundColor Green

}
catch {
    Write-Host "Task NOT found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "The scheduled task '$TaskName' does not exist." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To create it, run:" -ForegroundColor Cyan
    Write-Host "  1. Right-click 'setup_scheduled_maintenance.bat'"
    Write-Host "  2. Select 'Run as administrator'"
    Write-Host "  3. Confirm UAC prompt"
}

Write-Host ""
