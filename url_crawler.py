# url_crawler.py

import time
import pyautogui
from ewmh import EWMH

# 从我们自己的 screen_shot.py 文件中导入核心功能函数
import screen_shot 

# ==============================================================================
# --- 流程控制配置 ---
# ==============================================================================
# 需要巡检的 URL 列表
URL_LIST = [
    "https://mgr.qwgas.com/#/login",
    "http://www.qwgas.cn/"
]

# 两个URL之间的间隔时间（秒）
N_SECONDS = 30

# 导航到URL后，等待页面加载的时间（秒）
M_SECONDS = 10

# 一整轮完整巡检的周期时间（秒）
# 注意：Z_SECONDS 必须大于 (N_SECONDS + M_SECONDS) * URL数量
Z_SECONDS = 600 # 

# 目标浏览器窗口的标题关键字
TARGET_BROWSER_TITLE = "Brave"


def find_target_window(ewmh, title_keyword):
    """查找标题包含关键字的、面积最大的窗口"""
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
    """主函数，负责循环和浏览器控制"""
    ewmh = EWMH()
    print("自动化URL巡检脚本已启动...")
    print(f"将巡检 {len(URL_LIST)} 个URL，完整周期为 {Z_SECONDS} 秒。")
    print("[!] 请注意：请将Chrome浏览器最大化放置在主屏幕上。")

    JOB_COUNT = 0

    while True:
        cycle_start_time = time.time()
        print(f"\n--- {time.strftime('%Y-%m-%d %H:%M:%S')} | 开始新一轮巡检,当前循环次数 {JOB_COUNT} ---")

        for i, url in enumerate(URL_LIST):
            print(f"\n[任务 {i+1}/{len(URL_LIST)}] 正在处理 URL: {url}")
            try:
                target_window = find_target_window(ewmh, TARGET_BROWSER_TITLE)

                if not target_window:
                    print("  [!] 警告：未找到浏览器窗口，跳过此URL。")
                    continue
                
                # 睡5s,让我有时间把鼠标聚焦到brave上
                time.sleep(5)
                
                # 1. 激活并导航
                ewmh.setActiveWindow(target_window)
                ewmh.display.flush()
                time.sleep(0.5)
                pyautogui.hotkey('ctrl', 'l') # 聚焦地址栏
                time.sleep(0.5)
                pyautogui.typewrite(url, interval=0.01) # 输入URL
                pyautogui.press('enter') # 确认导航
                print(f"  [+] 已导航至目标URL。")

                # 2. 等待页面加载 (m秒)
                print(f"  [+] 等待 {M_SECONDS} 秒让页面加载...")
                time.sleep(M_SECONDS)

                # 3. 调用截图模块执行截图
                screen_shot.capture_and_save()

                # 4. 等待URL之间的间隔 (n秒)
                if i < len(URL_LIST) - 1: # 如果不是最后一个URL
                    print(f"  [+] 等待 {N_SECONDS} 秒进入下一个URL...")
                    time.sleep(N_SECONDS)

            except Exception as e:
                print(f"  [!] 处理URL {url} 时发生意外错误: {e}")

        JOB_COUNT += 1
        
        # 5. 计算并等待至完整周期 (z秒)
        cycle_end_time = time.time()
        elapsed_time = cycle_end_time - cycle_start_time
        wait_duration = Z_SECONDS - elapsed_time
        
        print(f"\n--- 本轮巡检耗时 {elapsed_time:.2f} 秒 ---")
        if wait_duration > 0:
            print(f"等待 {wait_duration:.2f} 秒后开始下一轮...")
            time.sleep(wait_duration)

if __name__ == '__main__':
    main()