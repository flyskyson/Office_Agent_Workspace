@echo off
chcp 65001 >nul
echo ========================================================================
echo 🏦 超级文件管理中心 - 快速启动
echo ========================================================================
echo.
echo 请选择操作:
echo.
echo 1. 📊 查看工作区状态
echo 2. 📁 整理文件
echo 3. 🧹 清理工作区
echo 4. 🔍 检查Git状态
echo 5. 📸 创建快照
echo 6. 📄 生成报告
echo 7. 🤖 智能推荐
echo 8. 🔧 运行维护
echo 9. 查看帮助
echo 0. 退出
echo.
set /p choice=请输入选项 (0-9):

if "%choice%"=="1" goto status
if "%choice%"=="2" goto organize
if "%choice%"=="3" goto clean
if "%choice%"=="4" goto git
if "%choice%"=="5" goto snapshot
if "%choice%"=="6" goto report
if "%choice%"=="7" goto auto
if "%choice%"=="8" goto maintenance
if "%choice%"=="9" goto help
if "%choice%"=="0" goto end
goto invalid

:status
python file_manager_center.py status
pause
goto end

:organize
echo.
echo 警告：此操作将移动文件！
set /p confirm=确认执行？(Y/N):
if /i not "%confirm%"=="Y" goto end
python file_manager_center.py organize
pause
goto end

:clean
echo.
echo 警告：此操作将删除缓存文件！
set /p confirm=确认执行？(Y/N):
if /i not "%confirm%"=="Y" goto end
python file_manager_center.py clean
pause
goto end

:git
python file_manager_center.py check-git
pause
goto end

:snapshot
python file_manager_center.py snapshot
pause
goto end

:report
python file_manager_center.py report
pause
goto end

:auto
python file_manager_center.py auto
pause
goto end

:maintenance
python file_manager_center.py maintenance
pause
goto end

:help
python file_manager_center.py help
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
