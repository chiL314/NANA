from wechat.wechat_app import WeChatController
from llm.client import LLMClient
from memory.memory_manager import MemoryManager
import config
import time
import threading
from pynput import keyboard as pynput_keyboard
import keyboard


def main():
    print("AI女友启动...")

    # 步骤1：等待按空格开始校准（这个没问题，保留）
    print("\n[*] 请确保微信聊天窗口已打开并就位。按下空格键开始校准...") 
    def on_space_press(key):
        if key == pynput_keyboard.Key.space:
            return False  # 停止监听
    with pynput_keyboard.Listener(on_press=on_space_press) as listener:
        listener.join()

    wechat = WeChatController(config.TARGET_NAME)
    llm = LLMClient()
    memory = MemoryManager()  # 使用长期记忆系统

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

    # 消息计数器（用于动态记忆注入）
    message_count = 0

    try:
        while running:
            new_msg = wechat.fetch_new_message()

            if new_msg:
                # 防止抓到自己刚发的内容
                history = memory.get_context_for_llm()
                if history and new_msg in history[-1].get('content', ''):
                    continue

                print(f"📩 发现新消息: {new_msg}")
                memory.add_conversation("user", new_msg)

                print("💭 六花思考中...")
                
                # 动态记忆注入：每 3 条消息才注入一次记忆摘要
                message_count += 1
                if message_count % 3 == 0:
                    memory_summary = memory.get_memory_summary()
                    if memory_summary:
                        print(f"  [记忆] {memory_summary}")
                else:
                    memory_summary = ""
                
                reply = llm.get_reply(memory.get_context_for_llm(), memory_summary)

                if reply:
                    wechat.send_reply(reply)
                    print(f"💖 六花回复: {reply}")
                    memory.add_conversation("assistant", reply)

            time.sleep(0.5)

    except Exception as e:
        print(f"\n[!] 程序异常: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 保存记忆到磁盘
        print("\n[*] 正在保存记忆...")
        memory.save_to_disk()
        
        # 确保鼠标键盘恢复正常
        print("六花下线啦~ 再见！程序已安全退出。")
        time.sleep(0.5)

if __name__ == "__main__":
    main()