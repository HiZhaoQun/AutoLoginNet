import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# selenium 4
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import easygui
from Functions.Config import Config


def CheckStatus(brower):
    success_messages = [
        '终端IP已经在线',
        '你已成功登录',
    ]
    false_messages = [
        'Radius认证超时',
        'AC认证失败，请检查账号密码',
    ]

    try:
        wait = WebDriverWait(brower, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '''div#message.edit_lobo_cell''')))
        status = brower.find_element(By.CSS_SELECTOR, '''div#message.edit_lobo_cell''').text
        # status2 = brower.find_element(By.CSS_SELECTOR, '''''')
    except (NoSuchElementException, TimeoutException):
        return False

    return status in success_messages


def PutInfo(browser, username, password):
    try:
        username_location = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form .edit_lobo_cell[type='text']")))
        password_location = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form .edit_lobo_cell[type='password']")))
        reset_location = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form .edit_lobo_cell[type='reset']")))
        log_location = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form .edit_lobo_cell[type='submit']")))

        reset_location.send_keys(Keys.ENTER)
        username_location.send_keys(username)
        password_location.send_keys(password)
        # print(username, password)
        log_location.send_keys(Keys.ENTER)

    except (NoSuchElementException, TimeoutException) as e:
        pass
    finally:
        pass


def Login(username, password, url):
    # brower = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    brower = webdriver.Edge()
    brower.set_page_load_timeout(5)

    for i in range(2):
        try:
            brower.get(url)
        except TimeoutException:
            return False
        except selenium.common.exceptions.WebDriverException as e:
            return False
        finally:
            pass
        PutInfo(brower, username, password)
        if CheckStatus(brower=brower):
            brower.close()
            return True

    brower.close()
    return False

def get_credentials(username, password, default_url):
    msg = "请输入账号、密码和目标网址:"
    title = "登录信息"
    field_names = ["账号", "密码", "目标网址"]
    field_values = easygui.multenterbox(
        msg, title, field_names, [username, password, default_url])
    return field_values


def login_ui(cong):
    credentials = get_credentials(cong.username, cong.password, cong.url)
    if credentials is not None:
        username, password, target_url = credentials
        # print("账号:", username)
        # print("密码:", password)
        # print("目标网址:", target_url)
        cong.WriteConfigJson(username, password, target_url, False)

