import pyautogui

class MessageSender:
    @staticmethod
    def send(message):
        try:
            pyautogui.typewrite(message)
            pyautogui.press("enter")
            return True
        except Exception as e:
            print("[发送失败]", e)
            return False
