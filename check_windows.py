# check_windows.py
# 这是一个诊断工具，用来查看当前所有窗口的信息

from ewmh import EWMH

def list_windows():
    """列出所有窗口的详细信息"""
    ewmh = EWMH()
    all_windows = ewmh.getClientList()
    
    print("--- 侦测到以下窗口 ---")
    print(f"{'窗口标题':<60} | {'位置 (x, y)':<18} | {'尺寸 (w, h)':<18} | {'面积':<10}")
    print("-" * 110)

    for win in all_windows:
        try:
            win_name = ewmh.getWmName(win).decode('utf-8', 'ignore')
            if not win_name:
                continue # 跳过没有标题的窗口
                
            geom = win.get_geometry()
            area = geom.width * geom.height
            
            # 格式化输出
            title_str = (win_name[:57] + '...') if len(win_name) > 60 else win_name
            pos_str = f"{geom.x}, {geom.y}"
            size_str = f"{geom.width}, {geom.height}"
            
            print(f"{title_str:<60} | {pos_str:<18} | {size_str:<18} | {area:<10}")

        except Exception:
            # 忽略一些特殊窗口导致的小错误
            continue

if __name__ == "__main__":
    list_windows()