@echo off
chcp 65001 >nul
cls
echo ========================================
echo VSCode Python 语法高亮完全修复
echo ========================================
echo.
echo 问题分析：
echo - 工作区配置正常
echo - Python扩展已安装
echo - 但所有文件夹都没有语法高亮
echo.
echo 可能原因：
echo 1. Pylance扩展损坏或未正确加载
echo 2. VSCode全局配置问题
echo 3. Python扩展与VSCode版本不兼容
echo 4. 语言服务器进程卡死
echo.
echo ========================================
echo 解决方案 A: 重置Pylance扩展（推荐）
echo ========================================
echo.
echo 步骤：
echo 1. 按 Ctrl+Shift+X 打开扩展面板
echo 2. 搜索 "Pylance"
echo 3. 点击扩展右侧的小齿轮图标
echo 4. 选择 "禁用" (Disable)
echo 5. 等待3秒
echo 6. 再次点击齿轮图标
echo 7. 选择 "启用" (Enable)
echo 8. 重新加载窗口（会提示）
echo.
pause
echo.
echo ========================================
echo 解决方案 B: 清除VSCode缓存
echo ========================================
echo.
echo 步骤：
echo 1. 完全关闭VSCode（所有窗口）
echo 2. 删除以下文件夹：
echo    - %%USERPROFILE%%\.vscode\extensions\.obsolete
echo    - %%USERPROFILE%%\.vscode\cachedData
echo 3. 重新打开VSCode
echo.
echo 按任意键查看VSCode安装位置...
pause >nul
echo.
echo VSCode 配置位置：
where code
echo.
echo 扩展位置：
dir "%USERPROFILE%\.vscode\extensions" /b | findstr python
echo.
pause
