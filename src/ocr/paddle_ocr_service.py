import os
import json
import time
from typing import List, Dict, Optional

class PaddleOCRService:
    """PaddleOCR服务类，封装OCR相关操作"""
    
    def __init__(self, model_path: str = None, lang: str = "ch"):
        """初始化OCR服务
        Args:
            model_path: 模型存储路径，默认为None则使用当前目录下的paddle_models
            lang: 识别语言，默认中文
        """
        # 设置模型路径
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), 'paddle_models')
        
        # 设置环境变量（必须在导入paddleocr之前设置）
        os.environ['PADDLE_HOME'] = model_path
        os.environ['PADDLE_OCR_PATH'] = os.path.join(model_path, '.paddleocr', 'whl')
        
        # 在设置完环境变量后再导入PaddleOCR
        from paddleocr import PaddleOCR
        
        # 模型路径配置
        self.det_model_dir = os.path.join(model_path, '.paddleocr', 'whl', 'det', 'ch', 'ch_PP-OCRv4_det_infer')
        self.rec_model_dir = os.path.join(model_path, '.paddleocr', 'whl', 'rec', 'ch', 'ch_PP-OCRv4_rec_infer')
        self.cls_model_dir = os.path.join(model_path, '.paddleocr', 'whl', 'cls', 'ch_ppocr_mobile_v2.0_cls_infer')
        
        # 初始化OCR实例
        self.ocr = self._init_ocr(lang, PaddleOCR)
        
    def _init_ocr(self, lang: str, PaddleOCR) -> 'PaddleOCR':
        """初始化PaddleOCR实例"""
        return PaddleOCR(
            use_angle_cls=True,
            lang=lang,
            use_gpu=False,
            det_model_dir=self.det_model_dir,
            rec_model_dir=self.rec_model_dir,
            cls_model_dir=self.cls_model_dir
        )
    
    def recognize_image(self, image_path: str) -> List[Dict]:
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"图片不存在: {image_path}")
                
            result = self.ocr.ocr(image_path, cls=True)
            if not result or not result[0]:
                return []
                
            return [
                {
                    'text': line[1][0],
                    'confidence': line[1][1],
                    'position': line[0]
                }
                for line in result[0]
            ]
        except Exception as e:
            print(f"识别图片 {image_path} 时发生错误: {str(e)}")
            return []
    
    @staticmethod
    def extract_text(recognition_result: List[Dict]) -> str:
        """提取纯文本内容"""
        return '\n'.join(item['text'] for item in recognition_result)
    
    def recognize_to_json(self, image_path: str, output_path: Optional[str] = None) -> Dict:
        """识别单张图片并输出JSON
        Args:
            image_path: 图片路径
            output_path: JSON输出路径，可选
        Returns:
            识别结果字典
        """
        result = self.recognize_image(image_path)
        text_content = self.extract_text(result)
        
        json_result = {"第1页": text_content}
        
        if output_path:
            self.save_json(json_result, output_path)  # 修改为使用公共方法
        
        return json_result
    
    def batch_recognize_to_json(self, image_dir: str, output_path: str) -> Dict:
        """批量识别图片并输出JSON"""
        import time
        start_time = time.time()
        
        if not os.path.exists(image_dir):
            raise FileNotFoundError(f"目录不存在: {image_dir}")
        
        results = {}
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp')
        
        # 获取所有支持格式的图片文件
        # 修改文件获取方式，按文件名排序
        image_files = sorted([
            f for f in os.listdir(image_dir) 
            if f.lower().endswith(supported_formats)
        ], key=lambda x: int(x.split('_')[1].split('.')[0]))  # 按page_x.png中的x数字排序
        
        total_images = len(image_files)
        print(f"\n找到 {total_images} 个图片文件待处理")
        
        for i, file in enumerate(image_files, 1):
            image_path = os.path.join(image_dir, file)
            print(f"\n[{i}/{total_images}] 开始处理: {file}")
            
            try:
                result = self.recognize_image(image_path)
                text_content = self.extract_text(result)
                results[f"第{i}页"] = text_content
                
                # 显示进度
                progress = i / total_images * 100
                print(f"\r当前进度: {progress:.1f}% ({i}/{total_images}张)", end="")
                
            except Exception as e:
                print(f"\n处理图片 {image_path} 时出错: {str(e)}")
                results[f"第{i}页"] = f"识别失败: {str(e)}"
        
        # 计算总耗时
        total_time = time.time() - start_time
        print(f"\n转换完成！总耗时: {total_time:.2f}秒")
        self.save_json(results, output_path)  # 修改为使用公共方法
        return results
    @staticmethod
    def save_json(data: Dict, output_path: str) -> None:
        """保存JSON文件
        Args:
            data: 要保存的数据字典
            output_path: JSON文件保存路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    """使用示例"""
    start_time = time.time()
    
    # 创建OCR服务实例
    ocr_service = PaddleOCRService()
    
    # 单图片识别示例
    # image_path = r"src\input\image\父与子.jpg"
    # output_path = r"src\output\recognition_result.json"
    # result = ocr_service.recognize_to_json(image_path, output_path)
    # print("单图识别结果已保存到:", output_path)
    # print("识别内容:", json.dumps(result, ensure_ascii=False, indent=2))
    
    # 批量识别示例
    book_name = "《贪心的小妖怪捉鲸鱼：声音的传播》"
    image_dir = os.path.join("src", "input", "PDFs", book_name)
    batch_output_path = os.path.join("src", "output", f"{book_name}.json")
    batch_result = ocr_service.batch_recognize_to_json(image_dir, batch_output_path)
    print("\n批量识别结果已保存到:", batch_output_path)
    print("识别内容:", json.dumps(batch_result, ensure_ascii=False, indent=2))
    
    # 计算总耗时
    total_time = time.time() - start_time
    print(f"\n所有处理完成！总耗时: {total_time:.2f}秒")

if __name__ == '__main__':
    # uv run src\ocr\paddle_ocr_service.py
    main()


