@echo off
chcp 65001 >nul
echo ========================================================================
echo 📁 每日文件整理器 - 快速启动
echo ========================================================================
echo.
echo 请选择操作:
echo.
echo 1. 📋 模拟运行（查看哪些文件会被移动，不实际执行）
echo 2. ✅ 执行整理（实际移动文件）
echo 3. 📄 查看最近的整理报告
echo 4. ⚙️  自定义运行（高级选项）
echo 0. 退出
echo.
set /p choice=请输入选项 (0-4):

if "%choice%"=="1" goto dry_run
if "%choice%"=="2" goto run_organize
if "%choice%"=="3" goto view_report
if "%choice%"=="4" goto custom
if "%choice%"=="0" goto end
goto invalid

:dry_run
echo.
echo ========================================================================
echo 🔍 模拟运行模式
echo ========================================================================
echo.
python daily_file_organizer.py --dry-run
echo.
pause
goto end

:run_organize
echo.
echo ========================================================================
echo ✅ 执行文件整理
echo ========================================================================
echo.
echo 警告：此操作将移动文件！
echo.
set /p confirm=确认执行？(Y/N):
if /i not "%confirm%"=="Y" goto end

python daily_file_organizer.py
echo.
echo 整理完成！
pause
goto end

:view_report
echo.
echo ========================================================================
echo 📄 查看整理报告
echo ========================================================================
echo.
echo 正在查找最新的整理报告...
for /f "delims=" %%i in ('dir /b /o-d "05_Outputs\Reports\file_organize_report_*.md" 2^>nul') do (
    set "latest_report=%%i"
    goto :found_report
)
echo 没有找到整理报告。
pause
goto end

:found_report
echo 最新报告: %latest_report%
echo.
type "05_Outputs\Reports\%latest_report%"
echo.
pause
goto end

:custom
echo.
echo ========================================================================
echo ⚙️  自定义运行
echo ========================================================================
echo.
echo 请输入完整命令，例如：
echo python daily_file_organizer.py --dry-run
echo python daily_file_organizer.py --workspace "D:\MyWorkspace"
echo.
set /p cmd=命令:
if not defined cmd goto invalid
%cmd%
echo.
pause
goto end

:invalid
echo.
echo ❌ 无效选项，请重新运行脚本
echo.
pause
goto end

:end
echo.
echo 感谢使用! 🎉
echo.
timeout /t 2 >nul
