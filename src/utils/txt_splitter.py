import os
import math

def split_txt_file(file_path: str, num_parts: int):
    """
    将TXT文件按指定份数拆分为多个文件
    
    参数:
        file_path: TXT文件路径
        num_parts: 要拆分的份数
    
    返回:
        生成的文件路径列表
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    # 检查文件是否为TXT文件
    if not file_path.lower().endswith('.txt'):
        raise ValueError(f"文件必须是TXT格式: {file_path}")
    
    # 检查拆分份数是否有效
    if num_parts <= 0:
        raise ValueError(f"拆分份数必须大于0: {num_parts}")
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按段落拆分内容（空行分隔）
    paragraphs = content.split('\n\n')
    # 过滤掉空段落
    paragraphs = [p for p in paragraphs if p.strip()]
    
    # 计算每个文件应包含的段落数
    total_paragraphs = len(paragraphs)
    
    # 如果段落数小于拆分份数，调整拆分份数
    if total_paragraphs < num_parts:
        print(f"警告: 段落数({total_paragraphs})小于拆分份数({num_parts})，将调整为按段落数拆分")
        num_parts = total_paragraphs
    
    # 计算每个文件的段落数
    paragraphs_per_file = math.ceil(total_paragraphs / num_parts)
    
    # 获取原文件名（不含扩展名）和目录
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    file_name_without_ext = os.path.splitext(file_name)[0]
    
    # 创建输出文件
    output_files = []
    for i in range(num_parts):
        # 计算当前文件的段落范围
        start_idx = i * paragraphs_per_file
        end_idx = min((i + 1) * paragraphs_per_file, total_paragraphs)
        
        # 如果已经没有段落可处理，则退出循环
        if start_idx >= total_paragraphs:
            break
        
        # 构建当前文件的内容
        current_content = '\n\n'.join(paragraphs[start_idx:end_idx])
        
        # 构建输出文件路径
        output_file = os.path.join(file_dir, f"{file_name_without_ext}_{i+1}.txt")
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(current_content)
        
        output_files.append(output_file)
        print(f"已创建文件: {output_file}，包含 {end_idx - start_idx} 个段落")
    
    print(f"拆分完成！共创建了 {len(output_files)} 个文件")
    return output_files

def main():
    """
    主函数，用于测试文件拆分功能
    """
    # 示例用法
    book_name = "《贪心的小妖怪捉鲸鱼，声音的传播》"
    # 构建文件路径表达式
    txt_file = os.path.join("src","output", "book_polished",f"{book_name}.txt")
    
    # 调用拆分函数，将文件拆分为3份
    split_txt_file(txt_file, 4)

if __name__ == '__main__':
    # uv run src\utils\txt_splitter.py
    main()