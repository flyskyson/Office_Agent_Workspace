@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo 市场监管智能体 - 数据编辑工具
echo ============================================
echo.
echo 选择模式:
echo 1. 命令行交互式编辑 (推荐)
echo 2. 启动 Web 界面 (Python 3.12)
echo 3. 直接更新电话号码
echo.
set /p choice="请选择 (1-3): "

if "%choice%"=="1" goto cmd_edit
if "%choice%"=="2" goto web_ui
if "%choice%"=="3" goto quick_update

:cmd_edit
echo.
echo 启动命令行编辑工具...
venv_py312\Scripts\python.exe test_form_submit.py
goto end

:web_ui
echo.
echo 启动 Web 界面 (Python 3.12)...
echo 访问地址: http://localhost:5000
echo.
venv_py312\Scripts\python.exe ui/flask_app.py
goto end

:quick_update
echo.
set /p operator_id="请输入记录ID: "
set /p phone="请输入新电话号码: "
venv_py312\Scripts\python.exe -c "from src.database_manager import DatabaseManager; db = DatabaseManager(); print('成功' if db.update_operator(%operator_id%, {'phone': '%phone%'}) else '失败')"
goto end

:end
echo.
pause
