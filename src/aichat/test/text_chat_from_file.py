import os
import sys
from pathlib import Path
from aichat.llm_openai import LLMChat

def test_file_chat():
    """
    测试从文件读取内容并进行AI对话的功能
    """
    try:
        # 初始化LLMChat实例
        chat = LLMChat()
        
        # 测试文件路径 - 转换为Path对象
        test_file = Path(__file__).parent.parent.parent / "output" / "1.txt"
        
        # 确保文件存在且有内容
        if not test_file.exists():
            test_file.parent.mkdir(parents=True, exist_ok=True)
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("请用中文润色文本")
        elif test_file.stat().st_size == 0:
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("请用中文润色文本")
        
        print(f"\n测试文件路径: {test_file}")
        print("文件内容:")
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
            print(content)
            if not content.strip():
                raise ValueError("输入文件内容不能为空")
        
        print("\n开始测试流式输出...")
        # 测试流式输出
        print("流式输出结果:")
        try:
            chat.sync_stream_chat_from_file(
                file_path=str(test_file),
                prompt_template="polish_book",
                service="ali",
                text=content  # 显式传递文本内容
            )
        except Exception as e:
            print(f"流式输出错误: {str(e)}")
            raise
        
        # 测试保存结果到文件
        output_file = Path(__file__).parent.parent.parent / "output" / "test_output.txt"
        print(f"\n测试将结果保存到文件: {output_file}")
        result_path = chat.stream_chat_to_file(
            input_file=str(test_file),
            output_file=str(output_file),
            service="ali"
        )
        
        if result_path:
            print(f"结果已保存到: {result_path}")
            print("输出文件内容:")
            with open(result_path, "r", encoding="utf-8") as f:
                print(f.read())
        
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")

if __name__ == "__main__":
    # uv run src\aichat\test\text_chat_from_file.py
    print("开始测试文件聊天功能...")
    test_file_chat()
    print("\n测试完成!")