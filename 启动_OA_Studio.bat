@echo off
chcp 65001 >nul
title Office Agent Studio v2.0

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║        🚀 Office Agent Studio v2.0 - 统一启动器             ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM 检查 Python 是否可用
py -3.12 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python 3.12
    echo.
    echo 请先安装 Python 3.12 或设置环境变量
    echo.
    pause
    exit /b 1
)

echo [提示] 正在启动 Office Agent Studio...
echo.
echo ══════════════════════════════════════════════════════════════
echo.

py -3.12 office_agent_studio.py

echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo 程序已退出
echo.
pause
