@echo off
chcp 65001 >nul
echo ====================================
echo 学习记忆助手 - Web UI 启动器
echo ====================================
echo.

cd /d "%~dp0"

REM 检查 Python 是否可用
py -3.12 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python 3.12
    echo.
    pause
    exit /b 1
)

echo [提示] 检查依赖...
py -3.12 -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 正在安装 Flask...
    py -3.12 -m pip install flask
    echo.
)

echo [提示] 启动 Web 服务器...
echo [提示] 浏览器访问: http://127.0.0.1:5555
echo.
echo 按 Ctrl+C 停止服务器
echo ====================================
echo.

py -3.12 ui\app.py

pause
