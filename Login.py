import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "http://172.16.253.3/"
LOGURL = "http://172.16.253.3/a79.htm?wlanusermac=CC-6B-1E-A2-15-31&wlanuserip=172.31.72.102&wlanssid=ahu%2Eportal&wlanacname=AHULHAC"

UserName = "Y02114279"
PassWord = "1A2B3C4d5e6f@"


def CheckStatus(brower):
    try:
        wait = WebDriverWait(brower, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '''div#message.edit_lobo_cell''')))
        status = brower.find_element(By.CSS_SELECTOR, '''div#message.edit_lobo_cell''').text
    except selenium.common.exceptions.NoSuchElementException:
        return False
    success = [
        '终端IP已经在线',
        '你已成功登录',
    ]
    false = [
        'Radius认证超时',

    ]
    if status in success:
        return True
    else:
        return False
    


def input(brower):


    username = brower.find_element(By.CSS_SELECTOR, '''form .edit_lobo_cell[type='text']''')
    password = brower.find_element(By.CSS_SELECTOR, '''form .edit_lobo_cell[type='password']''')
    reset = brower.find_element(By.CSS_SELECTOR, '''form .edit_lobo_cell[type='reset']''')
    log = brower.find_element(By.CSS_SELECTOR, '''form .edit_lobo_cell[type='submit']''')

    reset.send_keys(Keys.ENTER)
    username.send_keys(UserName)
    password.send_keys(PassWord)
    log.send_keys(Keys.ENTER)

    # CheckStatus(brower=brower)
    # time.sleep(5)



def login():
    brower = webdriver.Edge()

    flag = False
    for i in range(3):
        brower.get(URL)
        input(brower=brower)
        if CheckStatus(brower=brower):
            flag=True
            print('login success')
            break
    if not flag:
        print('login false')
    brower.close()

login()


