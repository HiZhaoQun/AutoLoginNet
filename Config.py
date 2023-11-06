import json
import os
ConfigJsonName = 'config.json'
def CheckAndCreateFile(filename = ConfigJsonName):
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            return True
    else:
        return True
    

def WriteJson(username, password, filename = ConfigJsonName):
    if CheckAndCreateFile():
        with open(filename, 'w') as f:
            userinfo = {
                'UserInfo':{
                    'username':username,
                    'password':password
                }
            }
            json.dump(userinfo, f)

def GetConfigJson(filename = ConfigJsonName):
    if CheckAndCreateFile():
        with open(filename, 'r') as f:
            return json.load(f)


WriteJson('aa', 'ce')
print(GetConfigJson()['UserInfo'])




    