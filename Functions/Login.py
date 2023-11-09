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
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '''div.edit_lobo_cell''')))
        status = brower.find_element(By.CSS_SELECTOR, '''div.edit_lobo_cell''').text
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
    # edge_options = Options()
    # edge_options.add_argument("--remote-allow-origins=*")
    # driver = webdriver.Edge(options=edge_options)
    options = webdriver.EdgeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # web = webdriver.Chrome(options=options)
    brower = webdriver.Edge(options=options)
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
        cong.SetConfigJson('username', username)
        cong.SetConfigJson('password', password)
        cong.SetConfigJson('url', target_url)
        cong.SetConfigJson('ui', False)


def login_request():
    url = '''http://172.16.253.3:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=Y02114279&user_password=1A2B3C4d5e6f%40&wlan_user_ip=172.21.2.58&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=172.16.253.1&wlan_ac_name=&jsVersion=3.3.2&v=5237'''
