#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WAV 转 MP3 格式转换工具
将当前目录下的所有 WAV 文件转换为 MP3 格式
"""

import os
import subprocess
import time
import sys

def convert_wav_to_mp3():
    """
    将当前目录下的所有 WAV 文件转换为 MP3 格式
    """
    # 检查 ffmpeg 是否安装
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("错误: 未找到 ffmpeg。请确保 ffmpeg 已安装并添加到系统 PATH 中。")
        print("您可以从 https://ffmpeg.org/download.html 下载 ffmpeg。")
        return

    # 获取当前目录下的所有 WAV 文件
    wav_files = [f for f in os.listdir('.') if f.lower().endswith('.wav')]
    
    if not wav_files:
        print("当前目录下没有找到 WAV 文件。")
        return
    
    # 创建输出目录
    output_dir = "mp3_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 统计数据
    total = len(wav_files)
    converted = 0
    failed = 0
    
    print(f"===================================")
    print(f"    WAV 转 MP3 格式转换工具")
    print(f"===================================")
    print()
    print(f"找到 {total} 个 WAV 文件需要转换。")
    print()
    print("开始转换...")
    print()
    
    # 转换所有 WAV 文件
    for wav_file in wav_files:
        print(f"正在处理: {wav_file}")
        
        # 获取不带扩展名的文件名
        filename = os.path.splitext(wav_file)[0]
        mp3_file = os.path.join(output_dir, f"{filename}.mp3")
        
        # 记录开始时间
        start_time = time.time()
        
        try:
            # 使用 ffmpeg 转换文件
            subprocess.run([
                'ffmpeg', 
                '-i', wav_file, 
                '-codec:a', 'libmp3lame', 
                '-qscale:a', '2', 
                mp3_file, 
                '-y', 
                '-loglevel', 'warning'
            ], check=True)
            
            # 计算处理时间
            elapsed_time = time.time() - start_time
            
            print(f"转换成功: {filename}.mp3 (用时: {elapsed_time:.2f}秒)")
            converted += 1
        except subprocess.SubprocessError:
            print(f"转换失败: {wav_file}")
            failed += 1
        
        print()
    
    # 显示转换结果
    print("===================================")
    print("转换完成!")
    print(f"总文件数: {total}")
    print(f"成功转换: {converted}")
    print(f"转换失败: {failed}")
    print(f"输出目录: {os.path.abspath(output_dir)}")
    print("===================================")

if __name__ == "__main__":
    convert_wav_to_mp3()
    
    print()
    print("按 Enter 键退出...")
    input()