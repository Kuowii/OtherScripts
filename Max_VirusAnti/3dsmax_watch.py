import time
import os
import pyautogui
import pywinauto
import pygetwindow as gw

# 监听文件路径
command_file = os.path.join(os.getcwd(), "maxscript_command.txt")
screenshot_dir = os.path.join(os.getcwd(), "Screenshots")
os.makedirs(screenshot_dir, exist_ok=True)

def get_3dsmax_window():
    """获取 3ds Max 主窗口"""
    windows = gw.getWindowsWithTitle("Autodesk 3ds Max")
    return windows[0] if windows else None

def capture_screen(filename):
    """截取整个屏幕"""
    img = pyautogui.screenshot()
    img.save(filename)
    print(f"截图已保存: {filename}")

def close_modal_windows():
    """检测并关闭 3ds Max 的模态弹窗"""
    for win in gw.getAllWindows():
        if win.title and "Autodesk 3ds Max" not in win.title:
            print(f"发现弹窗: {win.title}")
            capture_screen(os.path.join(screenshot_dir, f"{win.title}.png"))
            pyautogui.hotkey("enter")  # 模拟回车关闭对话框
            time.sleep(1)

def main():
    print(f"监听 3ds Max 事件中... {command_file}")
    last_command = ""

    while True:
        if os.path.exists(command_file):
            with open(command_file, "r") as f:
                command = f.read().strip()
            
            if command and command != last_command:
                last_command = command

                if command.startswith("OPEN:"):
                    print(f"正在打开文件: {command[5:]}")
                    time.sleep(5)  # 预留时间等待文件加载
                    filename = os.path.join(screenshot_dir, f"screenshot_{int(time.time())}.png")
                    capture_screen(filename)
                    time.sleep(2)
                    close_modal_windows()

                elif command == "CAPTURE":
                    filename = os.path.join(screenshot_dir, f"screenshot_{int(time.time())}.png")
                    capture_screen(filename)

                elif command == "CLOSE_DIALOGS":
                    close_modal_windows()

                elif command == "DONE":
                    print("所有文件处理完毕，退出监听...")
                    break

        time.sleep(1)


def close_max_dialogs():
    """持续检测 3ds Max 弹出的 MessageBox 并关闭"""
    maxWin = get_3dsmax_window()
    # 连接到 3ds Max 进程
    app = pywinauto.Application().connect(handle = maxWin._hWnd, timeout=5)
    print("Connect Success!")

    while True:
        try:
            # 获取所有窗口（包括隐藏的 MessageBox）
            all_windows = app.windows()
            for win in all_windows:
                title = win.window_text()                
                # 过滤掉主窗口，仅处理小型弹窗
                if title and "Autodesk 3ds Max" not in title:
                    print(f"检测到弹窗: {title}")
                    time.sleep(1)
                    filename = os.path.join(screenshot_dir, f"screenshot_{int(time.time())}.png")
                    capture_screen(filename)
                    try:
                        win.type_keys("{ENTER}")
                        # win.child_window(title="确定", control_type="Button").click()
                        print("已点击‘确定’按钮")
                    except:
                        # 如果没有“确定”按钮，尝试按 ESC 关闭
                        win.type_keys("{ESC}")
                        print("已按 ESC 关闭")


        except Exception as e:
            print(e);
            pass  # 忽略错误，继续循环

        time.sleep(1)  # 每秒检测一次

if __name__ == "__main__":
    # main()
    close_max_dialogs()
