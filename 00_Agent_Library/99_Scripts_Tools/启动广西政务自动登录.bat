@echo off
chcp 65001 >nul
echo ====================================
echo 广西政务服务平台 - 自动登录
echo ====================================
echo.
echo 正在启动自动化脚本...
echo.

cd /d "%~dp0"

REM 检查 Python 是否可用
py -3.12 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python 3.12，请先安装 Python
    echo.
    pause
    exit /b 1
)

REM 检查 playwright 是否安装
py -3.12 -c "import playwright" >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 未安装 playwright，正在安装...
    echo.
    py -3.12 -m pip install playwright
    echo.
    echo [提示] 正在安装浏览器...
    py -3.12 -m playwright install chromium
    echo.
)

REM 运行脚本
py -3.12 广西政务自动登录.py

echo.
echo ====================================
echo 程序已结束
echo ====================================
pause
