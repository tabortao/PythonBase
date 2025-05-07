# Spark-TTS Windows安装教程

## 安装依赖
```bash
# 安装micromamba
Invoke-Expression ((Invoke-WebRequest -Uri https://micro.mamba.pm/install.ps1 -UseBasicParsing).Content)
# 下载代码
git clone https://github.com/SparkAudio/Spark-TTS.git

cd Spark-TTS


# 创建虚拟环境
micromamba create -n sparktts python=3.12 -y
micromamba activate sparktts
micromamba deactivate

# 安装依赖
pip install -r requirements.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple
# 或者按下述命令安装，使用阿里云镜像
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com

# 安装PyTorch
pip3 install torch==2.5.1 torchvision torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu126
```
## 下载模型
方式一：在Spark-TTS文件夹新建download_model.py, 粘贴如下内容并运行`python download_model.py`:
```python
from huggingface_hub import snapshot_download

snapshot_download("SparkAudio/Spark-TTS-0.5B", local_dir="pretrained_models/Spark-TTS-0.5B")

```
方式二：Git下载

```bash
mkdir -p pretrained_models

# Make sure you have git-lfs installed (https://git-lfs.com)
git lfs install

git clone https://hf-mirror.com/SparkAudio/Spark-TTS-0.5B pretrained_models/Spark-TTS-0.5B

```

## 运行模型
```bash
python webui.py
```
