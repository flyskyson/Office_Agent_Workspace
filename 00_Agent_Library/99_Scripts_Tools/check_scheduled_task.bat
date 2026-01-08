@echo off
REM Check Workspace Scheduled Task Status

echo.
echo ============================================================
echo Checking Scheduled Task Status
echo ============================================================
echo.

PowerShell -NoProfile -ExecutionPolicy Bypass -File "%~dpn0.ps1"

echo.
pause
