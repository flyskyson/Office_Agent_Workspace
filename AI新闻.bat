@echo off
chcp 65001 >nul 2>&1
title AI 技术新闻看板

:menu
cls
echo.
echo █━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo █                                                                █
echo █            🤖 AI 技术新闻看板 🤖                                █
echo █                                                                █
echo █━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 请选择：
echo.
echo   1. 启动 AI 新闻看板（交互式菜单）
echo.
echo   2. 快速获取 AI 新闻聚合
echo.
echo   3. 查看 AI 工具追踪
echo.
echo   4. 智能监控（学习您的兴趣）
echo.
echo   5. 管理兴趣关键词
echo.
echo   0. 退出
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

set /p choice="请选择 (0-5): "

if "%choice%"=="1" goto news_hub
if "%choice%"=="2" goto aggregator
if "%choice%"=="3" goto tracker
if "%choice%"=="4" goto monitor
if "%choice%"=="5" goto interests
if "%choice%"=="0" goto end
goto invalid

:news_hub
cls
echo 正在启动 AI 新闻看板...
python news_hub.py
pause
goto menu

:aggregator
cls
echo 正在获取 AI 新闻聚合...
python 00_Agent_Library\ai_news_aggregator.py
pause
goto menu

:tracker
cls
echo 正在追踪 AI 工具更新...
python 01_Active_Projects\ai_news_tracker\src\news_tracker.py
pause
goto menu

:monitor
cls
echo 正在启动智能新闻监控...
python 00_Agent_Library\smart_news_monitor.py
pause
goto menu

:interests
cls
echo 兴趣关键词管理
echo.
type 06_Learning_Journal\workspace_memory\user_interests.json 2>nul
echo.
echo.
echo 💡 提示：这些关键词用于智能筛选AI新闻
echo.
pause
goto menu

:invalid
cls
echo ❌ 无效选择！
pause
goto menu

:end
cls
echo 👋 感谢使用！
timeout /t 2 >nul
exit
