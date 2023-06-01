from Xlib import X, display
from pynput.mouse import Button, Controller
from pynput import keyboard
import time
import random
from cps_monitor import CPSMonitorLeftClick, CPSMonitorRightClick
import threading
import subprocess
import notify2

target_window = int(subprocess.check_output("xwininfo -root -tree | grep \"Lunar Client\"", shell=True).split()[0].decode('utf-8'), 16)
click_interval = 0.05  # Random interval added to the click speed
is_paused = False
notify2.init("Auto clicker")
n_active = notify2.Notification("Auto clicker",
                                "Auto clicker started",
                                "cursor.png"   # Icon name
                                )
n_stop = notify2.Notification("Auto clicker",
                                "Auto clicker stopped",
                                "cursor.png"   # Icon name
                                )
n_active.show()

def on_key_press(key):
    global is_paused
    if key == keyboard.KeyCode.from_char('`'):
        is_paused = not is_paused
        if is_paused:
            print("Auto clicker paused")
            n_active.close()
            n_stop.show()
        else:
            print("Auto clicker resumed")
            n_stop.close()
            n_active.show()


def auto_clicker_when_more_4cps(target_window, click_interval):
    d = display.Display()
    root = d.screen().root
    mouse = Controller()

    cps_monitor_right_click = CPSMonitorRightClick()
    cps_monitor_left_click = CPSMonitorLeftClick()
    cps_monitor_right_click_thread = threading.Thread(target=cps_monitor_right_click.start_monitoring)
    cps_monitor_right_click_thread.start()
    cps_monitor_left_click_thread = threading.Thread(target=cps_monitor_left_click.start_monitoring)
    cps_monitor_left_click_thread.start()
    
    keyboard_listener = keyboard.Listener(on_press=on_key_press)
    keyboard_listener.start()

    while True:
        with cps_monitor_right_click.lock:
            cps_right_click = cps_monitor_right_click.clicks / (time.time() - cps_monitor_right_click.start_time)
        with cps_monitor_left_click.lock:
            cps_left_click = cps_monitor_left_click.clicks / (time.time() - cps_monitor_left_click.start_time)
        
        if not is_paused and root.get_full_property(d.intern_atom('_NET_ACTIVE_WINDOW'), X.AnyPropertyType).value[0] == target_window:
            # print("cps left : " + str(cps_left_click))
            # print("cps right : " + str(cps_right_click))

            if cps_left_click > 6:
                mouse.click(Button.left, 1)

            if cps_right_click > 6:
                mouse.click(Button.right, 1)

        time.sleep(random.uniform(0, click_interval))


auto_clicker_when_more_4cps(target_window, click_interval)


# add a key listener to stop the program
from pynput import keyboard
def on_press(key):
    if key == keyboard.Key.esc:
        exit()
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()