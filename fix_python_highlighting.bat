@echo off
chcp 65001 >nul
echo ========================================
echo Python 语法高亮修复脚本
echo ========================================
echo.
echo 此脚本将帮助修复 Python 文件的语法高亮和代码提示问题
echo.
echo 步骤:
echo 1. ✓ 已更新 .vscode/settings.json 配置
echo 2. ✓ 已创建 .vscode/extensions.json 推荐扩展
echo.
echo ========================================
echo 已安装的 Python 扩展:
echo ========================================
code --list-extensions | findstr /i python
echo.
echo ========================================
echo 下一步操作:
echo ========================================
echo.
echo 方案 A: 在 VSCode 中重新加载窗口 (推荐)
echo   按 Ctrl+Shift+P
echo   输入 "Reload Window"
echo   按 Enter
echo.
echo 方案 B: 使用命令重载窗口
echo   在 VSCode 中按 Ctrl+Shift+P
echo   输入 "Developer: Reload Window"
echo.
echo 方案 C: 重启 VSCode
echo   关闭并重新打开 VSCode
echo.
pause
