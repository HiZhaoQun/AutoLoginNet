import time

from Functions.Login import *
from Functions.Config import Config
from win10toast import ToastNotifier
from plyer import notification
import threading
import pywintypes
import win32api

import winreg
import os



def run_noti():
    cong = Config()
    if cong.ui:
        login_ui(cong)

    end = Login(cong.username, cong.password, cong.url)

    if end:
        note = '登录成功'
        cong.ResetFalseCount()
    else:
        note = '登录失败'
        cong.AddFalseCount()

    def notif():
        notification.notify(title=f'登录到{cong.url}', message=note, timeout=10)

    notification_thread = threading.Thread(
        target=notif)
    notification_thread.start()


def main():
    _logined = False
    while True:
        if not _logined:
            _logined = True
            notification_thread = threading.Thread(target=run_noti)
            notification_thread.start()
            time.sleep(5)

        else:
            time.sleep(300)
            # _logined = False


def set_autostart():
    try:
        # 打开注册表项
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, '''Software\Microsoft\Windows\CurrentVersion\Run''', 0,
                             winreg.KEY_ALL_ACCESS)
        # 设置程序的路径作为键值
        current_file = os.path.abspath(__file__)
        winreg.SetValueEx(key, "MyProgram", 0, winreg.REG_SZ, current_file)
        # 关闭注册表项
        winreg.CloseKey(key)
        notification.notify(title=f'注册表成功', message='success', timeout=10)
    except Exception as e:
        notification.notify(title=f'注册表失败', message='false', timeout=10)
    finally:
        pass


if __name__ == '__main__':
    set_autostart()
    main()
