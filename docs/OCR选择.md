## OCR工具
### Umi-OCR
> OCR software, free and offline. 开源、免费的离线OCR软件。支持截屏/批量导入图片，PDF文档识别，排除水印/页眉页脚，扫描/生成二维码。内置多国语言库。
1. https://github.com/hiroi-sora/Umi-OCR
2. https://github.com/eaeful/WechatOCR_umi_plugin

### PaddleOCR-json
> OCR离线图片文字识别命令行windows程序，以JSON字符串形式输出结果，方便别的程序调用。提供各种语言API。由 PaddleOCR C++ 编译。
- https://github.com/hiroi-sora/PaddleOCR-json
- 可以考虑使用这个命令行库，来实现OCR功能。



## OCR库


以下是对主流免费开源Python OCR库的对比分析，重点从识别精度、速度和易用性三个维度进行比较：

### 1. PaddleOCR（百度飞桨）
**核心优势**：
- 中文识别效果最佳（官方中文预训练模型）
- 轻量模型速度极快（PP-OCRv4）
- 支持多语言混合识别
```python
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch")
result = ocr.ocr("image.jpg", cls=True)
```

### 2. EasyOCR
**核心优势**：
- 支持80+种语言
- 默认GPU加速（需CUDA环境）
- 复杂背景适应性较强
```python
import easyocr
reader = easyocr.Reader(["ch_sim","en"])
result = reader.readtext("image.jpg")
```

### 3. Tesseract
**核心优势**：
- 历史最久（1984年诞生）
- 本地运行无依赖
- 可高度自定义训练
```python
import pytesseract
text = pytesseract.image_to_string("image.jpg", lang="chi_sim")
```

### 对比总结表
| 特性               | PaddleOCR | EasyOCR | Tesseract |
|--------------------|-----------|---------|-----------|
| 中文识别精度       | ★★★★★    | ★★★★☆  | ★★☆☆☆    |
| 英文识别精度       | ★★★★☆    | ★★★★☆  | ★★★★★    |
| 识别速度（CPU）    | 150ms/页 | 800ms/页| 200ms/页  |
| 多语言支持         | 100+      | 80+     | 100+      |
| 安装便捷性         | 简单      | 中等    | 较复杂    |
| 版面分析能力       | 支持      | 不支持  | 有限支持  |

### 推荐方案
- **中文优先场景**：<mcsymbol name="PaddleOCR" filename="paddleocr.py" path="f:\Code\PythonBase\ocr_demo.py" startline="3" type="class"></mcsymbol> 首选
- **多语言混合场景**：<mcsymbol name="EasyOCR" filename="easyocr_demo.py" path="f:\Code\PythonBase\easyocr_demo.py" startline="2" type="function"></mcsymbol> 更优
- **嵌入式设备部署**：Tesseract+量化模型更适合

建议在实际环境中用测试图片对比：`f:\Code\PythonBase\test_images` 目录下放置不同类型样本（扫描件/照片/低分辨率图片）进行基准测试。