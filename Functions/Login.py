import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium import webdriver


def CheckStatus(brower):
    success_messages = [
        '终端IP已经在线',
        '你已经成功登录。',
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


def PutInfo(brower, username, password):
    try:
        username_location = WebDriverWait(brower, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form .edit_lobo_cell[type='text']")))
        password_location = WebDriverWait(brower, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form .edit_lobo_cell[type='password']")))
        reset_location = WebDriverWait(brower, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form .edit_lobo_cell[type='reset']")))
        log_location = WebDriverWait(brower, 10).until(
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

def GetBack(brower):
    try:
        back = WebDriverWait(brower, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.edit_lobo_cell[name='GobackButton']")))
        back.send_keys(Keys.ENTER)
        return True
    except (NoSuchElementException, TimeoutException):
        return False

def PutAndCheck(brower, username, password):
    PutInfo(brower, username, password)
    # 登录成功则返回true
    if CheckStatus(brower=brower):
        brower.close()
        return True
    return False

def Login(username, password, url):
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_argument('--headless --disable-gpu --no-sandbox')
    # options.add_argument('-ignore-certificate-errors')
    # options.add_argument('-ignore -ssl-errors')
    # op = webdriver.EdgeOptions()
    # op.add_experimental_option("detach", True)
    brower = webdriver.Edge(options=options)
    # brower = webdriver.Edge()
    brower.set_page_load_timeout(5)

    for _ in range(2):
        # 先对url进行访问，访问成功才进行下一步，否则直接跳出，返回false
        try:
            brower.get(url)
        except:
            break

        if PutAndCheck(brower, username, password):
            return True
        if GetBack(brower):
            if PutAndCheck(brower, username, password):
                return True
        else:
            break

    brower.close()
    return False