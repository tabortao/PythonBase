import os
import time
from gradio_client import Client, handle_file
from typing import Literal, Optional, Union

class TTSClient:
    """
    文本转语音API客户端
    """
    def __init__(self, api_url: str = "http://localhost:7860/"):
        """
        初始化TTS客户端
        
        参数:
            api_url: API服务器地址，默认为本地服务器
        """
        self.client = Client(api_url)
        # 获取可用的音色列表
        self.available_voices = self.get_available_voices()
    
    def get_available_voices(self) -> list:
        """
        获取可用的音色列表
        
        返回:
            音色列表
        """
        try:
            result = self.client.predict(api_name="/change_choices")
            # 处理返回的结果，提取音色名称
            if isinstance(result, dict) and 'choices' in result:
                # 从choices中提取音色名称
                return [choice[0] for choice in result['choices']]
            elif isinstance(result, list):
                # 如果直接返回列表，则直接使用
                return result
            else:
                # 其他情况，打印结果并返回默认值
                print(f"获取音色列表返回了意外的格式: {result}")
                return ['使用参考音频']
        except Exception as e:
            print(f"获取音色列表失败: {e}")
            return ['使用参考音频']
    
    def text_to_speech(self, 
                       text: str, 
                       output_path: str,
                       voice_name: Optional[str] = "使用参考音频",
                       reference_audio: Optional[str] = None,
                       speed: float = 1.0) -> str:
        """
        将文本转换为语音
        
        参数:
            text: 要转换的文本
            output_path: 输出音频文件路径
            voice_name: 音色名称，默认使用参考音频
            reference_audio: 参考音频文件路径，当voice_name为"使用参考音频"时必须提供
            speed: 语速，默认为1.0
            
        返回:
            生成的音频文件路径
        """
        # 检查参数
        if voice_name == "使用参考音频" and reference_audio is None:
            raise ValueError("当选择'使用参考音频'时，必须提供参考音频文件路径")
        
        if voice_name not in self.available_voices:
            raise ValueError(f"无效的音色名称: {voice_name}。可用音色: {self.available_voices}")
        
        # 准备参考音频参数
        voice_param = None
        if voice_name == "使用参考音频":
            if not os.path.exists(reference_audio):
                raise FileNotFoundError(f"参考音频文件不存在: {reference_audio}")
            voice_param = handle_file(reference_audio)
        
        try:
            # 调用API生成语音
            result = self.client.predict(
                name=voice_name,
                voice=voice_param,
                text=text,
                speed=speed,
                api_name="/infer"
            )
            
            # 保存结果到指定路径
            if result:
                # 如果result是文件路径，复制文件到output_path
                if os.path.exists(result):
                    import shutil
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    shutil.copy2(result, output_path)
                    return output_path
            
            return result
        except Exception as e:
            print(f"生成语音失败: {e}")
            return None
    
    def save_voice(self, voice_name: str) -> bool:
        """
        保存音色
        
        参数:
            voice_name: 音色名称
            
        返回:
            是否保存成功
        """
        try:
            result = self.client.predict(
                name=voice_name,
                api_name="/save_audio"
            )
            return True if result else False
        except Exception as e:
            print(f"保存音色失败: {e}")
            return False


def text_file_to_speech(
    text_file_path: str,
    output_audio_path: str,
    voice_name: str = "使用参考音频",
    reference_audio: Optional[str] = None,
    speed: float = 1.0,
    api_url: str = "http://localhost:7860/"
) -> str:
    """
    将文本文件转换为语音文件
    
    参数:
        text_file_path: 文本文件路径
        output_audio_path: 输出音频文件路径
        voice_name: 音色名称，默认使用参考音频
        reference_audio: 参考音频文件路径，当voice_name为"使用参考音频"时必须提供
        speed: 语速，默认为1.0
        api_url: API服务器地址，默认为本地服务器
        
    返回:
        生成的音频文件路径
    """
    # 检查文本文件是否存在
    if not os.path.exists(text_file_path):
        raise FileNotFoundError(f"文本文件不存在: {text_file_path}")
    
    # 读取文本文件内容
    try:
        with open(text_file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
    except Exception as e:
        raise IOError(f"读取文本文件失败: {e}")
    
    # 初始化TTS客户端
    tts_client = TTSClient(api_url)
    
    # 调用API生成语音
    result_path = tts_client.text_to_speech(
        text=text_content,
        output_path=output_audio_path,
        voice_name=voice_name,
        reference_audio=reference_audio,
        speed=speed
    )
    
    return result_path


# 使用示例
if __name__ == "__main__":
    # uv run src\tts\tts_api_client.py
    start_time = time.time()
    # 示例1：使用预设音色
    book_name = "《贪心的小妖怪捉鲸鱼，声音的传播》"
    
    # 定义文本文件路径
    text_file_path_1 = os.path.join("src","output", "book_polished",f"{book_name}_1.txt")
    text_file_path_2 = os.path.join("src","output", "book_polished",f"{book_name}_2.txt")
    text_file_path_3 = os.path.join("src","output", "book_polished",f"{book_name}_3.txt")
    text_file_path_4 = os.path.join("src","output", "book_polished",f"{book_name}_4.txt")
    
    # 存储实际文本文件路径列表
    text_files = [text_file_path_1, text_file_path_2, text_file_path_3, text_file_path_4]
    
    # 检查文件是否存在
    existing_files = []
    for file_path in text_files:
        if os.path.exists(file_path):
            existing_files.append(file_path)
        else:
            print(f"警告: 文件不存在: {file_path}")
    
    if not existing_files:
        print("错误: 没有找到任何有效的文本文件!")
        exit(1)
    
    # 输出目录
    output_audio_path = os.path.join("src","output", "book_polished")
    
    # 初始化客户端并打印可用音色，帮助调试
    client = TTSClient()
    print(f"可用音色: {client.available_voices}")
    
    # 批量处理文本文件
    print(f"开始处理 {len(existing_files)} 个文本文件...")
    
    for i, file_path in enumerate(existing_files):
        print(f"正在处理文件 {i+1}/{len(existing_files)}: {file_path}")
        
        # 构建输出音频文件路径
        file_name = os.path.basename(file_path)
        base_name = os.path.splitext(file_name)[0]  # 获取不带扩展名的文件名
        output_file = os.path.join(output_audio_path, f"{base_name}.wav")
        
        try:
            # 读取文本内容
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            # 生成语音
            result = client.text_to_speech(
                text=text_content,
                output_path=output_file,
                voice_name="Lei.pt",
                speed=1.0
            )
            
            print(f"已生成音频: {output_file}")
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
    
    # 打印结果路径
    print(f"所有音频文件已保存到: {output_audio_path}")
    
    # 计算总耗时
    total_time = time.time() - start_time
    print(f"\n所有处理完成！总耗时: {total_time:.2f}秒")
