# PythonBase 项目

Python基础功能学习项目，集成多种AI和文档处理功能。
本项目远程仓库地址：https://gitee.com/tabortao/PythonBase

## 功能特性
- Gemini AI客户端 (支持文本生成、多模态输入、图片生成、音频转录)
- OCR功能 (支持PaddleOCR和EasyOCR)
- PDF处理 (PDF转图片、PDF内容提取)
- OpenAI兼容接口

## 安装依赖
```bash
pip install -e .
```

## 配置文件
项目使用`config.toml`作为配置文件，需要配置以下内容：
```toml
[google]
api_key = "your_api_key"
base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
models = ["gemini-pro"]
default_model = "gemini-pro"
```

## 使用示例
```python
from aichat.llm_gemini import GeminiClient

# 初始化客户端
gemini = GeminiClient()

# 文本生成
for chunk in gemini.text_completion("你好，请介绍一下你自己"):
    print(chunk, end="", flush=True)

# 多模态输入(文本+图片)
result = gemini.multimodal_input("这张图片里有什么?", "path/to/image.jpg")
print(result)

# 音频转录
transcript = gemini.audio_transcription("path/to/audio.m4a")
print(transcript)
```

## 项目结构
```
src/
├── aichat/          # AI聊天相关功能
│   └── llm_gemini.py  # Gemini客户端实现
docs/               # 项目文档
```

## 许可证
MIT License



        