import pyautogui
import time
import random
import math

def get_bezier_curve(p0, p1, p2, n=50):
    """生成二阶贝塞尔曲线上的 n 个点"""
    points = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        points.append((x, y))
    return points

def move_mouse_bezier(to_x, to_y, duration=0.4):
    """模拟人类风格的鼠标轨迹（贝塞尔+随机扰动）"""
    from_x, from_y = pyautogui.position()

    # 计算控制点：加一些随机偏移，使轨迹不死板
    cp_x = from_x + (to_x - from_x) / 2 + random.randint(-100, 100)
    cp_y = from_y + (to_y - from_y) / 2 + random.randint(-100, 100)

    bezier_points = get_bezier_curve(
        (from_x, from_y),
        (cp_x, cp_y),
        (to_x, to_y),
        n=int(duration * 100)
    )

    for point in bezier_points:
        # 小扰动模拟“人手不稳”
        x, y = point
        jitter_x = random.uniform(-1.5, 1.5)
        jitter_y = random.uniform(-1.5, 1.5)
        pyautogui.moveTo(x + jitter_x, y + jitter_y)
        time.sleep(duration / len(bezier_points))

    # 最后精准对齐
    pyautogui.moveTo(to_x, to_y)

