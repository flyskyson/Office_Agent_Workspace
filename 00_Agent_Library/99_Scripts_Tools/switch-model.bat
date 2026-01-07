@echo off
REM Claude Code 模型切换脚本 (Windows 批处理版)
REM 使用方法: switch-model.bat sonnet|haiku|opus|deepseek|deepseek-reasoner

setlocal

if "%1"=="" (
    echo 用法: switch-model.bat sonnet^|haiku^|opus^|deepseek^|deepseek-reasoner
    echo.
    echo 可用模型:
    echo   sonnet           - Claude Sonnet 4.5 (平衡)
    echo   haiku            - Claude Haiku 4.5 (快速)
    echo   opus             - Claude Opus 4.5 (最强)
    echo   deepseek         - DeepSeek Chat (高性价比)
    echo   deepseek-reasoner - DeepSeek Reasoner (强化推理)
    goto :eof
)

set "MODEL=%1"
set "CONFIG_DIR=.claude"
set "SETTINGS_FILE=%CONFIG_DIR%\settings.local.json"
set "CONFIG_FILE=%CONFIG_DIR%\config-%MODEL%.json"

REM 检查配置文件是否存在
if not exist "%CONFIG_FILE%" (
    echo 错误: 配置文件不存在: %CONFIG_FILE%
    goto :eof
)

REM 备份当前配置
if exist "%SETTINGS_FILE%" (
    for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
    set "TIMESTAMP=%datetime:~0,8%_%datetime:~8,6%"
    set "BACKUP_FILE=%CONFIG_DIR%\settings.backup.%TIMESTAMP%.json"
    copy "%SETTINGS_FILE%" "%BACKUP_FILE%" >nul
    echo 已备份当前配置到: %BACKUP_FILE%
)

REM 复制选定的配置
copy "%CONFIG_FILE%" "%SETTINGS_FILE%" /Y >nul

REM 显示当前配置
set "MODEL_NAME="
if "%MODEL%"=="sonnet" set "MODEL_NAME=Sonnet 4.5 (平衡)"
if "%MODEL%"=="haiku" set "MODEL_NAME=Haiku 4.5 (快速)"
if "%MODEL%"=="opus" set "MODEL_NAME=Opus 4.5 (最强)"
if "%MODEL%"=="deepseek" set "MODEL_NAME=DeepSeek Chat (高性价比)"
if "%MODEL%"=="deepseek-reasoner" set "MODEL_NAME=DeepSeek Reasoner (强化推理)"

echo.
echo √ 已切换到模型: %MODEL_NAME%
echo 配置文件: %SETTINGS_FILE%

REM DeepSeek 特殊提示
if "%MODEL:~0,8%"=="deepseek" (
    echo.
    echo 提示: 确保 DEEPSEEK_API_KEY 环境变量已设置
    echo       设置命令: set DEEPSEEK_API_KEY=your-api-key
) else (
    echo.
    echo 提示: 重启 VSCode 或重新加载 Claude Code 窗口以应用更改
)

endlocal
