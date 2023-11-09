from Functions.Login import *
from Functions.Config import Config
from plyer import notification
import threading
import winreg
import os
import pywintypes
import win32api


def run_noti():
    if cong.ui:
        login_ui(cong)
    end = Login(cong.username, cong.password, cong.url)
    if end:
        note = '登录成功'
        # cong.ResetFalseCount()
    else:
        note = '登录失败'
        # cong.AddFalseCount()

    def notif():
        notification.notify(title=f'登录到{cong.url}', message=note, timeout=10)

    notification_thread = threading.Thread(
        target=notif)
    notification_thread.start()


def is_user_logged_in():
    try:
        # 尝试获取当前登录用户的用户名
        win32api.GetUserName()
        return True
    except:
        # 如果获取用户名失败，则表示没有用户登录
        return False


# # 调用函数检测用户是否登录
# if is_user_logged_in():
#     print("有用户登录")
# else:
#     print("没有用户登录")
#

def main():
    while True:
        _win_logined = is_user_logged_in()
        _login_first = True
        if _win_logined and _login_first:
            notification_thread = threading.Thread(target=run_noti)
            notification_thread.start()
            _login_first = False
            time.sleep(600)
        else:
            _login_first = True
            time.sleep(30)


def set_autostart():
    if cong.first_run:
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
        cong.SetConfigJson('first_run', False)


if __name__ == '__main__':
    try:
        cong = Config()
        set_autostart()
        main()
    except:
        pass
