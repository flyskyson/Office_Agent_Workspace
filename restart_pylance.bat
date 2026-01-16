@echo off
chcp 65001 >nul
cls
echo ========================================
echo Pylance 语言服务器重启工具
echo ========================================
echo.
echo 正在尝试重启 Pylance 语言服务器...
echo.
echo 请在 VSCode 中执行以下操作:
echo.
echo 步骤 1: 打开命令面板
echo   按 Ctrl+Shift+P
echo.
echo 步骤 2: 选择命令
echo   输入并选择: "Pylance: Restart Server"
echo   或者: "Python: Restart Language Server"
echo.
echo 步骤 3: 等待重启完成
echo   查看底部状态栏的 "Pylance" 指示器
echo.
echo ========================================
echo 其他解决方案:
echo ========================================
echo.
echo 方案 A: 选择 Python 解释器
echo   1. 按 Ctrl+Shift+P
echo   2. 输入 "Python: Select Interpreter"
echo   3. 选择: C:\Users\flyskyson\AppData\Local\Programs\Python\Python312\python.exe
echo.
echo 方案 B: 重载窗口
echo   1. 按 Ctrl+Shift+P
echo   2. 输入 "Developer: Reload Window"
echo.
echo 方案 C: 完全重启 VSCode
echo   关闭所有 VSCode 窗口，然后重新打开
echo.
echo 方案 D: 检查输出面板
echo   1. 按 Ctrl+Shift+U (打开输出面板)
echo   2. 在下拉菜单中选择 "Pylance"
echo   3. 查看是否有错误信息
echo.
pause
