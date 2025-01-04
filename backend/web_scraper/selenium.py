from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumHelper:
    @staticmethod
    def init_driver():
        """初始化無頭模式的 Chrome driver"""

        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 啟用無頭模式
        chrome_options.add_argument('--disable-gpu')  # 某些系統需要
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)

        return driver
