from Functions.Config import Config
from Functions.Login import LoginManager
from Functions.CtrlWin import *


def run(config):
    """
    调用登录，界面登录
    :param config:配置文件
    :return: 无
    """
    # 全局变量
    title = ''
    message = ''
    login_info = LoginManager()
    # 获取配置信息并进行登录
    for i in range(2):
        # 判断是否首次使用ui登录，如果是， 通过ui填入登录信息
        if config.ui:
            config.SetConfigJsonByUi()

        # 开始登录
        end = login_info.login(config.username, config.password, config.url)
        if end:
            title = f'登录到{config.url[:20]}'
            message = '登录成功'
            break
        else:
            title = f'登录到{config.url[:20]}'
            message = '登录失败'
            if config.first_run:
                config.SetConfigJson('ui', True)
    win_notice(title, message)


if __name__ == '__main__':
    try:
        # 基础配置
        cong = Config()
        run(cong)
        cong.SetConfigJson('first_run', False)

    except:
        win_notice('系统错误', '程序出现未知错误')
