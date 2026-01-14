@echo off
REM AI 新闻追踪器 - Windows 任务计划程序设置脚本
REM 自动每天运行获取 AI 新闻

setlocal enabledelayedexpansion

echo.
echo ============================================
echo    AI 新闻追踪器 - 自动任务配置
echo ============================================
echo.

REM 获取工作区路径
set "WORKSPACE_DIR=%~dp0..\..\.."
set "PYTHON_SCRIPT=%WORKSPACE_DIR%\01_Active_Projects\ai_news_tracker\src\news_tracker.py"
set "OUTPUT_DIR=%WORKSPACE_DIR%\01_Active_Projects\ai_news_tracker\data"

echo [配置信息]
echo 工作区目录: %WORKSPACE_DIR%
echo Python 脚本: %PYTHON_SCRIPT%
echo 输出目录: %OUTPUT_DIR%
echo.

REM 检查脚本是否存在
if not exist "%PYTHON_SCRIPT%" (
    echo [错误] 未找到新闻追踪器脚本！
    echo 路径: %PYTHON_SCRIPT%
    pause
    exit /b 1
)

REM 删除现有任务（如果存在）
echo [1/4] 删除现有任务计划...
schtasks /delete /tn "AI_News_Daily" /f >nul 2>&1
schtasks /delete /tn "AI_News_Weekly" /f >nul 2>&1
echo   ✓ 已清理旧任务

REM 创建每日任务（每天早上 9:00 运行）
echo.
echo [2/4] 创建每日新闻任务...
schtasks /create /tn "AI_News_Daily" /tr "python \"%PYTHON_SCRIPT%\"" /sc daily /st 09:00 /ru "%USERNAME%" /f

if %errorlevel% equ 0 (
    echo   ✓ 每日任务创建成功（每天 09:00）
) else (
    echo   ✗ 创建失败，可能需要管理员权限
    echo   请以管理员身份运行此脚本
    pause
    exit /b 1
)

REM 创建每周任务（每周一早上 9:00 运行）
echo.
echo [3/4] 创建周报任务...
schtasks /create /tn "AI_News_Weekly" /tr "python \"%PYTHON_SCRIPT%\"" /sc weekly /d MON /st 09:00 /ru "%USERNAME%" /f

if %errorlevel% equ 0 (
    echo   ✓ 周报任务创建成功（每周一 09:00）
) else (
    echo   ⚠ 周报任务创建失败（可选）
)

REM 显示已创建的任务
echo.
echo [4/4] 验证任务配置...
echo.
echo ============================================
echo    已创建的自动任务
echo ============================================
echo.
schtasks /query /fo LIST /v | findstr /i "AI_News"
echo.

REM 创建快捷启动脚本
echo.
echo [额外] 创建手动运行脚本...
set "RUN_SCRIPT=%WORKSPACE_DIR%\00_Agent_Library\99_Scripts_Tools\运行AI新闻追踪.bat"

(
echo @echo off
echo echo 正在运行 AI 新闻追踪器...
echo echo.
echo python "%PYTHON_SCRIPT%"
echo echo.
echo echo 按任意键关闭...
echo pause ^>nul
) > "%RUN_SCRIPT%"

echo   ✓ 已创建手动运行脚本
echo   路径: %RUN_SCRIPT%
echo.

echo ============================================
echo    配置完成！
echo ============================================
echo.
echo 📅 自动任务：
echo    - 每日新闻: 每天 09:00
echo    - 每周报告: 每周一 09:00
echo.
echo 📁 新闻报告保存位置:
echo    %OUTPUT_DIR%\daily_news_YYYYMMDD.md
echo.
echo 💡 手动运行：
echo    - 双击: 运行AI新闻追踪.bat
echo    - 或运行: python "%PYTHON_SCRIPT%"
echo.
echo 🗑️  取消自动任务：
echo    schtasks /delete /tn "AI_News_Daily" /f
echo.
echo ============================================
echo.
pause
