import mss
import numpy as np
from PIL import Image
import pyautogui
import torch
import keyboard
import time
from bezier_mouse import move_mouse_bezier


# 加载模型（路径替换成你的模型）
model = torch.hub.load('ultralytics/yolov5', 'custom',
                       path='/yolo/winvalorant.pt',
                       force_reload=True, trust_repo=True)

# 定义监控区域（根据游戏窗口设置）
monitor = {
    "top": 0,
    "left": 0,
    "width": 1920,
    "height": 1080
}

shooting_enabled = False  # 自动开火开关状态

def toggle_shooting():
    global shooting_enabled
    shooting_enabled = not shooting_enabled
    print("自动开火：", "✅ 开启" if shooting_enabled else "❌ 关闭")

# 设置热键：空格键切换自动开火状态
keyboard.add_hotkey('shift', toggle_shooting)
print("🚀 脚本已启动，按空格切换自动开火，按 ESC 退出。")

try:
    with mss.mss() as sct:
        while True:
            if keyboard.is_pressed('esc'):
                print("🛑 用户按下 ESC，退出脚本。")
                break

            # 抓取屏幕
            img = np.array(sct.grab(monitor))
            img = Image.fromarray(img)

            # YOLOv5 检测
            results = model(img)
            boxes = results.xyxy[0]

            # 如果启用了自动开火
            if shooting_enabled:
                for box in boxes:
                    conf = box[4]
                    if conf < 0.5:
                        continue  # 忽略低置信度目标

                    x1, y1, x2, y2 = map(int, box[:4])
                    cx = (x1 + x2) // 2 + monitor["left"]
                    cy = (y1 + y2) // 2 + monitor["top"]

                    # 替代 pyautogui.moveTo(cx, cy)
                    move_mouse_bezier(cx, cy, duration=0.5)
                    pyautogui.click()
                    print(f"🎯 点击目标 at ({cx}, {cy})")

            time.sleep(0.1)  # 降低 CPU 占用

except Exception as e:
    print("发生异常：", e)
