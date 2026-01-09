@echo off
chcp 65001 >nul
echo ========================================================================
echo 🔄 重新创建桌面快捷方式
echo ========================================================================
echo.
echo 这个脚本会:
echo 1. 设置 PowerShell 执行策略
echo 2. 重新创建所有桌面快捷方式
echo 3. 使用新的配置修复工作目录问题
echo.
echo 正在启动...
echo.

REM 检查是否有管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️  需要管理员权限
    echo.
    echo 正在请求管理员权限...
    echo.
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

REM 设置 PowerShell 执行策略
echo 步骤 1/2: 设置 PowerShell 执行策略...
powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"
if errorlevel 1 (
    echo ❌ 设置执行策略失败
    pause
    exit /b 1
)
echo ✅ 执行策略设置完成
echo.

REM 创建快捷方式
echo 步骤 2/2: 创建桌面快捷方式...
powershell -ExecutionPolicy Bypass -File "%~dp0create_shortcut.ps1"
if errorlevel 1 (
    echo ❌ 创建快捷方式失败
    pause
    exit /b 1
)
echo.
echo ========================================================================
echo ✅ 完成！
echo ========================================================================
echo.
echo 桌面快捷方式已重新创建！
echo.
echo 下一步:
echo 1. 关闭这个窗口
echo 2. 删除桌面上旧的快捷方式
echo 3. 使用桌面上新创建的快捷方式
echo.
echo 新创建的快捷方式:
echo   - Workspace Butler.lnk
echo   - File Manager Center.lnk
echo   - New Session Launcher.lnk
echo   - 📖 User Guide.lnk
echo.
pause
