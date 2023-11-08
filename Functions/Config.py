import json
import os

ConfigJsonName = 'config1.json'


class Config:
    def __init__(self, username=None, password=None, url="http://172.16.253.3/"):
        self.username = username
        self.password = password
        self.url = url
        self.false_count = 0
        self.ui = True
        if self.CheckAndCreateFile(ConfigJsonName):
            self.GetConfigJson()
            if self.false_count == 3:
                self.ui = True
                self.ResetFalseCount()
        else:
            self.WriteConfigJson(self.username, self.password, self.url)

    def CheckAndCreateFile(self, filename=ConfigJsonName):
        if not os.path.isfile(filename):
            return False
        else:
            return True

    def GetConfigJson(self, filename=ConfigJsonName):
        if self.CheckAndCreateFile():
            with open(filename, 'r') as f:
                cong = json.load(f)
                self.username = cong['UserInfo']['username']
                self.password = cong['UserInfo']['password']
                self.url = cong['AppInfo']['url']
                self.ui = cong['AppInfo']['ui']
                self.false_count = cong['AppInfo']['false_count']

    def WriteConfigJson(self, username=None, password=None,
                        url='http://172.16.253.3/', ui=True,
                        filename=ConfigJsonName):
        with open(filename, 'w') as f:
            info = {
                'UserInfo': {
                    'username': username,
                    'password': password,
                },
                'AppInfo': {
                    'url': url,
                    'ui': ui,
                    'false_count': self.false_count
                }
            }
            json.dump(info, f)
        self.GetConfigJson()

    def AddFalseCount(self, filename=ConfigJsonName):
        with open(filename, 'r+') as f:
            cong = json.load(f)
            count = cong['AppInfo']['false_count']
            cong['AppInfo']['false_count'] = count + 1
            f.seek(0)  # 将文件指针移动到文件开头
            f.truncate()  # 清空文件内容
            json.dump(cong, f)

    def ResetFalseCount(self, filename=ConfigJsonName):
        with open(filename, 'r+') as f:
            cong = json.load(f)
            cong['AppInfo']['false_count'] = 0
            f.seek(0)  # 将文件指针移动到文件开头
            f.truncate()  # 清空文件内容
            json.dump(cong, f)
