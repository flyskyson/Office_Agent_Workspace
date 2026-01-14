@echo off
chcp 65001 >nul
echo ============================================
echo Python 版本管理工具
echo ============================================
echo.
echo 当前默认版本:
py --version
echo.
echo 可用版本:
py --list
echo.
echo ============================================
echo 选择操作:
echo 1. 设置 Python 3.12 为全局默认
echo 2. 设置 Python 3.14 为全局默认
echo 3. 查看当前版本
echo 4. 仅对此项目使用 Python 3.12
echo.
set /p choice="请选择 (1-4): "

if "%choice%"=="1" goto set_312_global
if "%choice%"=="2" goto set_314_global
if "%choice%"=="3" goto show_version
if "%choice%"=="4" goto set_312_project

:set_312_global
echo.
echo 设置 Python 3.12 为全局默认...
echo 这需要管理员权限
echo.
py -3.12 -m pip install --upgrade pip
echo.
echo 完成！现在运行 'py' 将使用 Python 3.12
goto end

:set_314_global
echo.
echo 设置 Python 3.14 为全局默认...
echo 这需要管理员权限
echo.
py -3.14 -m pip install --upgrade pip
echo.
echo 完成！现在运行 'py' 将使用 Python 3.14
goto end

:show_version
echo.
echo 当前默认版本:
py --version
echo.
echo 所有版本:
py --list
goto end

:set_312_project
echo.
echo 为此项目创建 Python 3.12 启动脚本...
echo.

REM 创建启动脚本
echo @echo off > start_py312.bat
echo py -3.12 %%* >> start_py312.bat

echo.
echo 已创建 start_py312.bat
echo 使用方法: start_py312.bat script.py
echo.
goto end

:end
echo.
pause
