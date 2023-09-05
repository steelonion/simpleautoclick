import json
from pynput import keyboard, mouse
import time
from enum import IntEnum
import pyautogui


class Replayer:
    def __init__(self, save):
        self.save = save
        self.start_timestamp = 0

    def replay(self):
        print("replay now...")
        self.start_timestamp = time.time()
        for action in self.save.content["mouse_move"]:
            while (action[0] > time.time()-self.start_timestamp):
                time.sleep(0.1)
            if (action[1] == EAction.mousemove.value):
                pyautogui.moveTo(action[2], action[3])


class EAction(IntEnum):
    mousemove = 1
    keydown = 3
    keyup = 4


class InputRecorder:
    # 记录器
    def __init__(self, quit_key: str = 'q'):
        self.record_interval = 0.2
        self.next_record_time = 0
        self.running = False
        self.quit_key = quit_key
        self.position_list = []
        self.key_list = []
        self.start_timestamp = 0
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press, on_release=self.on_key_release)
        self.mouse_listener = mouse.Listener(
            on_move=self.on_mouse_move, on_click=self.on_mouse_click, on_scroll=self.on_mouse_scroll)
        print(f"quit_key:{self.quit_key}")

    def start(self):
        self.running = True
        self.next_record_time = 0
        self.start_timestamp = time.time()
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def stop(self):
        self.running = False
        self.keyboard_listener.stop()
        self.mouse_listener.stop()

    def export(self, save):
        # 导出当前数据
        save.content["mouse_move"] = self.position_list
        save.content["key_action"] = self.key_list

    # 键盘事件回调函数
    def on_key_press(self, key):
        if (key.char == self.quit_key):
            self.stop()
            return
        timespan = time.time()-self.start_timestamp
        self.key_list.append((timespan, EAction.keydown, key.char))

    def on_key_release(self, key):
        timespan = time.time()-self.start_timestamp
        self.key_list.append((timespan, EAction.keyup, key.char))

    # 鼠标事件回调函数
    def on_mouse_move(self, x, y):
        timespan = time.time()-self.start_timestamp
        if (timespan > self.next_record_time):
            self.next_record_time = timespan+self.record_interval
            self.position_list.append((timespan, EAction.mousemove, x, y))
            print(f'鼠标移动到 ({x}, {y})')

    def on_mouse_click(self, x, y, button, pressed):
        action = '点击' if pressed else '释放'
        print(f'鼠标{action}: ({x}, {y})')

    def on_mouse_scroll(self, x, y, dx, dy):
        print(f'鼠标滚轮滚动: ({x}, {y}) ({dx}, {dy})')


class RecorderSave:
    # 记录存档
    def __init__(self):
        self.content = {}

    def write(self, file_name):
        # 写入json文件
        with open(f'{file_name}.json', 'w') as file:
            json.dump(self.content, file, indent=4)
