from wechat.wechat_app import WeChatController
from llm.client import LLMClient
from conversation.state import ConversationState
import config
import time
import threading
from pynput import keyboard as pynput_keyboard
import keyboard


def main():
    print("小鸟游六花 AI女友启动...")

    # 步骤1：等待按空格开始校准（这个没问题，保留）
    print("\n[*] 请确保微信聊天窗口已打开并就位。按下空格键开始校准...")
    def on_space_press(key):
        if key == pynput_keyboard.Key.space:
            return False  # 停止监听
    with pynput_keyboard.Listener(on_press=on_space_press) as listener:
        listener.join()

    wechat = WeChatController(config.TARGET_NAME)
    llm = LLMClient()
    state = ConversationState()

    # 校准
    wechat.calibrate()
    print("[*] 校准完成，进入自动监控状态...")
    print("[*] 退出方式：随时按下 Ctrl + Shift + Q 即可安全退出程序")

    # 步骤2：设置全局退出标志
    running = True

    def wait_for_exit_hotkey():
        nonlocal running
        print("[*] 全局热键监听已启动（Ctrl + Shift + Q 退出）")
        keyboard.wait('ctrl + shift + q')  # 阻塞等待，直到按下热键
        print("\n[*] 检测到退出热键！正在安全关闭程序...")
        running = False

    # 启动独立线程监听退出热键（不会被pyautogui干扰）
    exit_thread = threading.Thread(target=wait_for_exit_hotkey, daemon=True)
    exit_thread.start()

    try:
        while running:
            new_msg = wechat.fetch_new_message()

            if new_msg:
                # 防止抓到自己刚发的内容
                if state.history and new_msg in state.history[-1]['content']:
                    continue

                print(f"📩 发现新消息: {new_msg}")
                state.add_message("user", new_msg)

                print("💭 六花思考中...")
                reply = llm.get_reply(state.get_context())

                if reply:
                    wechat.send_reply(reply)
                    print(f"💖 六花回复: {reply}")
                    state.add_message("assistant", reply)

            time.sleep(0.5)

    except Exception as e:
        print(f"\n[!] 程序异常: {e}")
    finally:
        # 确保鼠标键盘恢复正常
        print("\n六花下线啦~ 再见！程序已安全退出。")
        # 可选：加个短暂延迟让系统恢复焦点
        time.sleep(0.5)

if __name__ == "__main__":
    main()