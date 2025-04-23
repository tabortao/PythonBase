@echo off
chcp 65001
setlocal enabledelayedexpansion

:: 创建临时文件夹
if not exist temp mkdir temp

:: 创建文件列表（使用UTF-8编码）
echo.>temp\filelist.txt

:: 生成2秒静音文件
ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 2 -q:a 9 -acodec libmp3lame temp\silence.mp3

:: 初始化计数器
set /a count=0

:: 首先将所有音频文件转换为相同格式的临时文件
for %%i in (*.mp3 *.wav *.aac *.flac *.m4a *.ogg *.opus *.wma *.amr) do (
    echo 正在处理: %%i
    ffmpeg -i "%%i" -ar 44100 -ac 2 -acodec libmp3lame -q:a 2 "temp\%%~ni_converted.mp3"
    echo file '%cd%\temp\%%~ni_converted.mp3'>>temp\filelist.txt
    echo file '%cd%\temp\silence.mp3'>>temp\filelist.txt
    set /a count+=1
)

:: 如果没有找到音频文件则退出
if %count%==0 (
    echo 当前目录没有找到支持的音频文件！
    echo 支持的格式：mp3, wav, aac, flac, m4a, ogg, opus, wma, amr
    rd /s /q temp
    exit /b
)

:: 使用ffmpeg合并所有文件（使用绝对路径）
ffmpeg -f concat -safe 0 -i temp\filelist.txt -c copy merged_output.mp3

:: 清理临时文件
rd /s /q temp

echo 音频合并完成！输出文件：merged_output.mp3
pause