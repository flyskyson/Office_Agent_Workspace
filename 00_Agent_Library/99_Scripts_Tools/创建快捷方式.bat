@echo off
echo ============================================
echo   创建桌面快捷方式和批处理文件
echo ============================================
echo.

cd /d C:\Users\flyskyson\Office_Agent_Workspace

echo 步骤1: 创建批处理启动文件...
echo.

REM 1. 今日启动器
echo @echo off > 启动今日启动器.bat
echo chcp 65001 ^> nul >> 启动今日启动器.bat
echo cd /d C:\Users\flyskyson\Office_Agent_Workspace >> 启动今日启动器.bat
echo python daily_launcher.py >> 启动今日启动器.bat
echo pause >> 启动今日启动器.bat
echo [OK] 创建: 启动今日启动器.bat

REM 2. 文件管理中心
echo @echo off > 启动文件管理中心.bat
echo chcp 65001 ^> nul >> 启动文件管理中心.bat
echo cd /d C:\Users\flyskyson\Office_Agent_Workspace >> 启动文件管理中心.bat
echo python file_manager_center.py >> 启动文件管理中心.bat
echo pause >> 启动文件管理中心.bat
echo [OK] 创建: 启动文件管理中心.bat

REM 3. 市场监管智能体
echo @echo off > 启动市场监管智能体.bat
echo chcp 65001 ^> nul >> 启动市场监管智能体.bat
echo cd /d C:\Users\flyskyson\Office_Agent_Workspace\01_Active_Projects\market_supervision_agent >> 启动市场监管智能体.bat
echo python 新版申请书填充工具.py >> 启动市场监管智能体.bat
echo pause >> 启动市场监管智能体.bat
echo [OK] 创建: 启动市场监管智能体.bat

echo.
echo ============================================
echo   批处理文件创建完成！
echo ============================================
echo.
echo 已创建的批处理文件:
echo   1. 启动今日启动器.bat
echo   2. 启动文件管理中心.bat
echo   3. 启动市场监管智能体.bat
echo.
echo 使用方法: 双击.bat文件即可启动对应工具
echo.
pause