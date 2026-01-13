import time


class MessageListener:
    def __init__(self, chat_window):
        self.chat_window = chat_window
        self.last_message = None

    def get_latest_message(self):
        messages = self.chat_window.descendants(control_type="Text")
        if not messages:
            return None

        latest = messages[-1].window_text()
        return latest

    def wait_for_new_message(self, interval=1.5):
        while True:
            msg = self.get_latest_message()
            if msg and msg != self.last_message:
                self.last_message = msg
                return msg
            time.sleep(interval)
