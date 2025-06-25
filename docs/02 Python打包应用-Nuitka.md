# Python打包应用-Nuitka

如何将 Python 程序打包成 exe 文件？

## Nuitka简介
Nuitka 是一款用 Python 编写的优化型 Python 编译器，可直接生成无需独立安装器的可执行文件。数据文件既可选择内嵌打包，也可部署在程序外部。Nuitka 作为一款强大的 Python 程序打包工具，它将 Python 代码编译成单个的可执行文件（Windows系统下为 exe 文件），非常适合需要隐藏源码或便于移植的项目。与 PyInstaller 相比，Nuitka 生成的可执行文件体积更小，打包速度更快，尤其适合依赖大型第三方库的项目。

Nuitka 特性和优势主要有：
1. 核心特性
	- 全版本兼容：完美支持 Python 3（3.4至3.13）与 Python 2（2.6、2.7）双轨生态
	- 跨平台构建：适配 Windows/macOS/Linux 等主流系统，覆盖Python原生支持的任意环境
	- 编译级优化：通过C++转译实现运行效率提升（典型场景性能增益达30-300%）

2. 工业级优势
```bash
# 典型应用场景示例 
python -m nuitka --onefile --standalone --include-package=numpy app.py  # 生成含科学计算依赖的独立可执行文件
```
	- 二进制文件自带Python解释器核心（仅2-5MB增量）
	- 支持UPX压缩（可缩减最终体积达60%）


## Nuitka安装 
```bash
pip install nuitka  
# 或 
python -m pip install nuitka  
# 或 
uv add nuitka # uv用户推荐
python -m nuitka --version # 验证安装

# 运行nuitka时，会自动下载指定版本的mingw64,推荐
# C:\Users\Lei\AppData\Local\Nuitka\Nuitka\Cache\DOWNLO~1\gcc\x86_64\14.2.0posix-19.1.1-12.0.0-msvcrt-r2\mingw64\bin\

# MinGW64的下载地址：https://github.com/niXman/mingw-builds-binaries/releases，win10以上系统一般选择x86_64-14.2.0-release-win32-seh-ucrt-rt_v12-rev2.7z，解压到某个目录并将bin目录添加到环境变量里就算安装完成了
```
## Nuitka常用命令

```bash
--mingw64 #默认为已经安装的vs2017去编译，否则就按指定的比如mingw(官方建议)
--standalone 独立环境，这是必须的(否则拷给别人无法使用)
--windows-disable-console 没有CMD控制窗口
--output-dir=out 生成exe到out文件夹下面去
--show-progress 显示编译的进度，很直观
--show-memory 显示内存的占用
--enable-plugin=pyqt5
--plugin-enable=tk-inter 打包tkinter模块的刚需
--plugin-enable=numpy 打包numpy,pandas,matplotlib模块的刚需
--plugin-enable=torch 打包pytorch的刚需
--plugin-enable=tensorflow 打包tensorflow的刚需
--windows-icon-from-ico=你的.ico 软件的图标
--windows-company-name=Windows下软件公司信息
--windows-product-name=Windows下软件名称
--windows-file-version=Windows下软件的信息
--windows-product-version=Windows下软件的产品信息
--windows-file-description=Windows下软件的作用描述
--windows-uac-admin=Windows下用户可以使用管理员权限来安装
--linux-onefile-icon=Linux下的图标位置
--onefile 像pyinstaller一样打包成单个exe文件
--include-package=复制比如numpy,PyQt5 这些带文件夹的叫包或者轮子
--include-module=复制比如when.py 这些以.py结尾的叫模块
--output-dir=dist：输出到dist目录
--output-filename：指定输出exe文件名
--onefile-compression=upx：使用UPX压缩exe文件，体积小，但打包速度
--nofollow-imports：所有不是你写的代码（import的模块）全部不使用，交给python3x.dll执行
--follow-import-to=need ：need为你需要编译成C/C++的py文件夹命名，里面放你的py文件或者文件夹
--enable-plugin=tk-inter：自动包含tkinter依赖
--include-data-file/--include-data-dir：如需额外资源（如icon、模型、说明文档等）可用
--output-filename=OCRmyPDF.exe：输出文件名
```
### Nuitka打包示意
```bash
python -m nuitka --standalone --mingw64 --show-memory --show-progress --show-scons --nofollow-imports --windows-disable-console --windows-icon-from-ico=app_icon.ico --output-dir=dist --enable-plugin=tk-inter --follow-import-to=OCRmyPDF --include-data-file=app_icon.ico=app_icon.ico --include-data-dir=.venv/Lib/site-packages/ocrmypdf/data=ocrmypdf/data --include-package=ocrmypdf,pdfminer,pikepdf  --output-filename=OCRmyPDF.exe OCRmyPDF/main.py

# 注意修改include-data-dir 对应的路径，为ocrmypdf/data的相对路径；调试阶段可以去掉--windows-disable-console。

```


### 进阶参数与性能调优
1. 关键编译参数
```bash
--follow-imports # 递归打包所有依赖库（默认启用）
--include-package=mod # 强制包含指定包（处理动态导入问题）
--windows-icon=icon.ico	# 添加 EXE 文件图标
--remove-output	# 编译后删除临时文件
```

2. 性能优化技巧
```bash
# 编译为 C 代码（默认启用）
nuitka --standalone --lto=yes hello.py  # 启用链接时优化（Link Time Optimization）
# 多线程加速
nuitka --jobs=4 hello.py  # 使用 4 个 CPU 核心并行编译 
# 体积压缩，需提前安装 UPX 压缩工具
nuitka --standalone --onefile --enable-plugins=upx hello.py  #  
```
3. UPX 进一步压缩
[下载UPX](https://github.com/upx/upx/releases)并添加到环境变量
上述nuitka中添加 --onefile-compression=upx，使用UPX压缩exe文件，体积小，但打包速度会慢一些。

## 参考文章
- [Nuitka 安装使用教程：Python程序加密打包成exe新贵](https://mp.weixin.qq.com/s/XWhX4Hw2LFPvBLPOJy5UGw)

- [分享nuitka2.5和gcc的Mingw64的下载安装及python打包问题](https://www.bilibili.com/opus/1004021680028254247)

- [python打包exe的神器(nuitka)的详细教程](https://mp.weixin.qq.com/s/EYFwUmsJoYbccIl5lwRCvw)

- [Python打包exe的王炸-Nuitka](https://zhuanlan.zhihu.com/p/133303836?share_code=DFH2hv4wZRIW&utm_psn=1913709014929354778)

- [Python打包exe(32/64位)-Nuitka再下一城](https://zhuanlan.zhihu.com/p/141810934?share_code=4y5S9rAqSYVc&utm_psn=1913707335827817074)

