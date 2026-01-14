@echo off
setlocal enabledelayedexpansion

echo.
echo ============================================
echo    Chrome DevTools MCP 演示启动器
echo ============================================
echo.

REM 步骤 1: 关闭现有 Chrome
echo [步骤 1/4] 关闭现有 Chrome 进程...
taskkill /F /IM chrome.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✓ Chrome 已关闭
) else (
    echo   - 没有运行中的 Chrome
)

REM 等待进程完全退出
echo.
echo [步骤 2/4] 等待进程清理...
timeout /t 2 /nobreak >nul

REM 步骤 3: 查找 Chrome 路径
echo.
echo [步骤 3/4] 定位 Chrome 浏览器...
set "CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe"
if not exist "!CHROME_PATH!" (
    set "CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
)
if not exist "!CHROME_PATH!" (
    echo   [错误] 未找到 Chrome 浏览器！
    echo   请确认 Chrome 已安装在标准路径
    pause
    exit /b 1
)
echo   ✓ 找到: !CHROME_PATH!

REM 步骤 4: 启动 Chrome 调试模式
echo.
echo [步骤 4/4] 启动 Chrome（远程调试端口 9222）...
start "" "!CHROME_PATH!" --remote-debugging-port=9222 --user-data-dir="%LOCALAPPDATA%\ChromeDebugProfile"

REM 等待 Chrome 启动
echo.
echo   等待 Chrome 启动...
timeout /t 3 /nobreak >nul

REM 验证端口
echo.
echo ============================================
echo    验证连接状态
echo ============================================
powershell -Command "$tcp = New-Object System.Net.Sockets.TcpClient; try { $tcp.Connect('localhost', 9222); if ($tcp.Connected) { Write-Host '✓ Chrome 调试端口 9222 已开启！' -ForegroundColor Green; $tcp.Close() } } catch { Write-Host '✗ 端口未开启，请稍等片刻后重试' -ForegroundColor Yellow }"

echo.
echo ============================================
echo    📖 使用指南
echo ============================================
echo.
echo 1. 在 Claude Code 中输入: /mcp
echo    查看可用的 MCP 服务器
echo.
echo 2. 对我说:
echo    - "用 Chrome 访问百度首页"
echo    - "帮我截图当前页面"
echo    - "分析页面性能"
echo.
echo 3. 调试地址:
echo    http://localhost:9222
echo.
echo ============================================
echo.
pause
