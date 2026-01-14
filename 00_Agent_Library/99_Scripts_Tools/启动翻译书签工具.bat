@echo off
REM 启动智能翻译书签工具页面

set "HTML_FILE=%~dp0..\..\01_Active_Projects\smart_translator\browser_tools.html"

echo.
echo ============================================
echo    🌐 智能翻译书签工具
echo ============================================
echo.

if exist "%HTML_FILE%" (
    echo 正在打开书签工具页面...
    start "" "%HTML_FILE%"
    echo.
    echo ✅ 页面已在浏览器中打开
    echo.
    echo 💡 使用说明：
    echo    1. 选择推荐的翻译引擎
    echo    2. 复制书签代码到浏览器书签栏
    echo    3. 在任意网页点击书签即可翻译
    echo.
) else (
    echo [错误] 未找到书签工具页面！
    echo 路径: %HTML_FILE%
    echo.
    pause
    exit /b 1
)

pause
