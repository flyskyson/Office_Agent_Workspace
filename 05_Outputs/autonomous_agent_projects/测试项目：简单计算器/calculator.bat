@echo off
REM 简单计算器启动脚本 (Windows)
REM 使用方法: calculator.bat 运算符 数字1 数字2
REM 示例: calculator.bat add 10 5

python "%~dp0main.py" %*
