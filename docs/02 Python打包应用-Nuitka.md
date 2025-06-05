# 如何将 Python 程序打包成 exe 文件？

## Nuitka打包
### Nuitka简介
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

### Nuitka 在Windows系统如何安装使用

#### 安装 Nuitka
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

### Nuitka打包示意
```bash
python -m nuitka --standalone --onefile --windows-icon-from-ico=app_icon.ico --output-dir=dist --enable-plugin=tk-inter --windows-disable-console --include-data-file=app_icon.ico=app_icon.ico --include-data-dir=.venv/Lib/site-packages/ocrmypdf/data=ocrmypdf/data --onefile-compression=upx OCRmyPDF/main.py

# 注意修改include-data-dir 对应的路径，为ocrmypdf/data的相对路径

# 说明：
# --standalone：打包所有依赖为独立目录
# --onefile：生成单一exe（可选，首次启动慢）
# --windows-icon-from-ico=app_icon.ico：指定exe图标
# --windows-disable-console：打包exe时关闭控制台
# --enable-plugin=tk-inter：自动包含tkinter依赖
# --include-data-file/--include-data-dir：如需额外资源（如icon、模型、说明文档等）可用
# --output-dir=dist：输出到dist目录
# --output-filename：指定输出exe文件名
# --onefile-compression=upx：使用UPX压缩exe文件，体积小，但打包速度会慢一些

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
nuitka --standalone--lto=yes hello.py  # 启用链接时优化（Link Time Optimization）
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
