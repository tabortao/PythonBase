import os
import sys
import toml
from openai import OpenAI, APIError
from typing import Generator, Optional, Dict, Any
from pathlib import Path

class LLMChat:
    def __init__(self, config_path: str = None):
        """
        初始化LLMChat类
        :param config_path: 配置文件路径
        """
        try:
            # Get the directory containing the script
            script_dir = Path(__file__).parent
            # Use provided config_path or default to config.toml in script directory
            self.config_path = Path(config_path) if config_path else script_dir / "config.toml"
            
            self.config = toml.load(self.config_path)
            self.clients: Dict[str, OpenAI] = {}
            self._init_clients()
        except FileNotFoundError:
            print(f"错误: 找不到配置文件 {self.config_path}")
            sys.exit(1)
        except Exception as e:
            print(f"错误: 初始化失败 - {str(e)}")
            sys.exit(1)

    def _init_clients(self):
        """初始化所有LLM客户端"""
        services = ['openai', 'ali', 'openrouter','Vercel2Gemin']
        for service in services:
            if service in self.config:
                self.clients[service] = OpenAI(
                    base_url=self.config[service]['base_url'],
                    api_key=self.config[service]['api_key']
                )

    def _get_client_and_model(self, service: str = None, model: str = None) -> tuple[OpenAI, str]:
        """
        获取客户端和模型
        :param service: 服务名称
        :param model: 模型名称
        :return: (客户端实例, 模型名称)
        """
        if service is None:
            # 默认使用第一个可用的服务
            service = next(iter(self.clients.keys()))

        if service not in self.clients:
            raise ValueError(f"未找到服务: {service}")

        if model is None:
            model = self.config[service]['default_model']
        elif model not in self.config[service]['models']:
            raise ValueError(f"服务 {service} 不支持模型: {model}")

        return self.clients[service], model

    def _format_prompt(self, text: str, prompt_template: str = None, **kwargs) -> str:
        """
        格式化提示词
        :param text: 输入文本
        :param prompt_template: 提示词模板名称
        :return: 格式化后的提示词
        """
        if prompt_template and prompt_template in self.config['prompts']:
            return self.config['prompts'][prompt_template].format(**kwargs)
        return text

    def stream_chat(self, text: str, service: str = None, model: str = None, 
                   prompt_template: str = None, **kwargs) -> Generator:
        """
        基础流式输出
        :param text: 用户输入文本
        :param service: 服务名称
        :param model: 模型名称
        :param prompt_template: 提示词模板名称
        :return: 生成器对象
        """
        try:
            client, model = self._get_client_and_model(service, model)
            formatted_text = self._format_prompt(text, prompt_template, **kwargs)
            
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": formatted_text}],
                stream=True,
                temperature=self.config[service].get('temperature', 0.7)
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except APIError as e:
            print(f"API错误: {str(e)}")
        except Exception as e:
            print(f"错误: {str(e)}")

    def sync_stream_chat(self, text: str, service: str = None, model: str = None,
                        prompt_template: str = None, **kwargs) -> None:
        """
        同步流式输出
        :param text: 用户输入文本
        :param service: 服务名称
        :param model: 模型名称
        :param prompt_template: 提示词模板名称
        """
        try:
            for text in self.stream_chat(text, service, model, prompt_template, **kwargs):
                print(text, end='', flush=True)
            print()
        except Exception as e:
            print(f"错误: {str(e)}")

    def sync_stream_chat_from_file(self, file_path: str, service: str = None, model: str = None,
                             prompt_template: str = None, **kwargs) -> None:
        """
        从文件读取内容并进行同步流式对话
        :param file_path: 文本文件路径
        :param service: 服务名称
        :param model: 模型名称
        :param prompt_template: 提示词模板名称
        """
        try:
            # 直接调用stream_chat_from_file处理文件内容
            for text in self.stream_chat_from_file(
                file_path=file_path,
                service=service,
                model=model,
                prompt_template=prompt_template,
                **kwargs
            ):
                print(text, end='', flush=True)
            print()  # 输出完成后换行
            
        except FileNotFoundError as e:
            print(f"错误: 找不到文件 {file_path}")
        except ValueError as e:
            print(f"参数错误: {str(e)}")
        except APIError as e:
            print(f"API服务错误: {str(e)}")
        except Exception as e:
            print(f"未知错误: {str(e)}")
            import traceback
            print(f"错误堆栈:\n{traceback.format_exc()}")

    def stream_chat_from_file(self, file_path: str, service: str = None, model: str = None,
                            prompt_template: str = None, **kwargs) -> Generator:
        """
        从文件读取内容并进行流式对话
        :param file_path: 文本文件路径
        :param service: 服务名称
        :param model: 模型名称
        :param prompt_template: 提示词模板名称
        :return: 生成器对象
        """
        try:
            # 读取文本文件
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
                
            # 调用现有的stream_chat方法处理文本内容
            yield from self.stream_chat(
                text=text_content,
                service=service,
                model=model,
                prompt_template=prompt_template,
                **kwargs
            )
                    
        except FileNotFoundError:
            print(f"错误: 找不到文件 {file_path}")
        except Exception as e:
            print(f"错误: 处理文件时发生错误 - {str(e)}")

    def stream_chat_to_file(self, input_file: str, output_file: str, service: str = None, 
                           model: str = None, prompt_template: str = None, **kwargs) -> str:
        """
        从文件读取内容并将AI回复保存到文件
        :param input_file: 输入文本文件路径
        :param output_file: 输出文本文件路径
        :param service: 服务名称
        :param model: 模型名称
        :param prompt_template: 提示词模板名称
        :return: 输出文件路径
        """
        try:
            # 读取文本文件
            with open(input_file, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            # 创建输出文件的目录（如果不存在）
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 收集AI回复内容
            result = ""
            for chunk in self.stream_chat(
                text=text_content,
                service=service,
                model=model,
                prompt_template=prompt_template,
                **kwargs
            ):
                result += chunk
            
            # 将结果写入文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            
            return output_file
                    
        except FileNotFoundError:
            print(f"错误: 找不到输入文件 {input_file}")
            return ""
        except Exception as e:
            print(f"错误: 处理文件时发生错误 - {str(e)}")
            return ""

def main():
    # 示例用法
    chat = LLMChat()
    
    # 测试默认问答模式
    # print("默认问答模式示例:")
    # chat.sync_stream_chat("你好，请介绍一下你自己。")
    
    # 测试使用prompt模板
    # print("\n使用prompt模板示例:")
    # chat.sync_stream_chat("人工智能", prompt_template="joke", subject="人工智能")
    
    # 测试指定服务和模型
    # print("\n指定服务和模型示例:")
    # chat.sync_stream_chat("你好,介绍下你自己？", service="ali", model="qwen-plus")
    # chat.sync_stream_chat("你好,介绍下你自己？", service="openrouter")
    # chat.sync_stream_chat("人工智能",service="openrouter", prompt_template="joke", subject="人工智能")
    # chat.sync_stream_chat("你好,介绍下你自己？", service="Vercel2Gemin", model="gemini-2.5-pro-exp-03-25")

    # 测试从文件读取内容
    print("\n从文件读取内容示例:")
    test_file = r"F:\Code\PythonBase\src\output\1.txt"
    
    try:
        # 检查文件是否存在
        if not os.path.exists(test_file):
            raise FileNotFoundError(f"找不到文件: {test_file}")
            
        print(f"正在处理文件: {test_file}")
        print("文件内容处理中...")
        
        # 测试文件读取功能
        chat.sync_stream_chat_from_file(
            file_path=test_file,
            service="ali"  # 指定使用的服务，可以根据需要修改
        )
        
        print("\n处理完成!")
        
    except FileNotFoundError as e:
        print(f"文件错误: {str(e)}")
    except Exception as e:
        print(f"处理过程中发生错误:")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        import traceback
        print(f"错误堆栈:\n{traceback.format_exc()}")

if __name__ == "__main__":
    main()