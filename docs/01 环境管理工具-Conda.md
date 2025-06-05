
## 简介

就像给你的电脑装上"多功能工具箱"，Anaconda能帮你：

✅ 环境隔离：为不同项目创建独立Python环境

✅包管理：一键安装600+

科学计算库（NumPy/Pandas/Matplotlib等）

✅ 跨平台：Windows/Mac/Linux全支持

## 安装

推荐下载源：
(1) 官网（国际版）：
https://www.anaconda.com/download

(2)清华镜像（国内加速）：

https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive

安装注意：
(1) 勾选"Add Anaconda to my PATH"（系统环境变量自动配置）
(2) 安装路径不要包含中文或空格

## 常见命令

```bash
# 1.环境管理
# 升级conda
conda update -n base -c defaults conda 

# 创建一个新环境，并指定 Python 版本
conda create --name env_name python=3.8
# 切换到某个虚拟环境
# 退出环境
conda activate env_name
conda deactivate
# 查看所有环境
conda env list
# 移除指定的虚拟环境
conda remove --name env_name --all # 删除某个虚拟环境

# 2.包管理
# 安装包
conda install package_name
# 更新已安装的包
conda update package_name
# 更新所有包
conda update --all
# 查看已安装的包
conda list
# 清理缓存：清理 Conda 的索引缓存和未使用的包文件
conda clean --all
# 添加通道：添加一个软件源（如 `conda-forge`）
conda config --add channels conda-forge
# 查看当前配置的通道
conda config --show channels
# 设置 `conda-forge` 为最高优先级
conda config --set channel_priority strict

# 其他命令
# 升级 Conda
conda update conda
# 安装更快的 Conda 替代工具 Mamba
conda install mamba -n base -c conda-forge
# 使用 Mamba 安装包
mamba install package_name
# 使用 Mamba 创建环境
mamba create --name env_name python=3.8 numpy pandas

# 导出当前环境的配置文件
conda env export > environment.yml
# 根据配置文件重建环境
conda env create -f environment.yml

```



## 环境配置 

20250429 【暂时放弃了，不要用，每次设置后都有问题】

1. 加速配置（清华镜像源）
  操作步骤（需管理员权限运行Anaconda Prompt）：
```
# 查看当前版本（验证安装）
conda --version  
conda info
# 启用通道地址显示（配置成功后可在C:\Users\用户名\.condarc查看）
conda config --set show_channel_urls yes
    执行以上命令后便可以在C盘的用户名文件夹下找到.condar文件并修改以下路径为对应安装的路径：
```
2. 设置加速源
用记事本打开.condarc文件，该文件在C盘/用户/用户名下，输入以下内容，是常用的清华、中科大和北外镜像源。
```bash
channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/win-64/
  - https://mirrors.bfsu.edu.cn/anaconda/pkgs/free/
  - https://mirrors.bfsu.edu.cn/anaconda/pkgs/main/
  - https://mirrors.bfsu.edu.cn/anaconda/cloud/conda-forge/
  - https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
  - https://mirrors.ustc.edu.cn/anaconda/pkgs/main/
  - https://mirrors.ustc.edu.cn/anaconda/cloud/conda-forge/
  - https://mirrors.ustc.edu.cn/anaconda/cloud/bioconda/
  - https://mirrors.ustc.edu.cn/anaconda/cloud/msys2/
  - https://mirrors.ustc.edu.cn/anaconda/cloud/menpo/
show_channel_urls: true
envs_dirs:
  - D:\ProgramData\miniconda3\envs
pkgs_dirs:
  - D:\ProgramData\miniconda3\pkgs
```
原本默认配置，"D:\ProgramData\miniconda3\.condarc",这里不能修改，需要conda config --set show_channel_urls yes进行创建。
```bash
channels:
  - https://repo.anaconda.com/pkgs/main
  - https://repo.anaconda.com/pkgs/r
  - https://repo.anaconda.com/pkgs/msys2
```

3. 清除缓存
```bash
conda clean -i
conda create -n myenv numpy # 创建虚拟环境
```

## 使用
```bash
cd intex-tts
conda create -n intex-tts python=3.10 # 创建虚拟环境，intex-tts为环境名，自己任意修改，python=3.10指定python版本
conda activate intex-tts
```

## 高阶用法

### 导出环境并重新创建
```bash
# 导出环境为 YAML 文件
conda env export > environment.yml # 注意导入前，打开environment.yml，修改最后的虚拟环境位置，与自己虚拟环境位置和名称相符。
# prefix: C:\Users\Lei\.conda\envs\index-tts
conda env create -f environment.yml
```


## 参考文章
- [Anaconda安装与使用，一文看懂。——人工智能与机器学习必备的环境管理工具「腾晓」](https://mp.weixin.qq.com/s/5pVqLRFtZ83fkMvdUxdeVg)
- [手把手教你搞定Anaconda环境配置（2025最新版）](https://mp.weixin.qq.com/s/t6XFMH92Cc_umqJiuT7X5g)
- [conda 使用笔记](https://mp.weixin.qq.com/s/AktsGh2uKa7KxDe5V_W4Xw)
- [Anaconda安装与使用，一文看懂。——人工智能与机器学习必备的环境管理工具「腾晓」](https://mp.weixin.qq.com/s/5pVqLRFtZ83fkMvdUxdeVg)
- [pytorch官网](https://pytorch.org/)
- [推荐！Anaconda清华仓库](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)
- [2025年Anaconda最新镜像源配置](https://mp.weixin.qq.com/s/MFj0IKLVF4Lx10kOsfx8NA)
