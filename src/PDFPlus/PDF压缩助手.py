# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : PDF压缩助手.py
# Time       ：2025/5/10 20:59
# version    ：python 3.12
# Description：PDF压缩助手
将PDF中的图片进行压缩处理
"""
import pymupdf
import io
from PIL import Image
import os
from pathlib import Path

'''
压缩函数参数说明：
    source_file_path: 输入PDF文件路径
    save_file_path: 输出PDF文件路径
    quality: 图片压缩质量(1-100), 数值越小压缩率越高
    zoom_x: 水平缩放因子
    zoom_y: 垂直缩放因子
    grayscale: 是否转为灰度图
    use_jpg: 是否使用JPG格式(若为False则使用PNG格式)
    garbage:清理 PDF 中的无效对象（如删除未引用的资源），合并重复内容，并深度重组文档结构。数值越大，清理力度越强（PyMuPDF 中通常有效范围是 1-4）。

'''
# PDF压缩函数（通过对PDF中的图片进行压缩，来实现PDF整体大小的压缩）
def pdf_images_compress(source_file_path, save_file_path, quality=50, zoom_x=0.5, zoom_y=0.5, grayscale=False,use_jpg=True,garbage=4) :
    try:
        # Step1:确保保存的目录存在（若不存在，则创建）

        # 先从保存路径中提取目录部分
        save_dir = os.path.dirname(save_file_path)
        # 目录若不存在，则直接创建
        # parents=True 表示自动创建父目录（若不存在）
        # exist_ok=True 表示若目录已经存在，则不提醒异常
        Path(save_dir).mkdir(parents=True, exist_ok=True)

        # Step2:打开PDF文档
        doc = pymupdf.open(source_file_path)
        page_index=0
        # Step3:遍历PDF文件的每一页
        for page in doc:
            # 获取当前PDF页面中的图片信息
            img_list = page.get_images(full=True)
            # print(f'当前页面中共有{len(img_list)}张图片')

            # Step4:对每页中每一张的图片进行压缩处理
            for index,img in enumerate(img_list):
                # 定义一个计数变量，用于表示当前在处理第几张图片，由于索引index是从0开始，所以用index+1
                pointer=index+1

                xref = img[0]
                # 提取图片信息
                source_image = doc.extract_image(xref)
                # print(f'获取到的原始图片信息为：{source_image}')

                img_ext = source_image["ext"]        # 获取图片的格式后缀
                img_bytes = source_image["image"]
                # img_filter = img[7]  # 获取图片的Filter属性
                img_filter = img[8]  # 获取图片的Filter属性

                # 关键步骤：用于获取原图片在PDF中的区域坐标信息，主要用于保证压缩后，图片的位置和尺寸不变
                # 提取图片在页面中的坐标区域（rect）
                img_rects = list(page.get_image_rects(xref))  # 转换为列表
                if not img_rects:
                    print("发生异常信息，未找到图片的位置信息")
                    return
                img_rect = img_rects[0]  # 取第一个位置（可能存在多个区域引用同一图片）
                # print(f'当前处理的图片的Filter为：{img_filter}')
                # 检查图片是否为FlateDecode类型，如果为FlateDecode类型，则需要进行特殊处理
                is_flate_decode = img_filter == "FlateDecode"
                # 使用PIL打开图片
                try:
                    img = Image.open(io.BytesIO(img_bytes))

                    # 按照指定的缩放因子进行缩放图片
                    new_width = int(img.width * zoom_x)
                    new_height = int(img.height * zoom_y)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    # 转为灰度图
                    if grayscale:
                        img = img.convert("L")

                    # 压缩图片
                    img_byte_arr = io.BytesIO()

                    # 处理FlateDecode类型的图片
                    if is_flate_decode:
                        # 检查是否有透明通道
                        has_transparency = False
                        if img.mode == "RGBA":
                            has_transparency = True

                        # 对于有透明通道的图片，使用PNG格式
                        if has_transparency and not use_jpg:
                            img.save(img_byte_arr, format='PNG', compress_level=9)
                        else:
                            # 对于没有透明通道的图片，优先使用JPEG
                            if img.mode in ("RGBA", "P"):
                                img = img.convert("RGB")
                            img.save(img_byte_arr, format='JPEG', quality=quality, optimize=True)
                    else:
                        # 处理非FlateDecode类型的图片
                        if use_jpg and img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")

                        if use_jpg:
                            img.save(img_byte_arr, format='JPEG', quality=quality, optimize=True)
                        else:
                            img.save(img_byte_arr, format='PNG', compress_level=9)

                    img_byte_arr.seek(0)
                    new_img_bytes = img_byte_arr.read()
                    page.delete_image(xref)  # 删除原图片
                    page.insert_image(img_rect, stream=new_img_bytes)  # 按照原图片的区域位置插入新图片
                    # 打印处理信息
                    original_size = len(img_bytes)
                    new_size = len(new_img_bytes)
                    reduction = (1 - new_size / original_size) * 100
                    print(
                        f"第{page_index + 1}页第{pointer}个图片 ({img_filter}) 已压缩: {original_size / 1024:.2f}KB -> {new_size / 1024:.2f}KB ({reduction:.2f}%)")
                except Exception as e:
                    print(f"处理第{page_index + 1}页第{pointer}个图片时出错: {str(e)}")
                    continue
            page_index+=1
        # # 保存压缩后的PDF
        doc.save(save_file_path, garbage=garbage, deflate=True)
        doc.close()
    except PermissionError:
        print(f"无权限创建目录：{save_dir}")
    except FileExistsError:
        print(f"路径已被文件占用：{save_dir}")

# 程序主入口
if __name__ == "__main__":
    # uv run src/PDFPlus/PDF压缩助手.py
    # 示例使用
    input_pdf = r"E:\Lei\Downloads\新建文件夹\仇保兴-（部分）自主更新.pdf"
    output_pdf = r"E:\Lei\Downloads\新建文件夹\仇保兴-（部分）自主更新_压缩.pdf"

    print(f"开始压缩PDF: {input_pdf}")
    pdf_images_compress(
        input_pdf,
        output_pdf,
        # quality=15,  # 低质量以获得更高压缩率
        # zoom_x=0.6,  # 水平缩小到60%
        # zoom_y=0.6,  # 垂直缩小到60%

        quality=50,  # 低质量以获得更高压缩率
        zoom_x=1,  # 水平缩小(0-1)
        zoom_y=1,  # 垂直缩小(0-1)

        # grayscale=True,  # 转为灰度图
        grayscale=False,  # 转为灰度图
        # use_jpg=True  # 使用JPG格式
        use_jpg=False  # 使用JPG格式
    )
    print(f"压缩完成，已保存至: {output_pdf}")
