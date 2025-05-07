
**Micromamba** 是 [Mamba](https://mamba.readthedocs.io/en/latest/) 项目的一部分，它是 Conda 包管理器的一个轻量级、高效且快速的替代品。相比于传统的 Conda，Micromamba 提供了更小的安装体积和更快的性能，特别适合需要快速创建和管理虚拟环境的场景。

详见[Micromamba简介](Micromamba简介.md)
## 安装与升级

Windows Powershell安装

```bash
Invoke-Expression ((Invoke-WebRequest -Uri https://micro.mamba.pm/install.ps1 -UseBasicParsing).Content)
# 软件会被安装到如下目录
# 安装时候，可以自定义环境目录，如F:\Development\Python\micromamba
# C:\Users\Lei\micromamba\condabin
# C:\Users\Lei\AppData\Local\micromamba

# 升级
micromamba self-update
micromamba self-update --version 1.4.6 # 升级到某个版本

# 软件删除，需手动删除环境变量
Remove-Item -Recurse -Force $env:USERPROFILE\micromamba
# 刪除初始化文件 Init powershell profile at 'G:\Lei\Documents\WindowsPowerShell\profile.ps1'

```

![202504300924_PixPin](https://lei-1258171996.cos.ap-guangzhou.myqcloud.com/imgs/2025/202504300924643.png)

Pip缓存路径修改
```bash
# 查看现有pip缓存路径
pip cache dir
# 默认路径为下面，占用C盘空间，建议修改
c:\users\lei\appdata\local\pip\cache
# powershell执行下面命令，注意修改缓存路径
# 为当前用户修改pip缓存路径
[System.Environment]::SetEnvironmentVariable("PIP_CACHE_DIR", "D:\Development\Python\cache", [System.EnvironmentVariableTarget]::User)
# 为整个系统级修改缓存路径
[System.Environment]::SetEnvironmentVariable("PIP_CACHE_DIR", "D:\Development\Python\cache", [System.EnvironmentVariableTarget]::Machine)

# 重开一个powershell，执行下面命令，查看设置是否生效
echo $env:PIP_CACHE_DIR
# 下面这个路径的缓存，可以删除了
C:\Users\Lei\AppData\Local\pip\cache
# 注意下面这个路径，全局用户级pip会安装到这里
C:\Users\Lei\AppData\Roaming\Python\Python312
```


## 使用方法

```bash
# 创建环境，注意以管理员身份运行powershell
micromamba create -n py310 python=3.10

# 指定虚拟环境路径，注意不要新建py312文件夹
micromamba create -p F:\Code\TTS\index-tts\py312 python=3.12



# 激活虚拟环境
micromamba activate py310
# 激活指定路径的虚拟环境
micromamba activate F:\Code\TTS\index-tts\py312
# 运行指定环境的命令
micromamba run -p F:\Code\TTS\index-tts\py312 mycommand
micromamba deactivate
# 查看所有环境
micromamba env list
# 安装依赖
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
pip install -r requirements.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple
# 移除指定的虚拟环境
micromamba remove --name py310 --all # 删除某个虚拟环境

micromamba install -c conda-forge pynini==2.1.6
pip install WeTextProcessing --no-deps --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 命令行输入 nvidia-smi，查看显卡版本以及支持的Cuda版本

# 安装torch以及cuda支持的轮子，会自动安装合适自己电脑的版本
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
# 有时候需要安装Preview (Nightly)版本
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu126

# 使用 pip -m 确保使用虚拟环境中的 pip
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126



# 提示可能缺少模块importlib_resources的话
pip install importlib_resources==6.5.2 --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# micromamba导出项目依赖文件
micromamba list -p F:\Code\TTS\index-tts\py312 --export > requirements2.txt

# conda兼容的导出项目依赖文件
micromamba list -p F:\Code\TTS\index-tts\py312 --export | Select-String -NotMatch '^#' > requirements3.txt


# micromamba恢复环境
micromamba create --name <new_env_name> --file requirements.txt
micromamba create -p F:\Code\TTS\index-tts\py312 --file requirements2.txt




# 下载模型到当前目录的checkpoints目录下,详见下一步。
推荐使用下载工具，在hf-mirror下载模型，速度刚刚的。
https://hf-mirror.com/IndexTeam/Index-TTS/tree/main

# 最后运行gradio网页
python webui.py


pip3 uninstall torch torchvision torchaudio

# deepspeed安装
pip install deepspeed # 尝试多次，没法正常安装，尝试手动安装

# 阿里下载deepspeed编译好的Windows版本文件 deepspeed-0.16.5-cp310-cp310-win_amd64.whl
https://mirrors.aliyun.com/pypi/simple/deepspeed/
# 进入要安装到的python虚拟环境，并进入到文件所在目录，执行下列命令，手动安装deepspeed
pip install "deepspeed-0.16.5-cp310-cp310-win_amd64.whl"
pip install "deepspeed-0.16.3-cp312-cp312-win_amd64.whl"
# 测试cuda安装是否可以了，首先进入python
# 激活虚拟环境，首先输入
python
# 输出为true，说明安装成功了
import torch
torch.cuda.is_available()
torch.__version__
```


## 参考文章
- [Mamba--快速且跨平台的软件包管理器（conda的替代品）](https://mp.weixin.qq.com/s/8GXV_xiW5XVOtFaFqgfWbg)

## 问题解决

```bash
# 1. DeepSpeed加载失败: No module named 'deepspeed'
python -c "import torch; print(torch.__version__)"
# 2.7.0+cu126
确保下载安装好N卡驱动
https://www.nvidia.cn/geforce/drivers/


pip install deepspeed --index-url https://pypi.tuna.tsinghua.edu.cn/simple




```