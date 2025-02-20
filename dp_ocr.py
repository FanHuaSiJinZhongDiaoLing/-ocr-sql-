from PIL import Image
import numpy as np
from rapidocr_onnxruntime import RapidOCR

def process_image(image_path):
    # 打开图片并获取尺寸
    img = Image.open(image_path)
    width, height = img.size

    # 初始化OCR引擎
    ocr_engine = RapidOCR()
    all_ocr_results = []

    # 图片分割处理（按高度2000像素分段）
    split_height = 2000
    for y_start in range(0, height, split_height):
        y_end = min(y_start + split_height, height)
        sub_img = img.crop((0, y_start, width, y_end))
        sub_img_np = np.array(sub_img)

        # 执行OCR识别
        result, _ = ocr_engine(sub_img_np)
        
        # 处理OCR结果并转换坐标
        for res in result:
            box = res[0]
            text = res[1]
            x_coords = [p[0] for p in box]
            y_coords = [p[1] for p in box]
            
            # 计算坐标并转换到原图位置
            x_left = min(x_coords)
            x_right = max(x_coords)
            y_top = y_start + min(y_coords)
            
            all_ocr_results.append({
                "text": text,
                "x_left": x_left,
                "x_right": x_right,
                "y_top": y_top
            })

    # 按垂直位置排序结果
    sorted_results = sorted(all_ocr_results, key=lambda x: x["y_top"])

    # 分组为文本行（20像素阈值）
    lines = []
    current_line = []
    line_threshold = 20
    
    if sorted_results:
        current_line.append(sorted_results[0])
        current_y = sorted_results[0]["y_top"]
        
        for res in sorted_results[1:]:
            if abs(res["y_top"] - current_y) <= line_threshold:
                current_line.append(res)
            else:
                lines.append(current_line)
                current_line = [res]
                current_y = res["y_top"]
        lines.append(current_line)

    # 生成原始文本文件
    with open("raw.txt", "w", encoding="utf-8") as f:
        for line in lines:
            texts = [res["text"] for res in sorted(line, key=lambda x: x["x_left"])]
            f.write(" ".join(texts) + "\n")

if __name__ == "__main__":
    process_image("image.png")  # 替换为你的图片路径