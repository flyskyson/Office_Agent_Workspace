@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo 市场监管智能体 v4.0
echo Python 3.12 稳定版本
echo ============================================
echo.
echo 选择功能:
echo.
echo 1. 启动 Web UI (Flask)
echo 2. 启动 Web UI (Streamlit - 可能不兼容)
echo 3. OCR 识别测试
echo 4. 数据库管理
echo 5. 生成申请书
echo 6. 数据编辑工具
echo 7. 查看系统状态
echo 8. 运行完整测试
echo.
set /p choice="请选择功能 (1-8): "

if "%choice%"=="1" goto flask_ui
if "%choice%"=="2" goto streamlit_ui
if "%choice%"=="3" goto ocr_test
if "%choice%"=="4" goto database
if "%choice%"=="5" goto generate
if "%choice%"=="6" goto edit_tool
if "%choice%"=="7" goto status
if "%choice%"=="8" goto test_all

:flask_ui
echo.
echo ============================================
echo 启动 Flask Web UI (Python 3.12)
echo ============================================
echo.
echo 访问地址: http://localhost:5000
echo 按 Ctrl+C 停止服务器
echo.
py -3.12 ui/flask_app.py
goto end

:streamlit_ui
echo.
echo ============================================
echo 启动 Streamlit Web UI
echo ============================================
echo.
echo 注意: Streamlit 可能与 Python 3.12 不兼容
echo.
py -3.12 -m streamlit run ui/app_minimal.py
goto end

:ocr_test
echo.
echo ============================================
echo OCR 识别测试
echo ============================================
echo.
set /p image_path="请输入图片路径: "
py -3.12 start_v4.py ocr --image "%image_path%"
goto end

:database
echo.
echo ============================================
echo 数据库管理
echo ============================================
echo.
py -3.12 -c "from src.database_manager import DatabaseManager; db = DatabaseManager(); ops = db.list_operators(limit=20); print(f'共 {len(ops)} 条记录'); [print(f\"ID={o['id']}: {o['operator_name']} - 电话: {o.get('phone','空')}\") for o in ops]"
echo.
pause
goto end

:generate
echo.
echo ============================================
echo 生成申请书
echo ============================================
echo.
set /p operator_id="请输入记录ID: "
py -3.12 start_v4.py generate --id %operator_id%
goto end

:edit_tool
echo.
echo ============================================
echo 数据编辑工具
echo ============================================
echo.
call 启动编辑工具.bat
goto end

:status
echo.
echo ============================================
echo 系统状态
echo ============================================
echo.
echo Python 版本:
py --version
echo.
echo 可用版本:
py --list
echo.
echo Python 3.12 虚拟环境:
if exist venv_py312\Scripts\python.exe (
    echo [OK] 虚拟环境已创建
) else (
    echo [未创建] 虚拟环境
)
echo.
echo 数据库记录:
py -3.12 -c "from src.database_manager import DatabaseManager; db = DatabaseManager(); print(f'  共 {len(db.list_operators())} 条记录')"
echo.
goto end

:test_all
echo.
echo ============================================
echo 运行完整测试
echo ============================================
echo.
py -3.12 start_v4.py test
goto end

:end
echo.
pause
