@echo off
chcp 65001
REM 设置标题
title index-TTS API 客户端执行器

REM 显示开始信息
echo 正在启动 index-TTS API 客户端...
echo.

REM 检查uv命令是否可用
where uv >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo 错误: 未找到uv命令，请确保已安装并添加到PATH
    pause
    exit /b 1
)

REM 使用完整路径执行Python脚本
set SCRIPT_PATH=%~dp0src\tts\tts_api_client.py
if not exist "%SCRIPT_PATH%" (
    echo 错误: 找不到脚本文件 %SCRIPT_PATH%
    pause
    exit /b 1
)

REM 执行脚本并捕获错误
uv run "%SCRIPT_PATH%"
if %ERRORLEVEL% neq 0 (
    echo.
    echo 错误: TTS API 客户端执行失败！
    pause
    exit /b 1
)

REM 脚本执行完成后显示信息并暂停
echo.
echo index-TTS API 客户端执行成功！
echo.
pause