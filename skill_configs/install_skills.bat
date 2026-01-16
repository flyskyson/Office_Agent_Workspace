@echo off
REM -*- coding: utf-8 -*-
REM Office Agent Workspace - 技能一键安装脚本
REM 将生成的技能包安装到 Claude Code

chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================================================
echo 🚀 Office Agent Workspace - 技能安装脚本
echo ========================================================================
echo.

REM 设置路径
set WORKSPACE_ROOT=%~dp0
set SKILLS_DIR=%WORKSPACE_ROOT%05_Outputs\skills\packages
set CLAUDE_SKILLS_DIR=%USERPROFILE%\.claude\skills

REM 创建 Claude skills 目录
if not exist "%CLAUDE_SKILLS_DIR%" (
    echo 📁 创建 Claude skills 目录: %CLAUDE_SKILLS_DIR%
    mkdir "%CLAUDE_SKILLS_DIR%"
)

echo.
echo 📦 开始安装技能包...
echo.

REM 统计安装数量
set /a count=0

REM 遍历所有 ZIP 文件
for %%f in ("%SKILLS_DIR%\*.zip") do (
    set "filename=%%~nxf"

    echo 📦 安装: !filename!

    REM 解压到 Claude skills 目录
    powershell -Command "Expand-Archive -Path '%%f' -DestinationPath '%CLAUDE_SKILLS_DIR%\%%~nf' -Force"

    if !errorlevel! equ 0 (
        echo    ✅ 安装成功
        set /a count+=1
    ) else (
        echo    ❌ 安装失败
    )
    echo.
)

echo ========================================================================
echo ✅ 安装完成! 共安装 !count! 个技能
echo ========================================================================
echo.
echo 📁 安装位置: %CLAUDE_SKILLS_DIR%
echo.
echo 💡 提示:
echo    1. 重启 Claude Code 以加载新技能
echo    2. 在对话中使用 @技能名 调用技能
echo.
echo 📋 已安装技能:
dir /b "%CLAUDE_SKILLS_DIR%" 2>nul
echo.

pause
