@echo off
chcp 65001 >nul
REM 设置工作目录
cd /d "%~dp0"

echo ========================================================================
echo 🌅 正在启动今日启动器...
echo ========================================================================
echo.
echo 工作目录: %CD%
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python
    echo.
    echo 请确保已安装 Python 并添加到 PATH 环境变量中
    echo.
    pause
    exit /b 1
)

REM 检查索引文件是否存在
if not exist "06_Learning_Journal\workspace_memory\workspace_index_latest.json" (
    echo ⚠️  工作区索引不存在，正在生成...
    echo.
    python workspace_scanner.py
    echo.
    if errorlevel 1 (
        echo ❌ 索引生成失败
        pause
        exit /b 1
    )
)

REM 验证 JSON 文件
echo 验证索引文件...
python -c "import json; json.load(open('06_Learning_Journal\workspace_memory\workspace_index_latest.json', 'r', encoding='utf-8'))" 2>nul
if errorlevel 1 (
    echo ❌ 索引文件损坏，正在重新生成...
    echo.
    python workspace_scanner.py
    echo.
    if errorlevel 1 (
        echo ❌ 索引生成失败
        pause
        exit /b 1
    )
)

echo ✅ 索引文件正常
echo.
echo ========================================================================
echo 正在启动今日启动器...
echo ========================================================================
echo.

python daily_launcher.py

if errorlevel 1 (
    echo.
    echo ========================================================================
    echo ❌ 程序运行出错
    echo ========================================================================
    echo.
    echo 如果问题持续存在，请运行 fix_workspace_index.bat
    echo.
    pause
)

