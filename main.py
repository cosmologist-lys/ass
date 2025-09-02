import time
import os
from pathlib import Path
import pyautogui
from ewmh import EWMH

# ==============================================================================
# --- 配置区 ---
# ==============================================================================
TARGET_WINDOW_TITLE = "首页 - 知乎 - Google Chrome"
SAVE_DIRECTORY = "/home/ptk/top"
CYCLE_INTERVAL_SEC = 10

# (find_target_window 函数保持不变)
def find_target_window(ewmh, title_keyword):
    target_window = None
    max_area = 0
    all_windows = ewmh.getClientList()
    for win in all_windows:
        try:
            win_name = ewmh.getWmName(win).decode('utf-8', 'ignore')
            if title_keyword.lower() in win_name.lower():
                geom = win.get_geometry()
                area = geom.width * geom.height
                if area > max_area:
                    max_area = area
                    target_window = win
        except (UnicodeDecodeError, TypeError):
            continue
    return target_window

def main():
    save_path = Path(SAVE_DIRECTORY).expanduser()
    save_path.mkdir(parents=True, exist_ok=True)
    ewmh = EWMH()
    print("自动化脚本已启动...")
    print(f"配置：每 {CYCLE_INTERVAL_SEC}s 刷新一次 '{TARGET_WINDOW_TITLE}' 窗口。")
    print("[!] 请注意：请将Chrome浏览器最大化放置在主屏幕上以保证截图正确。")

    while True:
        try:
            print("\n--- 开始新周期 ---")
            print(f"正在查找 '{TARGET_WINDOW_TITLE}' 窗口...")
            target_window = find_target_window(ewmh, TARGET_WINDOW_TITLE)

            if not target_window:
                print(f"警告：未找到匹配窗口。将在 {CYCLE_INTERVAL_SEC}s 后重试。")
                time.sleep(CYCLE_INTERVAL_SEC)
                continue

            win_name = ewmh.getWmName(target_window).decode('utf-8', 'ignore')
            print(f"成功找到窗口: '{win_name}'")

            # --- 步骤 1: 激活、点击并刷新 ---
            ewmh.setActiveWindow(target_window)
            ewmh.display.flush()
            time.sleep(0.5)

            # 【新代码】在窗口中心点击一次以确保获取输入焦点
            geom = target_window.get_geometry()
            center_x = geom.x + geom.width / 2
            center_y = geom.y + geom.height / 2
            pyautogui.click(center_x, center_y)
            print("  [+] 已模拟鼠标点击以确保焦点。")
            time.sleep(0.2)

            pyautogui.hotkey('ctrl', 'r')
            print(f"  [+] 已发送刷新命令。当前时间: {time.strftime('%H:%M:%S')}")

            # --- 步骤 2: 等待1分钟 ---
            print("等待 10s 后进行截图...")
            time.sleep(10)

            # --- 步骤 3: 截取整个主屏幕 ---
            print("正在截取主屏幕...")
            # 【新代码】不再计算区域，直接截取主屏幕
            # screenshot = pyautogui.screenshot()
            primary_screen_size = pyautogui.size()
            print(f"  [+] 主屏幕尺寸: {primary_screen_size.width}x{primary_screen_size.height}")
            
            # 【新代码】根据主屏幕尺寸，只截取该区域
            screenshot = pyautogui.screenshot(region=(0, 0, 1920, primary_screen_size.height))
            
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = save_path / f"capture-{timestamp}.png"
            screenshot.save(filename)
            print(f"截图成功！已保存至: {filename}")
            
            # --- 步骤 4: 等待剩余时间 ---
            remaining_wait_seconds = (CYCLE_INTERVAL_SEC)
            if remaining_wait_seconds > 0:
                print(f"等待 {remaining_wait_seconds / 60:.1f} 分钟进入下一个周期...")
                time.sleep(remaining_wait_seconds)

        except Exception as e:
            print(f"\n发生了一个意外错误: {e}")
            print("将在 60 秒后尝试恢复...")
            time.sleep(60)

if __name__ == "__main__":
    main()