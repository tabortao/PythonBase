
https://paddlepaddle.github.io/PaddleOCR/latest/quick_start.html

```bash
uv init OCRPlus --python 3.10
cd OCRPlus
uv venv
.venv\Scripts\activate
# 安装PaddlePaddle，CPU端安装
uv pip install paddlepaddle==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
# 安装paddleocr
uv add paddleocr --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```