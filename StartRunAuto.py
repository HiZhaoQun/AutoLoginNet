import pywintypes
import win32api

def is_user_logged_in():
    try:
        # 尝试获取当前登录用户的用户名
        username = win32api.GetUserName()
        return True
    except pywintypes.error:
        # 如果获取用户名失败，则表示没有用户登录
        return False

# 调用函数检测用户是否登录
if is_user_logged_in():
    print("有用户登录")
else:
    print("没有用户登录")
    