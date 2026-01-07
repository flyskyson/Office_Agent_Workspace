@echo off
chcp 65001 > nul
echo.
echo ============================================================
echo            超级管家 - 准备新对话
echo ============================================================
echo.
echo 正在生成报告...
echo.

python 超级管家.py --export

echo.
echo ============================================================
echo 报告已生成!
echo ============================================================
echo.
echo 现在你可以对新AI助手说:
echo.
echo "请读取: 06_Learning_Journal/workspace_memory/super_butler_report.json"
echo "然后告诉我: 我的工作区状态如何?"
echo.
echo 按任意键退出...
pause > nul
