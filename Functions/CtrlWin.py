import winreg
import os
import threading
import win32api
from plyer import notification


def WinNotice(title, message):
    def notif():
        notification.notify(title=title, message=message, timeout=5)

    notification_thread = threading.Thread(target=notif)
    notification_thread.start()


def is_user_logged_in():
    try:
        # 尝试获取当前登录用户的用户名
        win32api.GetUserName()
        return True
    except:
        # 如果获取用户名失败，则表示没有用户登录
        return False


def RegisterRegistry():
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

