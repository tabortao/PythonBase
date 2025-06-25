# 自创推荐Bat To Exe Converter +Inno

## 嵌入式Python处理
### 下载嵌入式Python
[下载嵌入式Python](https://www.python.org/downloads/windows/)，这里我下载了[python-3.12.10-embed-amd64.zip](https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip)，放到要制作的包的空文件夹，解压后命名为`py312`。

### 下载pip
[下载pip](https://bootstrap.pypa.io/get-pip.py)，放入到刚刚解压的安装包内（`py312`文件夹内）
随后在项目的根目录执行命令：
```bash
.\py312\python.exe .\py312\get-pip.py
```
![](https://lei-1258171996.cos.ap-guangzhou.myqcloud.com/imgs/2025/202506052256274.jpg)
注意这里的python.exe并不是本地开发环境的Python，而是嵌入式解释器的Python。

此时我们的目录中多出两个文件夹Lib和Scripts。
随后修改python312._pth文件，将内容改成下面这样：
```txt
python312.zip
.

# Uncomment to run site.main() automatically
import site
```
至此，嵌入式解释器就配置好了。

## 嵌入式安装依赖

此后，当我们需要安装依赖时，必须用嵌入式的解释器进行安装：
```bash
.\py312\python.exe -m pip install ocrmypdf -t F:\Code\OCR\MyOCR\dist\MyOCR-By-embed\py312\Lib\site-packages
```
上面的命令展示如何嵌入式安装依赖库noisereduce。

这里需要注意的时，解释器必须是嵌入式解释器.\python310\python.exe，同时通过-t参数来指定三方库的位置，也就是说，必须安装到项目的目录中，而不是系统的默认开发环境目录。

安装成功后，我们必须可以在项目的目录下可以找到这个库。




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


## 参考文章
- [一键整合,万用万灵,Python3.10项目嵌入式一键整合包的制作(Embed)](https://zhuanlan.zhihu.com/p/667231476?share_code=BLdYs8kAl6R2&utm_psn=1913751113619997502)