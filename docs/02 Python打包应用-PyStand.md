# Python应用打包—PyStand

## 下载PyStand
1. 查看虚拟环境python版本，`MyOCR`项目采用的是Python-3.12.10-win32.
2. 选择32位的[PyStand下载](https://github.com/skywind3000/PyStand/releases),这里我下载了1.1.4版本的`PyStand-py38.7z`。
3. [下载嵌入式Python](https://www.python.org/downloads/windows/)，这里我下载了[python-3.12.10-embed-amd64.zip](https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip)（请注意32位pystand配32位python解释器，64位pystand配64位python解释器）
4. 将下载的PyStand-py38解压，重命名为PyStand-py312，并把python-3.12.10-embed-win32.zip解压放到runtime文件夹。

## 复制依赖
### 复制site-packages
1. 将uv虚拟环境`.venv\Lib\site-packages`文件夹下的依赖复制到`PyStand-py312\site-packages`。

2. 删掉与项目无关的包nuitka、pyinstaller等。

3. 打包tkinter模块

官方提供的嵌入式解释器并不包含pip工具，以及tkinter模块，下面的步骤是怎么补上这个tkinter模块。
> 注：本方法目的在于后续可以复用，所以并不按照官方的目录结构来。
- 复制tkinter模块。把tkinter文件夹`Python312\Lib\tkinter`复制到`PyStand-py312\runtime\Lib\`tkinter文件夹下。
- 复制tcl资源文件。复制tcl文件夹里面所有的文件`Python312\tcl`，到`PyStand-py312\runtime\`Lib文件夹下，tcl文件夹通常位于解释器的同级目录。(注意，这里是把`Python312\tcl`文件夹里面的所有内容，复制到`PyStand-py312\runtime\Lib`，不要搞错了)
![](https://lei-1258171996.cos.ap-guangzhou.myqcloud.com/imgs/2025/202506042351458.jpg)
- 复制二进制模块。复制_tkinter.pyd，tcl86t.dll，tk86t.dll、zlib1.dll（Python 3.12需要）三个文件到pystand/runtime/Lib文件夹下，这三个文件通常位于解释器的DLLs文件夹下。
- 修改路径。修改runtime文件夹里面的`python312._pth`文件，增加一行./Lib。注意，这里有个点，代表同级目录的Lib文件夹。

![](https://lei-1258171996.cos.ap-guangzhou.myqcloud.com/imgs/2025/202506042302913.jpg)

现在可以运行程序了。如果后续还需要打包tkinter模块。直接复制这里弄好的Lib文件夹跟`._pth`文件到runtime文件夹下即可实现复用。

## 复制项目代码
将代码复制到PyStand-py312目录，修改pystand.int中的代码，以文本编辑器打开该文件，直接清空内容，输入以下代码。这样就表示，从start函数启动程序。
```py
from main import start
if __name__ == "__main__":
    #运行入口函数
    start()
```
我们将main.py文件扔到了OCRmyPDF文件夹下，程序是不知道main.py文件在哪儿的，所以会报错：
```bash
from main import start.

ModuleNotFoundError: no module named "main"
```
（当然你也可以直接把main.py文件扔外面，不放在src文件夹下，这样就不会报错。）

所以我们需要告诉一下python，你需要去src目录找main模块，这里利用.pth文件。

新建main.txt文本文件（名称随意，程序自动加载.pth文件），里面写上OCRmyPDF，保存，修改后缀名为.pth，将该文件放在pystand.exe同级目录下。

tips：你要是觉得放在pystand.exe同级目录显得很乱，你可以将新建的main.pth放在其他地方，里面的路径也可以写其他相对路径，如./src，../src等

或者不创建main.pth了，去改runtime文件夹里面的`._pth`文件，加一行`../src`就ok了或者你代码里加`os.path.append("src")`也行的，就是改个搜索路径。

![](https://lei-1258171996.cos.ap-guangzhou.myqcloud.com/imgs/2025/202506042343547.jpg)

## 运行

双击pystand.exe，运行程序，可得到如期结果。到这儿，打包算初步完成。

！如果不能如期运行，可以使用cmd命令运行pystand.exe，可以查看到报错信息。

！如果需要自定义程序名字，需要同时修改pystand.exe及http://pystand.int两个文件，保持同名即可。

！如果觉得保持同名很麻烦，想允许用户自己随便改名，那么请将http://pystand.int改名为http://_pystand_static.int即可。

！如果觉得int文件有点碍眼，那就得修改pystand源码了，稍微改一下就可以让pystand去runtime里面找int文件，就可以藏起来了。（但是不推荐改，最好用韦神提供的exe，他拿去报白名单了，报毒概率低哦）

！如果需要自定义程序图标，请使用Resource Hacker 更换图标，非常简单。

！程序源代码是以源码形式放在script目录中的，建议使用nuitka批量将py文件转为pyd文件，提升运行速度的同时隐藏了源码。

## 修改程序图标

克隆项目https://github.com/skywind3000/PyStand ，替换appicon.ico图标为自己的应用，使用Github Action重新生成PyStand.exe

## 参考文章
- [python嵌入式打包，打包新姿势，打包速度比pyinstaller还快哦](https://zhuanlan.zhihu.com/p/691339803?share_code=1fr5TITEMEkcn&utm_psn=1913714962649559816)
