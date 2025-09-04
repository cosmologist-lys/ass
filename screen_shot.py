# screen_shot.py

import time
from pathlib import Path
import pyautogui
from PIL import Image, ImageDraw, ImageFont

# ==============================================================================
# --- 截图与水印配置 ---
# ==============================================================================
# --- 新增：平铺水印配置 ---
# 字体文件的绝对路径 (必须是支持中文的字体)
#FONT_PATH = "/usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc"
FONT_PATH = "/usr/share/fonts/adobe-source-han-sans/SourceHanSansCN-Bold.otf"
FONT_SIZE = 30                              # 水印文字大小
WATERMARK_TEXT_STATIC = "QWCSSC  刘雨松 "     # 水印中的静态文字
WATERMARK_ANGLE = 30                        # 水印旋转角度 (逆时针)
WATERMARK_OPACITY = 25                      # 水印不透明度 (0-255之间, 数值越小越透明)
WATERMARK_SPACING_X = 400                   # 水印在横向上的间距
WATERMARK_SPACING_Y = 300  
SAVE_DIRECTORY = "/home/ptk/top"

def add_watermark(image):
    """在给定的 Pillow 图片对象上添加平铺、旋转、半透明的水印"""
    current_date = time.strftime("%Y-%m-%d")
    full_text = f"{WATERMARK_TEXT_STATIC} {current_date}"
    
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        print(f"  [!] 错误：字体文件未找到: {FONT_PATH}。水印功能已跳过。")
        return image

    text_bbox = font.getbbox(full_text)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    stamp = Image.new('RGBA', (text_width, text_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(stamp)
    text_color = (255, 255, 255, WATERMARK_OPACITY)
    draw.text((-text_bbox[0], -text_bbox[1]), full_text, font=font, fill=text_color)

    rotated_stamp = stamp.rotate(WATERMARK_ANGLE, expand=True, resample=Image.Resampling.BICUBIC)

    img_width, img_height = image.size
    stamp_width, stamp_height = rotated_stamp.size
    
    watermarked_image = image.convert("RGBA")

    for x in range(0, img_width, stamp_width + WATERMARK_SPACING_X):
        for y in range(0, img_height, stamp_height + WATERMARK_SPACING_Y):
            watermarked_image.paste(rotated_stamp, (x, y), rotated_stamp)

    return watermarked_image.convert("RGB")

def capture_and_save():
    """
    执行“截图-加水印-保存”的核心功能函数
    """
    print("  [+] 正在截取主屏幕...")
    try:
        primary_screen_size = pyautogui.size()
        screenshot = pyautogui.screenshot(region=(0, 0, 1920, primary_screen_size.height))
        
        print("  [+] 正在添加平铺水印...")
        screenshot_with_watermark = add_watermark(screenshot)
        
        save_path = Path(SAVE_DIRECTORY).expanduser()
        save_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = save_path / f"f-{timestamp}.png"
        
        screenshot_with_watermark.save(filename)
        print(f"  [+] 截图成功！已保存至: {filename}")
    except Exception as e:
        print(f"  [!] 截图或保存过程中发生错误: {e}")

# 这段代码使得本文件也可以被单独运行以测试截图功能
if __name__ == '__main__':
    print("正在以独立模式测试截图功能...")
    capture_and_save()
    print("测试完成。")