from Functions.Config import Config
from Functions.Login import *
from Functions.CtrlWin import *


def Run(config):
    # 全局变量
    note = ''
    title = ''
    # 获取配置信息并进行登录
    for i in range(2):
        # 判断是否首次使用ui登录，如果是， 通过ui填入登录信息
        if config.ui:
            config.SetConfigJsonByUi()
        end = Login(config.username, config.password, config.url)
        if end:
            note = '登录成功'
            title = f'登录到{config.url[:20]}'
            break
        else:
            note = '登录失败'
            title = f'登录到{config.url[:20]}'
            if config.first_run:
                config.SetConfigJson('ui', True)
    # 将登录结果通知到win桌面
    WinNotice(title, note)


if __name__ == '__main__':
    global cong
    try:
        cong = Config()
        if cong.first_run:
            RegisterRegistry()
        Run(cong)
    except:
        WinNotice('系统错误', '程序出现未知错误')
    # cong.SetConfigJson('ui', False)
    cong.SetConfigJson('first_run', False)

