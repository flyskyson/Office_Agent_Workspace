@echo off
REM Setup Workspace Scheduled Maintenance - Administrator Launcher
REM This script will restart itself with administrator privileges

setlocal

set LOG_FILE=%TEMP%\workspace_maintenance_setup.log

echo.
echo ============================================================
echo Workspace Scheduled Maintenance Setup
echo ============================================================
echo.
echo Log file: %LOG_FILE%
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Running with administrator privileges...
    echo [INFO] Running with administrator privileges... > "%LOG_FILE%"
    echo.
) else (
    echo [INFO] Requesting administrator privileges...
    echo [INFO] Requesting administrator privileges... > "%LOG_FILE%"

    PowerShell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File ""%~dpn0.ps1""' -Verb RunAs"

    exit /b
)

REM Run the PowerShell script
echo [INFO] Executing PowerShell script...
echo [INFO] Executing PowerShell script... >> "%LOG_FILE%"

PowerShell -NoProfile -ExecutionPolicy Bypass -File "%~dpn0.ps1" >> "%LOG_FILE%" 2>&1

set SCRIPT_ERROR=%errorLevel%

echo.
if %SCRIPT_ERROR% == 0 (
    echo [SUCCESS] Setup completed successfully!
    echo [SUCCESS] Setup completed successfully! >> "%LOG_FILE%"
    echo.
    echo ============================================================
    echo Verifying task creation...
    echo ============================================================
    echo.

    PowerShell -NoProfile -ExecutionPolicy Bypass -Command "Get-ScheduledTask -TaskName 'Office_Workspace_Weekly_Maintenance' -ErrorAction SilentlyContinue | Select-Object TaskName, State"
) else (
    echo [ERROR] Setup failed with error code: %SCRIPT_ERROR%
    echo [ERROR] Setup failed with error code: %SCRIPT_ERROR% >> "%LOG_FILE%"
    echo.
    echo Please check the log file for details:
    echo %LOG_FILE%
    echo.
    echo Common issues:
    echo 1. User clicked "No" on UAC prompt
    echo 2. Python not found in PATH
    echo 3. workspace_maintenance.py not found
)

echo.
echo ============================================================
echo Log saved to: %LOG_FILE%
echo ============================================================
echo.
pause
