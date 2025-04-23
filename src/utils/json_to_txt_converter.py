import json
import os

def convert_json_to_txt(json_file_path: str, output_file_path: str = None):
    """
    将JSON文件转换为指定格式的TXT文件
    Args:
        json_file_path: JSON文件路径
        output_file_path: 输出TXT文件路径，如果为None则自动生成
    """
    # 如果未指定输出路径，则自动生成
    if output_file_path is None:
        output_file_path = json_file_path.rsplit('.', 1)[0] + '.txt'
    
    # 读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 转换并写入TXT文件
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for page_num in sorted(data.keys(), key=lambda x: int(''.join(filter(str.isdigit, x)))):
            content = data[page_num].strip()
            # 如果内容为空则跳过
            if not content:
                continue
            
            # 如果内容不为空，添加句号（如果末尾没有标点符号）
            if not content[-1] in ['。', '！', '？', '：', '…', '.', '!', '?', ':']:
                content += '。'
            
            # 写入内容和换行
            f.write(f"{content}请翻到下一页。\n\n")

def main():
    # 指定输入文件路径
    book_name = "《谁来拉雪橇：速度的快慢》"
    # 修正：直接使用完整的json文件路径
    json_file = os.path.join("src", "output", f"{book_name}.json")
    
    # 调用转换函数
    convert_json_to_txt(json_file)
    print(f"转换完成！输出文件保存在：{json_file.rsplit('.', 1)[0] + '.txt'}")

if __name__ == '__main__':
    # uv run src\utils\json_to_txt_converter.py
    main()