import base64
import toml
from openai import OpenAI
from typing import Optional, Union
from pathlib import Path
import os

class GeminiClient:
    def __init__(self, config_path: str = None):
        """
        初始化Gemini客户端
        :param config_path: 配置文件路径，如果为None则自动查找
        """
        try:
            # 自动确定配置文件路径
            if config_path is None:
                # 获取当前脚本所在目录
                script_dir = os.path.dirname(os.path.abspath(__file__))
                config_path = os.path.join(script_dir, "config.toml")
            
            # 从配置文件读取配置
            config = toml.load(config_path)
            google_config = config.get("google", {})
            
            self.client = OpenAI(
                api_key=google_config.get("api_key", ""),
                base_url=google_config.get("base_url", "https://generativelanguage.googleapis.com/v1beta/openai/")
            )
            self.models = google_config.get("models", ["gemini-2.0-flash"])
            self.default_model = google_config.get("default_model", "gemini-2.0-flash")
            # self.temperature = google_config.get("temperature", 0.7)
            
        except Exception as e:
            raise ValueError(f"初始化失败: {str(e)}")

    def text_completion(self, prompt: str, model: Optional[str] = None):
        """
        文本补全功能(仅流式输出)
        :param prompt: 输入的提示文本
        :param model: 使用的模型名称
        :return: 生成器(流式输出)
        """
        try:
            model = model or self.default_model
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            for chunk in response:
                yield chunk.choices[0].delta.content or ""
                
        except Exception as e:
            raise RuntimeError(f"文本生成失败: {str(e)}")

    def multimodal_input(self, text: str, image_path: str, model: Optional[str] = None):
        """
        多模态输入(文本+图片)
        :param text: 输入的文本
        :param image_path: 图片路径
        :param model: 使用的模型名称
        :return: 生成结果
        """
        try:
            model = model or self.default_model
            
            # 处理中文路径
            image_path = os.path.abspath(image_path)
            print(f"尝试加载图片路径: {image_path}")
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"图片文件不存在: {image_path}")
            
            # 编码图片为base64
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": text},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ]
            )
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"详细错误信息: {str(e)}")
            raise RuntimeError(f"多模态处理失败: {str(e)}")

    def generate_image(self, prompt: str, model: str = "imagen-3.0-generate-002"):
        """
        生成图片
        :param prompt: 生成图片的提示词
        :param model: 图片生成模型名称
        :return: 生成的图片(base64编码)
        """
        try:
            response = self.client.images.generate(
                model=model,
                prompt=prompt,
                response_format='b64_json',
                n=1
            )
            return response.data[0].b64_json
            
        except Exception as e:
            raise RuntimeError(f"图片生成失败: {str(e)}")

    def audio_transcription(self, audio_path: str, model: Optional[str] = None):
        """
        音频理解(转录)
        :param audio_path: 音频文件路径
        :param model: 使用的模型名称
        :return: 转录文本
        """
        try:
            model = model or self.default_model
            
            with open(audio_path, "rb") as audio_file:
                base64_audio = base64.b64encode(audio_file.read()).decode('utf-8')
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Transcribe this audio"},
                            {
                                "type": "input_audio",
                                "input_audio": {
                                    "data": base64_audio,
                                    "format": Path(audio_path).suffix[1:]  # 获取文件扩展名(不带点)
                                }
                            }
                        ]
                    }
                ]
            )
            return response.choices[0].message.content
            
        except Exception as e:
            raise RuntimeError(f"音频转录失败: {str(e)}")


# 使用示例
if __name__ == "__main__":
    try:
        # 初始化客户端
        gemini = GeminiClient()
        
        # 示例: 文本流式输出
        # print("流式输出示例:")
        # for chunk in gemini.text_completion("你好，请介绍一下你自己"):
        #     print(chunk, end="", flush=True)
        # print("\n")
        
        # 示例: 多模态输入(文本+图片)
        print("多模态输入示例:")
        image_path = r"F:\Code\PythonBase\src\input\image\父与子.jpg"
        prompt = "这张图片里有什么?请先识别输出所有文字，然后进行总结概括，请中文回复。"
        print(gemini.multimodal_input(prompt, image_path))
        
        # 示例: 生成图片，需要付费用户才能用
        # print("图片生成示例:")
        # image_data = gemini.generate_image("一只戴着帽子的猫")
        # with open("generated_image.jpg", "wb") as f:
        #     f.write(base64.b64decode(image_data))
        # print("图片已生成: generated_image.jpg")
        
        # 示例: 音频转录
        # print("音频转录示例:")
        # print(gemini.audio_transcription(r"F:\Code\PythonBase\src\input\audio\儿童公园喊话筒.wav"))
        
    except Exception as e:
        print(f"发生错误: {str(e)}")