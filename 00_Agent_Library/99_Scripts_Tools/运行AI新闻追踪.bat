@echo off
REM AI 新闻追踪器 - 手动运行脚本

echo.
echo ============================================
echo    🤖 AI 新闻追踪器
echo ============================================
echo.

set "WORKSPACE_DIR=%~dp0..\..\.."
set "PYTHON_SCRIPT=%WORKSPACE_DIR%\01_Active_Projects\ai_news_tracker\src\news_tracker.py"

echo 正在运行 AI 新闻追踪器...
echo.

python "%PYTHON_SCRIPT%"

echo.
echo ============================================
echo    运行完成
echo ============================================
echo.

REM 打开输出目录
echo 📁 打开新闻报告目录...
explorer "%WORKSPACE_DIR%\01_Active_Projects\ai_news_tracker\data"

echo.
pause
