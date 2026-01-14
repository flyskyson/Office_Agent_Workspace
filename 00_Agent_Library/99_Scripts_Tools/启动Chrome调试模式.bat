@echo off
REM Chrome DevTools 远程调试启动脚本
REM 用于 Claude Code MCP 集成

echo.
echo ========================================
echo    Chrome 远程调试模式启动器
echo    端口: 9222
echo ========================================
echo.

REM 关闭所有现有 Chrome 进程
echo [1/3] 关闭现有 Chrome 进程...
taskkill /F /IM chrome.exe >nul 2>&1
timeout /t 2 >nul

REM 获取 Chrome 路径
echo [2/3] 查找 Chrome 安装路径...
set "CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe"
if not exist "%CHROME_PATH%" (
    set "CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
)

if not exist "%CHROME_PATH%" (
    echo [错误] 未找到 Chrome 浏览器！
    echo 请确认 Chrome 已安装在标准路径
    pause
    exit /b 1
)

echo [找到] %CHROME_PATH%

REM 启动 Chrome 并开启远程调试
echo [3/3] 启动 Chrome（远程调试端口 9222）...
start "" "%CHROME_PATH%" --remote-debugging-port=9222 --user-data-dir="%LOCALAPPDATA%\ChromeDebugProfile"

echo.
echo ✅ Chrome 已启动！
echo 📍 调试端口: http://localhost:9222
echo.
echo 💡 现在可以在 Claude Code 中使用 Chrome DevTools MCP
echo.
pause
