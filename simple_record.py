import pyautogui
import threading
import time

class MouseRecorder:
    #鼠标记录器
    def __init__(self,interval_ms=500):
        self.record_interval_ms=interval_ms
        self.position_list=[]
        self.running=False
    
    def start(self):
        self.record_timer= threading.Timer(self.record_interval_ms/1000,self.record_handler)
        self.record_timer.start()
        self.position_list.clear()
        self.running=True

    def stop(self):
        self.running=False
    
    def record_handler(self):
        if(self.running):
            self.position_list.append(pyautogui.position())
            self.record_timer= threading.Timer(self.record_interval_ms/1000,self.record_handler)
            self.record_timer.start()