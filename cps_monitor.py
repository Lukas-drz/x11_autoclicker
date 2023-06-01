from pynput.mouse import Listener
import time
import threading

class CPSMonitor:
    def __init__(self):
        self.clicks = 0
        self.start_time = time.time()
        self.listener = Listener(on_click=self.on_click)
        self.listener.start()
        self.lock = threading.Lock()

    def calculate_cps(self):
        elapsed_time = time.time() - self.start_time
        with self.lock:
            cps = self.clicks / elapsed_time
            self.clicks = 0
            self.start_time = time.time()
            return cps

    def start_monitoring(self):
        while True:
            cps = self.calculate_cps()
            time.sleep(0.5)

    def stop_monitoring(self):
        self.listener.stop()

class CPSMonitorLeftClick(CPSMonitor):
    def on_click(self, x, y, button, pressed):
        if pressed and button == button.left:
            with self.lock:
                self.clicks += 1

class CPSMonitorRightClick(CPSMonitor):
    def on_click(self, x, y, button, pressed):
        if pressed and button == button.right:
            with self.lock:
                self.clicks += 1
