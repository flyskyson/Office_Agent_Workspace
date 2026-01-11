@echo off
REM 学习记忆助手 - 安装脚本
REM Memory Agent Installation Script for Windows

echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                                                                    ║
echo ║     🧠  学习记忆助手  -  安装向导                                 ║
echo ║                                                                    ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

REM 切换到脚本目录
cd /d "%~dp0"

echo 📋 安装步骤：
echo.
echo 1. 检查Python环境
echo 2. 安装依赖包
echo 3. 下载嵌入模型（首次运行，约500MB）
echo 4. 构建索引
echo.

pause

echo.
echo [1/4] 🔍 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)
✅ Python环境正常
echo.

echo [2/4] 📦 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
✅ 依赖安装完成
echo.

echo [3/4] 📥 首次运行会自动下载嵌入模型...
echo    模型大小：约500MB
echo    请确保网络畅通
echo.

echo [4/4] 🚀 现在可以开始使用了！
echo.
echo ════════════════════════════════════════════════════════════════════
echo.
echo 📖 使用方法：
echo.
echo   1. 构建索引（首次使用必须）：
echo      python memory_agent.py index
echo.
echo   2. 交互模式（推荐）：
echo      python memory_agent.py
echo.
echo   3. 命令行搜索：
echo      python memory_agent.py search "你的查询"
echo.
echo ════════════════════════════════════════════════════════════════════
echo.
echo 💡 提示：
echo   - 首次运行需要下载模型，请耐心等待
echo   - 查看完整文档：README.md
echo   - 问题反馈：06_Learning_Journal/
echo.
pause
