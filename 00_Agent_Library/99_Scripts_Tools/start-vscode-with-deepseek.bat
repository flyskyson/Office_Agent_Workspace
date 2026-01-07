@echo off
REM 启动 VSCode 并自动加载 DeepSeek API Key

echo Loading DeepSeek API Key...
for /f "tokens=2 delims==" %%A in ('wmic environment where "name='DEEPSEEK_API_KEY'" get value /value') do set API_KEY=%%A
set DEEPSEEK_API_KEY=%API_KEY%

echo.
echo ✓ DeepSeek API Key loaded
echo Starting VSCode...
echo.

code .

REM 如果需要在 VSCode 中打开新终端并保持环境变量:
REM code.cmd . -- &quot;&amp; { $env:DEEPSEEK_API_KEY = [System.Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY', 'User') }&quot;
