@echo off
REM 重启AI培训老师应用

echo ============================================
echo   重启 AI 培训老师
echo ============================================
echo.

echo [1/2] 停止旧进程...
taskkill /F /IM streamlit.exe 2>nul
timeout /t 2 /nobreak >nul

echo [2/2] 启动新进程...
cd /d "%~dp0ai_tutor_bot"
start "AI培训老师" cmd /k "streamlit run app.py"

echo.
echo 应用已重启！
echo 地址: http://localhost:8501
echo.
pause
