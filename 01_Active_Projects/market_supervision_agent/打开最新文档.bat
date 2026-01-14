@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo 正在用WPS打开最新生成的申请书...

for /f "delims=" %%i in ('dir /b /o-d output\*.docx') do (
    start "" "output\%%i"
    goto :found
)

:found
echo 已打开文档
pause
