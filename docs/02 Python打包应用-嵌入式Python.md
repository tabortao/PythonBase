# 自创推荐Bat To Exe Converter +Inno

1. 编写OCRmyPDF.bat，双击这个批处理命令，可以启动软件界面
```bash
@echo off
pushd %~dp0
echo Current directory is: %cd%
echo The program is starting, please wait...
set PYTHON_PATH=.\.venv\Scripts\python.exe
timeout /t 3 /nobreak > nul 
"%PYTHON_PATH%" OCRmyPDF/main.py
pause
```
2. Bat转Exe
使用软件`Bat To Exe Converter`把OCRmyPDF.bat转换为`OCRmyPDF.exe`
![](https://lei-1258171996.cos.ap-guangzhou.myqcloud.com/imgs/2025/202506041658179.jpg)

3. 使用Inno打包为exe安装程序