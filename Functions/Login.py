import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium import webdriver


class LoginManager:
    """
    该类用于浏览器配置和网页登录
    """

    def __init__(self):
        """
        初始化一个浏览器
        """
        self.driver_path = ".\Sources\msedgedriver.exe"
        self.options = webdriver.EdgeOptions()
        # self.options.add_argument('--headless')
        self.options.add_argument('-ignore-ssl-errors')
        self.options.add_argument("--disable-extensions")
        self.browser = webdriver.Edge(executable_path=self.driver_path, options=self.options)
        self.browser.set_page_load_timeout(5)

    def is_not_logged(self):
        """
        根据页面显示信息检测是否已经登录
        :return:True or False
        """
        success_messages = [
            '终端IP已经在线',
            '您已经成功登录。',
        ]

        try:
            wait = WebDriverWait(self.browser, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.edit_lobo_cell')))
            status = self.browser.find_element(By.CSS_SELECTOR, 'div.edit_lobo_cell').text
        except (NoSuchElementException, TimeoutException):
            return False

        return status in success_messages

    def put_info(self, username, password):
        """
        填入信息
        :param username: 用户名
        :param password: 用户密码
        :return: 无
        """
        try:
            username_location = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "form .edit_lobo_cell[type='text']")))
            password_location = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "form .edit_lobo_cell[type='password']")))
            reset_location = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "form .edit_lobo_cell[type='reset']")))
            log_location = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "form .edit_lobo_cell[type='submit']")))

            reset_location.send_keys(Keys.ENTER)
            username_location.send_keys(username)
            password_location.send_keys(password)
            log_location.send_keys(Keys.ENTER)

        except (NoSuchElementException, TimeoutException):
            pass

        if self.is_not_logged():
            self.browser.close()
            return True
        return False

    def get_back(self):
        """
        无线和有线连接下登陆后网址不同，会提示网址错误，此时返回，这样就获取到了正确的网址
        :return: True or False
        """
        try:
            back = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.edit_lobo_cell[name='GobackButton']")))
            back.send_keys(Keys.ENTER)
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def login(self, username, password, url):
        """
        调用登录和错误检测等
        :param username: 用户名
        :param password: 用户密码
        :param url: 登录网址
        :return: True or False
        """
        for _ in range(2):
            try:
                self.browser.get(url)
            except TimeoutException:
                break

            if self.put_info(username, password):
                return True
            if self.get_back():
                if self.put_info(username, password):
                    return True
            else:
                break

        self.browser.close()
        return False
