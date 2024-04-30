import cv2
import easyocr

def demo():
# 读取图像
    img = cv2.imread('images/original.png')
    # 创建 EasyOCR 对象，并指定要识别的语言
    reader = easyocr.Reader(['ch_sim', 'en']) # 'en'
    # 使用 EasyOCR 进行 OCR
    result = reader.readtext(img)
    # 打印识别结果
    for detection in result:
        print(detection[1])

if __name__ == "__main__":
    demo()