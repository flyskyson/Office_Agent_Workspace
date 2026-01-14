@echo off
REM Skill Creator CLI 启动脚本
REM 用法: skill_creator.bat [command] [options]

chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

REM 获取脚本目录（99_Scripts_Tools 的上级是 00_Agent_Library）
set "SCRIPT_DIR=%~dp0"
set "LIB_DIR=%SCRIPT_DIR%.."
set "SKILL_CREATOR=%LIB_DIR%\skill_creator.py"

REM 转换为完整路径
pushd "%LIB_DIR%"
set "LIB_DIR=%CD%"
popd

set "SKILL_CREATOR=%LIB_DIR%\skill_creator.py"

echo 🔧 Skill Creator CLI
echo 📁 工作目录: %CD%
echo.

REM 检查文件是否存在
if not exist "%SKILL_CREATOR%" (
    echo ❌ 错误: 找不到 skill_creator.py
    echo    预期路径: %SKILL_CREATOR%
    pause
    exit /b 1
)

REM 执行命令
python "%SKILL_CREATOR%" %*

if %errorlevel% neq 0 (
    echo.
    echo 💡 提示: 使用 --help 查看帮助
)
