# -*- coding: utf-8 -*-
import os
import time
import subprocess
import pyautogui

# 配置 3ds Max 可执行文件路径（请修改为你的 3ds Max 路径）
MAX_EXECUTABLE = r"C:\Program Files\Autodesk\3ds Max 2022\3dsmax.exe"

# 要遍历的 .max 文件所在的文件夹路径（请修改为你的路径）
FOLDER_PATH = r"D:\3dsmax_files"

# 截图保存路径
SCREENSHOT_FOLDER = os.path.join(os.getcwd(), "Screenshots")
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)

def find_max_files(directory):
    """获取指定目录下的所有 .max 文件路径"""
    max_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".max"):
                max_files.append(os.path.join(root, file))
    return max_files

def open_max_file(file_path):
    """使用 3ds Max 打开 .max 文件"""
    process = subprocess.Popen([MAX_EXECUTABLE, file_path], shell=True)
    return process

def capture_screenshot(file_name):
    """截图并保存"""
    screenshot_path = os.path.join(SCREENSHOT_FOLDER, f"{file_name}.png")
    time.sleep(5)  # 等待 5 秒，确保窗口完全打开
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"截图已保存: {screenshot_path}")

def main():
    max_files = find_max_files(FOLDER_PATH)
    
    if not max_files:
        print("未找到任何 .max 文件")
        return
    index = 0
    count=len(max_files)
    for file in max_files:
        index=index+1
        print(f"打开文件{index}/{count}: {file}")
        process = open_max_file(file)
        time.sleep(30)  # 给予足够时间加载文件
        
        # 截图（文件名去掉路径和后缀）
        file_name = os.path.splitext(os.path.basename(file))[0]
        capture_screenshot(file_name)

        # 关闭 3ds Max
        print("关闭 3ds Max")
        # process.terminate()  # 直接关闭进程
        os.system(f"taskkill /F /IM 3dsmax.exe /T")  # 强制关闭

    print("所有文件处理完成！")

if __name__ == "__main__":
    main()
