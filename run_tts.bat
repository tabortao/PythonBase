@echo off
REM 设置标题
title index-TTS API 客户端执行器

REM 显示开始信息
echo 正在启动 index-TTS API 客户端...
echo.

REM 使用 uv run 执行 Python 脚本
uv run src\tts\tts_api_client.py

REM 脚本执行完成后显示信息并暂停
echo.
echo index-TTS API 客户端执行完成！
echo.
pause