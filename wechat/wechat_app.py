import time
import pyperclip
import pyautogui
import pygetwindow as gw
from pynput import mouse

class WeChatController:
    def __init__(self, target_name):
        self.target_name = target_name
        self.last_msg = ""
        self.chat_pos = None
        self.input_pos = None

    def calibrate(self):
        print("\n=== 准备校准 (双击模式) ===")
        print("[步骤 1] 请点击【最后一条消息的气泡中心】")
        with mouse.Listener(on_click=self._on_click_chat) as listener:
            listener.join()
        print(f"   已记录气泡坐标: {self.chat_pos}")

        print("[步骤 2] 请点击【输入框中心】")
        with mouse.Listener(on_click=self._on_click_input) as listener:
            listener.join()
        print(f"   已记录输入框坐标: {self.input_pos}")

    def _on_click_chat(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            self.chat_pos = (x, y)
            return False

    def _on_click_input(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            self.input_pos = (x, y)
            return False

    def fetch_new_message(self):
        try:
            # 1. 强制激活微信
            wins = gw.getWindowsWithTitle('微信')
            if wins and not wins[0].isActive:
                wins[0].activate()

            # 2. 执行双击：微信会自动弹出全选框
            pyautogui.click(self.chat_pos[0], self.chat_pos[1], clicks=2, interval=0.1)
            time.sleep(0.2)

            # 3. 复制全文（双击后文字已全选）
            pyperclip.copy("EMPTY")
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.3)

            # 4. 【关键】点击一下输入框：这有两个作用：
            #    a. 取消掉微信消息全选的那个高亮状态
            #    b. 让焦点回到输入框，准备回复
            pyautogui.click(self.input_pos[0], self.input_pos[1])

            raw_text = pyperclip.paste().strip()

            if not raw_text or raw_text == "EMPTY":
                return None

            # 5. 简单的过滤逻辑
            # 由于双击抓取的是单条消息全文，不再需要复杂的行解析
            if raw_text != self.last_msg and raw_text != self.target_name:
                self.last_msg = raw_text
                return raw_text

            return None
        except Exception as e:
            print(f"[!] 抓取消息时出错: {e}")
            return None

    def send_reply(self, text):
        try:
            # 直接粘贴并发送（fetch里已经点过输入框了，这里更安全）
            pyautogui.click(self.input_pos[0], self.input_pos[1])
            pyperclip.copy(text)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            pyautogui.press('enter')
            self.last_msg = text
        except Exception as e:
            print(f"[!] 发送回复时出错: {e}")