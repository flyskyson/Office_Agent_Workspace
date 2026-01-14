@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================================================
echo 测试今日启动器
echo ========================================================================
echo.
echo 当前目录: %CD%
echo.
echo 检查 Python:
python --version
echo.
echo 检查索引文件:
dir "06_Learning_Journal\workspace_memory\workspace_index_latest.json"
echo.
echo 测试 JSON 解析:
python -c "import json; data = json.load(open('06_Learning_Journal\workspace_memory\workspace_index_latest.json', 'r', encoding='utf-8')); print('✅ JSON 有效'); print('项目数量:', len(data.get('projects', [])))"
echo.
echo ========================================================================
echo 如果上面的测试都通过了，按任意键启动今日启动器
echo ========================================================================
pause
python daily_launcher.py
