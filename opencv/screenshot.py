# pip install pyautogui Pillow
import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import pygetwindow as gw


def screenshot_window(x1, y1, x2, y2):
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    screenshot.show()  # 显示截图
    # screenshot.save("screenshot.png")  # 保存截图到文件

def screenshot_cv(x1, y1, x2, y2):
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    # 将截图转换为 OpenCV 格式
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    # 显示截图
    cv2.imshow('Screenshot', screenshot_cv)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def mouseMove():
    # 获取当前屏幕的宽度和高度
    screen_width, screen_height = pyautogui.size()
    # 将鼠标移动到屏幕中心位置
    pyautogui.moveTo(screen_width / 2, screen_height / 2, duration=0.5)
    # 模拟鼠标左键点击
    pyautogui.click()
    # 模拟键盘按下 'a' 键
    pyautogui.press('a')

def screenshot_cv_template():
    # 读取原始图像和模板图像
    img = cv2.imread('images/original.png', 0)
    template = cv2.imread('images/template.png', 0)
    # 获取模板图像的宽度和高度
    w, h = template.shape[::-1]
    # 使用模板匹配算法
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    # 设置阈值
    threshold = 0.8
    # 获取匹配位置
    loc = np.where(res >= threshold)
    # 标记匹配位置
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
    # 显示结果
    cv2.imshow('Detected', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def screenshot_cv_mouseMove(x1, y1, x2, y2):
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    template = cv2.imread('images/template.png', 0)
    # cv2.imshow('img', img)
    # cv2.imshow('template', template)
    # 使用模板匹配算法
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    # 获取最大匹配值和对应位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print("max_val", max_val, max_loc)
    print("min_val", min_val, min_loc)
    threshold = 0.8
    if (max_val < threshold):
        print("no find")
        return
    top_left = max_loc
    print("template.shape", template.shape)
    # 获取模板图像的宽度和高度
    w, h = template.shape[::-1]
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img, top_left, bottom_right, (0, 255, 255), 2)
    pyautogui.moveTo(top_left[0], top_left[1], duration=0.5)
    pyautogui.click()
    while True:
        cv2.imshow('detect', img)
        cv2.moveWindow('detect', 0, 0)
        key = cv2.waitKey(1000) & 0xFF
        if key == ord('q'):
            print("break")
            cv2.destroyAllWindows()
            break
        else:
            print("continue")

def get_window_handles():
    window_handles = gw.getAllTitles()
    for handle in window_handles:
        print(handle)


if __name__ == "__main__":
    # screenshot_window(0, 0, 500, 500)
    # screenshot_cv(0, 0, 500, 500)
    # mouseMove()
    # screenshot_cv_template()
    screenshot_cv_mouseMove(0, 0, 600, 600)
    # get_window_handles()