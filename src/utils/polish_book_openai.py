import os
import sys
from pathlib import Path
from aichat.llm_openai import LLMChat

def polish_book(file_path: str, output_file_path: str):
    """
    测试从文件读取内容并进行AI对话的功能
    """
    try:
        # 初始化LLMChat实例
        chat = LLMChat()
        
        print("文件内容:")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            print(content)
            if not content.strip():
                raise ValueError("输入文件内容不能为空")
        
        print("流式输出结果:")
        try:
            # 确保传递正确的参数
            chat.sync_stream_chat_from_file(
                file_path=str(file_path),
                prompt_template="polish_book_1",
                service="ali",
                # text=content  # 确保传递文本内容
            )
        except Exception as e:
            print(f"流式输出错误: {str(e)}")
            raise
        
        # 测试保存结果到文件
        
        print(f"\n将结果保存到文件: {output_file_path}")
        result_path = chat.stream_chat_to_file(
            input_file=str(file_path),
            output_file=str(output_file_path),
            service="ali"
        )
        
        if result_path:
            print(f"结果已保存到: {result_path}")
            print("输出文件内容:")
            with open(result_path, "r", encoding="utf-8") as f:
                print(f.read())
        
    except Exception as e:
        print(f"发生错误: {str(e)}")

def main():
    print("正在进行AI润色...")
    book_name = "《谁来拉雪橇：速度的快慢》"
    # 修正：直接使用完整的json文件路径
    file_path = os.path.join("src", "output", f"{book_name}.txt")
    output_file_path = os.path.join("src", "output","book_polished", f"{book_name}_polished.txt")
    polish_book(file_path,output_file_path)
    print("\n润色完成!")

if __name__ == "__main__":
    # uv run src\utils\polish_book_openai.py
    main()