import pyautogui
import threading
import json


class MouseRecorder:
    # 鼠标记录器
    def __init__(self, interval_ms=500):
        self.record_interval_ms = interval_ms
        self.position_list = []
        self.running = False

    def start(self):
        self.record_timer = threading.Timer(
            self.record_interval_ms/1000, self.record_handler)
        self.record_timer.start()
        self.position_list.clear()
        self.running = True

    def stop(self):
        self.running = False

    def record_handler(self):
        if (self.running):
            self.position_list.append(pyautogui.position())
            self.record_timer = threading.Timer(
                self.record_interval_ms/1000, self.record_handler)
            self.record_timer.start()

    def export(self, save):
        # 导出当前数据
        save.mouse_interval_ms = self.record_interval_ms
        save.mouse_pos_list = self.position_list


class RecorderSave:
    # 记录存档
    def __init__(self):
        self.mouse_interval_ms = 0
        self.mouse_pos_list = []

    def write(self, file_name):
        # 写入json文件
        with open(f'{file_name}.json', 'w') as file:
            json.dump(self, file, indent=4)
