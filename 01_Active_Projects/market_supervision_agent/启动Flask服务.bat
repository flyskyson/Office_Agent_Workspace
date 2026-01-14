@echo off
REM ========================================
REM 市场监管智能体 - Flask Web UI 启动脚本
REM ========================================
REM
REM 功能:
REM 1. 自动检查并安装依赖
REM 2. 使用虚拟环境 Python 启动服务
REM 3. 自动打开浏览器
REM
REM ========================================

cd /d "%~dp0"

echo.
echo ========================================
echo 市场监管智能体 v4.0 - 启动程序
echo ========================================
echo.

REM 检查虚拟环境
if not exist "venv_py312\Scripts\python.exe" (
    echo [ERROR] 虚拟环境不存在！
    echo 请先运行: python -m venv venv_py312
    pause
    exit /b 1
)

echo [1/4] 检查依赖...
venv_py312\Scripts\python.exe -c "from aip import AipOcr" 2>nul
if errorlevel 1 (
    echo.
    echo [!] 检测到依赖缺失，正在安装...
    echo.
    venv_py312\Scripts\pip.exe install -q chardet baidu-aip loguru flask python-docx pyyaml pypdf
    echo [OK] 依赖安装完成
    echo.
) else (
    echo [OK] 依赖检查通过
)

echo [2/4] 同步 requirements_v4.txt...
venv_py312\Scripts\pip.exe install -q -r requirements_v4.txt 2>nul
echo [OK] 依赖已同步

echo [3/4] 启动 Flask 服务...
echo.
echo ========================================
echo 服务将在以下地址启动:
echo   - 本地: http://127.0.0.1:5000
echo   - 局域网: http://192.168.3.224:5000
echo ========================================
echo.
echo 按 Ctrl+C 停止服务
echo.

REM 启动 Flask
venv_py312\Scripts\python.exe ui\flask_app.py

pause
