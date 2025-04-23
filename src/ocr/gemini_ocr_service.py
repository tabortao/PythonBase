import os
import time
import json
from typing import List, Dict, Optional
from pathlib import Path
from aichat.llm_gemini import GeminiClient

class GeminiOCRService:
    """使用Gemini实现OCR识别的服务类"""
    
    def __init__(self, config_path: str = None):
        """
        初始化OCR服务
        :param config_path: 配置文件路径，可选
        """
        self.client = GeminiClient(config_path)
    
    def recognize_image(self, image_path: str) -> str:
        """
        识别单张图片中的文字
        :param image_path: 图片路径
        :return: 识别结果文本
        """
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"图片不存在: {image_path}")
                
            result = self.client.multimodal_input(
                text="请识别图片中的文字，只需返回识别到的原始文本内容",
                image_path=image_path
            )
            
            # 处理返回结果，提取实际文本内容
            text = result.strip()
            if text.startswith("Here are the bounding box detections:"):
                # 尝试解析JSON格式的返回
                try:
                    import re
                    # 提取JSON字符串
                    json_str = re.search(r'```json\n(.*?)\n```', text, re.DOTALL)
                    if json_str:
                        import json
                        data = json.loads(json_str.group(1))
                        # 提取所有label中的文本
                        texts = [item['label'] for item in data if 'label' in item]
                        text = '\n'.join(texts)
                except:
                    pass
            
            # 如果是图片描述性文本，则返回空
            if text.startswith("That's") or text.startswith("I can") or "illustration" in text:
                return ""
                
            return text.strip()
            
        except Exception as e:
            print(f"识别图片 {image_path} 时发生错误: {str(e)}")
            return ""
    
    def batch_recognize(self, image_dir: str, output_path: Optional[str] = None) -> Dict[str, str]:
        """
        批量识别图片目录中的所有图片
        :param image_dir: 图片目录路径
        :param output_path: 结果输出路径，可选
        :return: 识别结果字典 {页码: 识别文本}
        """
        start_time = time.time()
        results = {}
        
        if not os.path.exists(image_dir):
            raise FileNotFoundError(f"目录不存在: {image_dir}")
        
        # 支持的图片格式
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
        
        # 获取所有图片文件并按数字顺序排序
        image_files = [
            f for f in os.listdir(image_dir) 
            if f.lower().endswith(supported_formats)
        ]
        # 按文件名中的数字排序
        image_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))) if any(c.isdigit() for c in x) else x)
        
        total_images = len(image_files)
        print(f"找到 {total_images} 个图片文件待处理")
        
        consecutive_failures = 0  # 连续识别失败计数
        
        for i, filename in enumerate(image_files, 1):
            image_path = os.path.join(image_dir, filename)
            print(f"[{i}/{total_images}] 正在处理: {filename}")
            
            try:
                text = self.recognize_image(image_path)
                
                # 检查识别结果是否为空
                if not text.strip():
                    consecutive_failures += 1
                    print(f"警告: 第 {i} 页未识别到内容")
                else:
                    consecutive_failures = 0  # 重置连续失败计数
                
                # 如果连续两次识别失败，退出程序
                if consecutive_failures >= 2:
                    print(f"\n错误: 连续 {consecutive_failures} 页未识别到内容，程序终止")
                    break
                
                # 使用"第X页"格式作为键
                page_key = f"第{i}页"
                results[page_key] = text
                
                # 显示进度
                progress = i / total_images * 100
                print(f"当前进度: {progress:.1f}%")
                
            except Exception as e:
                print(f"\n处理图片 {filename} 时出错: {str(e)}")
                page_key = f"第{i}页"
                results[page_key] = f"识别失败: {str(e)}"
                consecutive_failures += 1
                
                if consecutive_failures >= 2:
                    print(f"\n错误: 连续 {consecutive_failures} 页识别失败，程序终止")
                    break
        
        # 保存结果
        if output_path:
            self.save_json(results, output_path)
        
        total_time = time.time() - start_time
        print(f"\n处理完成! 总耗时: {total_time:.2f}秒")
        return results
    
    @staticmethod
    def save_json(data: Dict[str, str], output_path: str) -> None:
        """
        保存识别结果到JSON文件
        :param data: 识别结果字典
        :param output_path: 输出文件路径
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    try:
        ocr_service = GeminiOCRService()
        start_time = time.time()
        
        # 批量识别示例
        book_name = "《谁来拉雪橇：速度的快慢》"
        image_dir = os.path.join("src", "input", "PDFs", book_name)
        output_file = os.path.join("src", "output", f"{book_name}-gemini-ocr.json")        
        results = ocr_service.batch_recognize(image_dir, output_file)
        print(f"结果已保存到: {output_file}")
        
        total_time = time.time() - start_time
        print(f"\n所有处理完成！总耗时: {total_time:.2f}秒")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()