import json
import os

ConfigJsonName = 'config1.json'
filename = ConfigJsonName


class Config:
    def __init__(self, username=None, password=None, url="http://172.16.253.3/"):

        self.username = username
        self.password = password
        self.url = url
        self.false_count = 0
        self.ui = True
        self.first_run = True

        if self.CheckAndCreateFile():
            self.GetConfigJson()
        else:
            self.FirstTimeRun()



    def FirstTimeRun(self):
        with open(ConfigJsonName, 'w') as f:
            info = {
                'username': None,
                'password': None,
                'url': 'http://172.16.253.3/',
                'ui': True,
                'false_count': 0,
                'first_run': True,
            }
            json.dump(info, f, indent=4)

    def CheckAndCreateFile(self):
        return os.path.isfile(ConfigJsonName)

    def GetConfigJson(self):
        if self.CheckAndCreateFile():
            with open(ConfigJsonName, 'r') as f:
                cong = json.load(f)
            self.username = cong['username']
            self.password = cong['password']
            self.url = cong['url']
            self.ui = cong['ui']
            self.false_count = cong['false_count']
            self.first_run = cong['first_run']

    def SetConfigJson(self, key, new_vlaue):
        with open(ConfigJsonName, 'r') as f:
            data = json.load(f)
        data[key] = new_vlaue
        with open(ConfigJsonName, 'w') as f:
            json.dump(data, f, indent=4)
        self.GetConfigJson()

    def AddFalseCount(self):
        with open(ConfigJsonName, 'r+') as f:
            cong = json.load(f)
            count = cong['false_count']
            cong['false_count'] = count + 1
            f.seek(0)  # 将文件指针移动到文件开头
            f.truncate()  # 清空文件内容
            json.dump(cong, f)

    def ResetFalseCount(self):
        with open(ConfigJsonName, 'r+') as f:
            cong = json.load(f)
            cong['false_count'] = 0
            f.seek(0)  # 将文件指针移动到文件开头
            f.truncate()  # 清空文件内容
            json.dump(cong, f)

