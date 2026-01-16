@echo off
chcp 65001 >nul
cls
echo ========================================
echo Python 环境诊断工具
echo ========================================
echo.

echo [1/6] 检查 Python 安装...
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Python 已安装
    python --version
) else (
    echo ✗ Python 未安装
)
echo.

echo [2/6] 检查 VSCode Python 扩展...
echo 已安装的 Python 相关扩展:
code --list-extensions | findstr /i python
if %errorlevel% equ 0 (
    echo ✓ Python 扩展已安装
) else (
    echo ✗ 未找到 Python 扩展
)
echo.

echo [3/6] 检查 VSCode 配置文件...
if exist ".vscode\settings.json" (
    echo ✓ .vscode\settings.json 存在
    echo   包含 Python 配置:
    findstr /i "python" .vscode\settings.json | findstr /i "languageServer analysis"
) else (
    echo ✗ .vscode\settings.json 不存在
)
echo.

echo [4/6] 检查 Python 解释器...
python -c "import sys; print(f'  解释器路径: {sys.executable}'); print(f'  Python 版本: {sys.version}')" 2>nul
if %errorlevel% equ 0 (
    echo ✓ Python 解释器正常
) else (
    echo ✗ Python 解释器异常
)
echo.

echo [5/6] 检查 Python 模块...
python -c "import pathlib; import json; print('  ✓ 核心模块可用')" 2>nul
if %errorlevel% equ 0 (
    echo ✓ Python 模块正常
) else (
    echo ✗ Python 模块异常
)
echo.

echo [6/6] 测试文件语法检查...
echo 创建测试文件...
echo # -*- coding: utf-8 -*- > test_syntax.py.tmp
echo import sys >> test_syntax.py.tmp
echo from pathlib import Path >> test_syntax.py.tmp
echo. >> test_syntax.py.tmp
echo if __name__ == "__main__": >> test_syntax.py.tmp
echo     print("Hello World") >> test_syntax.py.tmp
move /y test_syntax.py.tmp test_syntax.py >nul 2>&1
echo ✓ 已创建 test_syntax.py
echo.

echo ========================================
echo 诊断完成!
echo ========================================
echo.
echo 建议操作:
echo 1. 重新加载 VSCode 窗口 (Ctrl+Shift+P ^> "Reload Window")
echo 2. 打开 test_syntax.py 检查是否有语法高亮
echo 3. 检查 VSCode 状态栏是否显示 Python 解释器
echo 4. 如果没有高亮,手动选择语言模式: 点击右下角 ^> 选择 "Python"
echo.
pause
