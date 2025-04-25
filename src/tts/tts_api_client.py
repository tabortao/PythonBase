import os
import time
from pathlib import Path
from typing import List, Optional, Union
from gradio_client import Client, handle_file
from tqdm import tqdm

class TTSClient:
    """
    文本转语音API客户端
    
    属性:
        client (Client): Gradio客户端实例
        available_voices (List[str]): 可用音色列表
    """
    def __init__(self, api_url: str = "http://localhost:7860/") -> None:
        """
        初始化TTS客户端
        
        参数:
            api_url: API服务器地址，默认为本地服务器
        """
        self.client = Client(api_url)
        self.available_voices = self._fetch_available_voices()

    def _fetch_available_voices(self) -> List[str]:
        """内部方法：获取可用音色列表"""
        try:
            result = self.client.predict(api_name="/change_choices")
            if isinstance(result, dict) and 'choices' in result:
                return [choice[0] for choice in result['choices']]
            elif isinstance(result, list):
                return result
            else:
                print(f"获取音色列表返回了意外的格式: {result}")
                return ['使用参考音频']
        except Exception as e:
            print(f"获取音色列表失败: {e}")
            return ['使用参考音频']

    def text_to_speech(
        self,
        text: str,
        output_path: Union[str, Path],
        voice_name: Optional[str] = "使用参考音频",
        reference_audio: Optional[Union[str, Path]] = None,
        speed: float = 1.0
    ) -> Optional[str]:
        """
        将文本转换为语音
        
        参数:
            text: 要转换的文本
            output_path: 输出音频文件路径(字符串或Path对象)
            voice_name: 音色名称，默认使用参考音频
            reference_audio: 参考音频文件路径(字符串或Path对象)
            speed: 语速，默认为1.0
            
        返回:
            生成的音频文件路径或None(失败时)
        """
        output_path = Path(output_path) if not isinstance(output_path, Path) else output_path
        
        # 参数验证
        if voice_name == "使用参考音频" and reference_audio is None:
            raise ValueError("当选择'使用参考音频'时，必须提供参考音频文件路径")
        
        if voice_name not in self.available_voices:
            raise ValueError(f"无效的音色名称: {voice_name}。可用音色: {self.available_voices}")

        # 准备参考音频参数
        voice_param = None
        if voice_name == "使用参考音频":
            ref_path = Path(reference_audio) if not isinstance(reference_audio, Path) else reference_audio
            if not ref_path.exists():
                raise FileNotFoundError(f"参考音频文件不存在: {ref_path}")
            voice_param = handle_file(str(ref_path))

        try:
            result = self.client.predict(
                name=voice_name,
                voice=voice_param,
                text=text,
                speed=speed,
                api_name="/infer"
            )
            
            if result and Path(result).exists():
                output_path.parent.mkdir(parents=True, exist_ok=True)
                import shutil
                shutil.copy2(result, str(output_path))
                return str(output_path)
            
            return result
        except Exception as e:
            print(f"生成语音失败: {e}")
            return None

    def save_voice(self, voice_name: str) -> bool:
        """保存音色到系统"""
        try:
            result = self.client.predict(
                name=voice_name,
                api_name="/save_audio"
            )
            return bool(result)
        except Exception as e:
            print(f"保存音色失败: {e}")
            return False


def text_file_to_speech(
    text_file_path: Union[str, Path],
    output_audio_path: Union[str, Path],
    voice_name: str = "使用参考音频",
    reference_audio: Optional[Union[str, Path]] = None,
    speed: float = 1.0,
    api_url: str = "http://localhost:7860/"
) -> Optional[str]:
    """
    将文本文件转换为语音文件
    
    参数:
        text_file_path: 文本文件路径(字符串或Path对象)
        output_audio_path: 输出音频文件路径(字符串或Path对象)
        voice_name: 音色名称，默认使用参考音频
        reference_audio: 参考音频文件路径(字符串或Path对象)
        speed: 语速，默认为1.0
        api_url: API服务器地址，默认为本地服务器
        
    返回:
        生成的音频文件路径或None(失败时)
    """
    text_path = Path(text_file_path) if not isinstance(text_file_path, Path) else text_file_path
    output_path = Path(output_audio_path) if not isinstance(output_audio_path, Path) else output_audio_path
    
    if not text_path.exists():
        raise FileNotFoundError(f"文本文件不存在: {text_path}")
    
    try:
        text_content = text_path.read_text(encoding='utf-8')
    except Exception as e:
        raise IOError(f"读取文本文件失败: {e}")
    
    tts_client = TTSClient(api_url)
    return tts_client.text_to_speech(
        text=text_content,
        output_path=output_path,
        voice_name=voice_name,
        reference_audio=reference_audio,
        speed=speed
    )


def _format_time(seconds: float) -> str:
    """格式化时间显示"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours}小时{minutes}分{seconds:.2f}秒"
    elif minutes > 0:
        return f"{minutes}分{seconds:.2f}秒"
    return f"{seconds:.2f}秒"


def main():
    """主函数，用于批量处理文本文件转语音"""
    start_time = time.time()
    
    # 方法一：执行book_polished文件夹下所有txt文件
    # 获取src/output/book_polished文件夹下所有txt文件(不含子文件夹)
    book_dir = Path("src") / "output" / "book_polished"
    text_files = [f for f in book_dir.glob("*.txt") if f.is_file()]
    
    # 方法二：自定义文件列表
    # text_files = [
    #     Path("src") / "output" / "book_polished" / "《穿靴子的猫》.txt",
    #     Path("src") / "output" / "book_polished" / "《造一个梦想的世界》.txt",
    #     Path("src") / "output" / "book_polished" / "《森林消失的绿岛，保护自然环境》.txt",
    #     Path("src") / "output" / "book_polished" / "《发明家图图和查理的火山旅行，火山的奥秘》.txt"
    # ]
    # 方法二：自定义单个文件 
    # text_files = [
    #     Path("src") / "output" / "book_polished" / "txt_test.txt"
    # ]
    
    # 过滤存在的文件
    existing_files = [f for f in text_files if f.exists()]
    if not existing_files:
        print("错误: 没有找到任何有效的文本文件!")
        return
    
    output_dir = Path("src") / "output" / "audio"
    client = TTSClient()
    print(f"可用音色: {client.available_voices}")
    print(f"开始处理 {len(existing_files)} 个文本文件...")
    
    for i, file_path in enumerate(tqdm(existing_files, desc="处理进度", unit="文件")):
        print(f"\n正在处理文件 {i+1}/{len(existing_files)}: {file_path}")
        print("模型处理时间较长，与电脑GPU能力相关，请耐心等待...")
        
        output_file = output_dir / f"{file_path.stem}.wav"
        file_start_time = time.time()
        
        try:
            text_content = file_path.read_text(encoding='utf-8')
            
            with tqdm(total=len(text_content), desc="文本转语音", unit="字符") as pbar:
                result = client.text_to_speech(
                    text=text_content,
                    output_path=output_file,
                    voice_name="Lei.pt",
                    speed=1.0
                )
                pbar.update(len(text_content) - pbar.n)
            
            file_time = time.time() - file_start_time
            print(f"已生成音频: {output_file}")
            print(f"文件处理耗时: {_format_time(file_time)} (总计{file_time:.2f}秒)")
            print(f"处理速度: {len(text_content)/file_time:.2f}字符/秒 (共{len(text_content)}字符)")
            print("-" * 50)
            
        except Exception as e:
            file_time = time.time() - file_start_time
            print(f"处理文件 {file_path} 时出错: {e}")
            print(f"失败处理耗时: {_format_time(file_time)} (总计{file_time:.2f}秒)")
            print("-" * 50)
    
    total_time = time.time() - start_time
    print(f"\n所有处理完成！总耗时: {_format_time(total_time)} (总计{total_time:.2f}秒)")


if __name__ == "__main__":
     # uv run src\tts\tts_api_client.py
    main()
