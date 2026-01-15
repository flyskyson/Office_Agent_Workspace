@echo off
chcp 65001 >nul 2>&1
title 工作区新闻中心

:menu
cls
echo.
echo █━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━█
echo █                                                                █
echo █            📰 工作区新闻中心 📰                                  █
echo █                                                                █
echo █━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━█
echo.
echo 请选择：
echo.
echo   1. 启动新闻中心（交互式菜单）
echo.
echo   2. 获取微博热搜（Playwright 爬虫 - 真实数据）
echo.
echo   3. 获取多平台模拟数据
echo.
echo   4. 查看部署教程
echo.
echo   0. 退出
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

set /p choice="请选择 (0-4): "

if "%choice%"=="1" goto news_hub
if "%choice%"=="2" goto scraper
if "%choice%"=="3" goto mock
if "%choice%"=="4" goto guide
if "%choice%"=="0" goto end
goto invalid

:news_hub
cls
echo 正在启动新闻中心...
python news_hub.py
pause
goto menu

:scraper
cls
echo 正在获取微博热搜...
python 00_Agent_Library\news_scraper.py -p weibo -n 10
pause
goto menu

:mock
cls
echo 正在获取模拟数据...
python 00_Agent_Library\news_reader.py
pause
goto menu

:guide
cls
echo 📖 部署教程
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 【DailyHotApi - Vercel 部署】
echo.
echo 1. 访问 https://github.com/imsyy/DailyHotApi-Vercel
echo 2. Fork 项目
echo 3. 在 Vercel 导入并部署
echo 4. 获得 API 域名
echo.
echo 【TrendRadar - GitHub Actions】
echo.
echo 1. 访问 https://github.com/sansan0/TrendRadar
echo 2. Fork 项目
echo 3. 启用 GitHub Actions
echo 4. 运行 Workflow
echo.
echo 📄 详细文档：
echo    - docs\guides\DEPLOY_DAILYHOTAPI.md
echo    - docs\guides\TRENDRADAR_SETUP.md
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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
