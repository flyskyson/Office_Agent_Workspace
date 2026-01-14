@echo off
echo ====================================
echo 卸载 Python 3.14.2
echo ====================================
echo.
echo 此脚本需要管理员权限运行
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] 需要管理员权限！
    echo 请右键点击此文件，选择"以管理员身份运行"
    echo.
    pause
    exit /b 1
)

echo [OK] 已获得管理员权限
echo.

REM 删除 Python 3.14 目录
if exist "C:\Python314" (
    echo 正在删除 C:\Python314 ...
    rmdir /s /q "C:\Python314"
    if %errorLevel% equ 0 (
        echo [OK] Python 3.14 目录已删除
    ) else (
        echo [ERROR] 删除失败
    )
) else (
    echo [INFO] C:\Python314 不存在
)

echo.
echo ====================================
echo 完成！
echo ====================================
echo.
echo 现在默认 Python 版本应该是 3.12.9
echo 请关闭并重新打开命令行窗口
echo.
pause
