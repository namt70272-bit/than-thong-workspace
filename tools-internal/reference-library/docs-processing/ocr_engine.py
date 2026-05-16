import pytesseract
from PIL import Image
import os
import sys

def perform_ocr(image_path, lang='vie+eng'):
    try:
        if not os.path.exists(image_path):
            return f"Lỗi: Không tìm thấy file ảnh tại {image_path}"
        
        # Mở ảnh và nhận diện văn bản
        text = pytesseract.image_to_string(Image.open(image_path), lang=lang)
        return text
    except Exception as e:
        return f"Lỗi khi thực hiện OCR: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
        result = perform_ocr(img_path)
        print("--- KẾT QUẢ OCR ---")
        print(result)
    else:
        print("Sử dụng: python ocr_engine.py <path_to_image>")
