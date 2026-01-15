@echo off
chcp 65001 >nul
echo ============================================================
echo                                                    新闻读取器
echo ============================================================
echo.
echo 正在启动...
echo.

python 00_Agent_Library\news_reader.py %*

pause
