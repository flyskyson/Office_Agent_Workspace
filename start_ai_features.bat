@echo off
REM ============================================================
REM AI 新功能快速启动脚本
REM 创建日期: 2026-01-14
REM ============================================================

echo.
echo ============================================================
echo    🚀 AI 新功能快速启动
echo ============================================================
echo.
echo 请选择要启动的功能:
echo.
echo [1] Gmail AI 启用指南
echo [2] 测试本地 AI 引擎
echo [3] 测试自然语言搜索
echo [4] 查看完整实施报告
echo [5] 全部测试
echo [0] 退出
echo.

set /p choice="请输入选项 (0-5): "

if "%choice%"=="1" goto gmail_ai
if "%choice%"=="2" goto local_ai
if "%choice%"=="3" goto natural_search
if "%choice%"=="4" goto report
if "%choice%"=="5" goto all_tests
if "%choice%"=="0" goto end

echo 无效选项，请重新运行脚本
goto end

:gmail_ai
cls
echo.
echo ============================================================
echo    📧 Gmail AI 启用指南
echo ============================================================
echo.
echo 正在打开 Gmail AI 设置指南...
echo.
start "" "00_Agent_Library\GMAIL_AI_SETUP_GUIDE.md"
echo.
echo ✅ 指南已打开，请按照步骤启用 Gmail AI 功能
echo.
pause
goto end

:local_ai
cls
echo.
echo ============================================================
echo    ⚡ 本地 AI 引擎测试
echo ============================================================
echo.
echo 正在测试本地 AI 引擎...
echo.
python "00_Agent_Library\local_ai_engine.py"
echo.
pause
goto end

:natural_search
cls
echo.
echo ============================================================
echo    🔍 自然语言搜索测试
echo ============================================================
echo.
echo 正在测试自然语言搜索...
echo.
python "00_Agent_Library\natural_language_search.py"
echo.
pause
goto end

:report
cls
echo.
echo ============================================================
echo    📊 AI 新技术实施报告
echo ============================================================
echo.
echo 正在打开完整实施报告...
echo.
start "" "AI_TECHNOLOGIES_IMPLEMENTATION_REPORT.md"
echo.
echo ✅ 报告已打开
echo.
pause
goto end

:all_tests
cls
echo.
echo ============================================================
echo    🧪 运行所有测试
echo ============================================================
echo.

echo [1/3] 测试本地 AI 引擎...
echo.
python "00_Agent_Library\local_ai_engine.py"
echo.

echo [2/3] 测试自然语言搜索...
echo.
python "00_Agent_Library\natural_language_search.py"
echo.

echo [3/3] 打开实施报告...
echo.
start "" "AI_TECHNOLOGIES_IMPLEMENTATION_REPORT.md"
start "" "00_Agent_Library\GMAIL_AI_SETUP_GUIDE.md"
echo.

echo ✅ 所有测试完成！
echo.
pause
goto end

:end
echo.
echo 感谢使用！
echo.
timeout /t 2 >nul
exit /b 0
