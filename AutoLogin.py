from Functions.Config import Config
from Functions.Login import *
from Functions.CtrlWin import *


def Run(config):

    _note = ''
    # 获取配置信息并进行登录
    for i in range(2):
        # 判断是否首次使用ui登录，如果是， 通过ui填入登录信息
        if config.ui:
            config.SetConfigJsonByUi()
        end = Login(config.username, config.password, config.url)
        if end:
            _note = '登录成功'
            title = f'登录到{config.url[:20]}'
            break
        else:
            _note = '登录失败'
            title = f'登录到{config.url[:20]}'
            if config.first_run:
                config.SetConfigJson('ui', True)
    # 将登录结果通知到win桌面
    WinNotice(title, _note)


if __name__ == '__main__':
    try:
        cong = Config()
        RegisterRegistry(cong)
        Run(cong)
    except:
        WinNotice('系统错误', '程序出现未知错误')
    # cong.SetConfigJson('ui', False)
    cong.SetConfigJson('first_run', False)

