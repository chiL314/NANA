# wechat/target.py
import pygetwindow as gw

class WeChatTarget:
    def __init__(self, window_name):
        self.window_name = window_name

    def get_window_rect(self):
        """获取微信窗口的坐标"""
        try:
            windows = gw.getWindowsWithTitle(self.window_name)
            if windows:
                win = windows[0]
                # 如果窗口最小化了，还原它
                if win.isMinimized:
                    win.restore()
                # 激活窗口到最前
                try:
                    win.activate()
                except:
                    pass
                return (win.left, win.top, win.width, win.height)
            else:
                return None
        except Exception as e:
            print(f"Window search error: {e}")
            return None
    
    def get_chat_area_region(self, win_rect):
        """
        根据窗口坐标，估算聊天记录区域。
        这里的比例可能需要根据你的微信版本和分辨率微调。
        假设：
        x, y, w, h 是窗口属性
        聊天内容区大概在窗口的中下部，输入框之上。
        """
        x, y, w, h = win_rect
        # 这是一个经验估算值，截取窗口底部向上约200像素，避开输入框
        # 你可能需要截图调试这里
        roi_x = x + int(w * 0.1) # 左边留点边距
        roi_w = int(w * 0.8)     # 宽度
        roi_h = 150              # 高度：只看最近的几行
        # 假设输入框高度约为 150px，所以从底部减去 200px 开始截取
        roi_y = y + h - 200 - roi_h 
        
        return (roi_x, roi_y, roi_w, roi_h)

    def get_input_box_point(self, win_rect):
        """获取输入框的点击坐标"""
        x, y, w, h = win_rect
        # 点击窗口底部偏上的位置
        return (x + w // 2, y + h - 80)