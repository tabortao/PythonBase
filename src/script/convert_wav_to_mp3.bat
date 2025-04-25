@echo off
:: 设置控制台代码页为 UTF-8
chcp 65001
setlocal enabledelayedexpansion

:: 设置标题
title WAV 转 MP3 转换器

:: 显示欢迎信息
echo ===================================
echo    WAV 转 MP3 格式转换工具
echo ===================================
echo.

:: 检查 ffmpeg 是否安装
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到 ffmpeg。请确保 ffmpeg 已安装并添加到系统 PATH 中。
    echo 您可以从 https://ffmpeg.org/download.html 下载 ffmpeg。
    goto :end
)

:: 计数器初始化
set total=0
set converted=0
set failed=0

:: 统计需要转换的文件数量
for %%f in (*.wav) do (
    set /a total+=1
)

if %total% equ 0 (
    echo 当前目录下没有找到 WAV 文件。
    goto :end
)

echo 找到 %total% 个 WAV 文件需要转换。
echo.
echo 开始转换...
echo.

:: 创建输出目录
if not exist "mp3_output" mkdir "mp3_output"

:: 转换所有 WAV 文件
for %%f in (*.wav) do (
    echo 正在处理: %%f
    
    :: 获取不带扩展名的文件名
    set "filename=%%~nf"
    
    :: 转换文件（添加 -hide_banner 选项隐藏 ffmpeg 的额外输出）
    ffmpeg -hide_banner -i "%%f" -codec:a libmp3lame -qscale:a 2 "mp3_output\!filename!.mp3" -y -loglevel warning
    
    if !errorlevel! equ 0 (
        echo 转换成功: !filename!.mp3
        set /a converted+=1
    ) else (
        echo 转换失败: %%f
        set /a failed+=1
    )
    echo.
)

:: 显示转换结果
echo ===================================
echo 转换完成!
echo 总文件数: %total%
echo 成功转换: %converted%
echo 转换失败: %failed%
echo 输出目录: %cd%\mp3_output
echo ===================================

:end
echo.
echo 按任意键退出...
pause >nul