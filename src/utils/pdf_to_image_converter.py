#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件名: pdf_converter.py
功能: 批量将PDF文件转换为图片
作者: UV
创建日期: 2025-04-20
Python版本: 3.x
依赖包: 
    - PyMuPDF==1.25.5 (导入为fitz)
    - pathlib
使用说明:
    1. 将PDF文件放入指定目录
    2. 创建PDFConverter实例并调用convert_directory方法
    3. 自动将每个PDF转换为单独文件夹中的PNG图片
"""

import os
import time
import fitz
from pathlib import Path
from typing import List, Tuple, Optional

class PDFToImageConverter:
    def __init__(self, dpi: int = 300):
        """
        初始化PDF转图片转换器
        Args:
            dpi: 输出图片的分辨率，默认300
        """
        self.dpi = dpi
        self._matrix = fitz.Matrix(dpi/72, dpi/72)

    def convert_directory(self, pdf_directory: str) -> List[Tuple[str, int]]:
        """
        转换目录中的所有PDF文件
        Args:
            pdf_directory: PDF文件所在目录
        Returns:
            List[Tuple[str, int]]: 处理结果列表，每项为(PDF路径, 页面数)
        """
        pdf_files = [f for f in os.listdir(pdf_directory) 
                    if f.lower().endswith('.pdf')]
        
        print(f"\n找到 {len(pdf_files)} 个PDF文件待处理")
        
        results = []
        for index, pdf_file in enumerate(pdf_files, 1):
            print(f"\n[{index}/{len(pdf_files)}] ", end="")
            pdf_path = os.path.join(pdf_directory, pdf_file)
            result = self.convert_pdf(pdf_path)
            results.append(result)
        
        return results

    def convert_pdf(self, pdf_path: str) -> Tuple[str, int]:
        """
        转换单个PDF文件
        Args:
            pdf_path: PDF文件路径
        Returns:
            Tuple[str, int]: (PDF文件路径, 处理的页面数)，失败返回(路径, 0)
        """
        output_dir = self._create_output_directory(pdf_path)
        doc: Optional[fitz.Document] = None
        
        try:
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            print(f"\n开始处理: {os.path.basename(pdf_path)} (共 {total_pages} 页)")
            
            for page_num, page in enumerate(doc):
                self._process_page(page, page_num, output_dir, total_pages)
                
            print("\n转换完成！")
            return pdf_path, total_pages
            
        except Exception as e:
            print(f"\n处理 {pdf_path} 时发生错误: {str(e)}")
            return pdf_path, 0
            
        finally:
            if doc:
                doc.close()

    def _create_output_directory(self, pdf_path: str) -> str:
        """创建输出目录"""
        pdf_name = Path(pdf_path).stem
        output_dir = os.path.join(os.path.dirname(pdf_path), pdf_name)
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    def _process_page(self, page: fitz.Page, page_num: int, 
                     output_dir: str, total_pages: int) -> None:
        """处理单个页面"""
        # 生成并保存图片
        image_data = self._convert_page_to_image(page)
        output_path = os.path.join(output_dir, f'page_{page_num + 1}.png')
        self._save_image(image_data, output_path)
        
        # 显示进度
        progress = (page_num + 1) / total_pages * 100
        print(f"\r当前进度: {progress:.1f}% ({page_num + 1}/{total_pages}页)", end="")

    def _convert_page_to_image(self, page: fitz.Page) -> bytes:
        """将PDF页面转换为图片"""
        pix = page.get_pixmap(matrix=self._matrix)
        return pix.tobytes("png")

    def _save_image(self, image_data: bytes, output_path: str) -> None:
        """保存图片到文件"""
        with open(output_path, 'wb') as f:
            f.write(image_data)


def main():
    """主函数：程序入口"""
    start_time = time.time()
    
    # 创建转换器实例
    converter = PDFToImageConverter(dpi=300)
    
    # 设置PDF源文件目录
    pdf_directory = r"src\input\PDFs"
    
    # 执行转换
    results = converter.convert_directory(pdf_directory)
    
    # 打印转换结果
    for pdf_path, page_count in results:
        if page_count > 0:
            print(f"成功转换 {pdf_path}，共 {page_count} 页")
        else:
            print(f"转换失败: {pdf_path}")
            
    # 计算总耗时
    total_time = time.time() - start_time
    print(f"\n所有处理完成！总耗时: {total_time:.2f}秒")

if __name__ == "__main__":
    # uv run src\utils\pdf_to_image_converter.py
    main()