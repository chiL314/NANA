from PIL import ImageGrab
import pytesseract

# 设置 tesseract.exe 路径
pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"

def get_latest_message(region):
    """
    region: (left, top, right, bottom) 截图区域
    """
    img = ImageGrab.grab(bbox=region)
    text = pytesseract.image_to_string(img, lang="chi_sim")
    return text.strip()

def clean_message(msg: str) -> str:
    """
    去掉时间戳、昵称、多余换行，只保留文字
    """
    lines = msg.splitlines()
    clean_lines = [line.strip() for line in lines if line.strip() and not line.strip().isdigit()]
    return " ".join(clean_lines)
