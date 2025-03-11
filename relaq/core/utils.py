from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import platform
import os


class SeleniumHelper:
    @staticmethod
    def init_driver():
        """初始化 Chrome driver，支援多平台"""

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # 根據系統架構選擇適當的設置
        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == 'linux' and ('aarch64' in machine or 'arm64' in machine):
            # ARM64 Linux 特殊處理
            chrome_binary = settings.CHROMIUM_BINARY
            chrome_options.binary_location = chrome_binary
            # 確保已安裝 chromium-chromedriver
            service = Service(settings.CHROMEDRIVER_PATH)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            # 其他平台的標準設置
            driver = webdriver.Chrome(options=chrome_options)

        driver.implicitly_wait(10)
        return driver

    @staticmethod
    def ensure_driver_installed():
        """確保必要的驅動程式已安裝"""
        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == 'linux' and ('aarch64' in machine or 'arm64' in machine):
            # 檢查是否已安裝必要套件
            if not os.path.exists('/usr/bin/chromium-browser'):
                raise RuntimeError(
                    "請先安裝 Chromium：\n"
                    "sudo apt-get update && "
                    "sudo apt-get install -y chromium-browser chromium-chromedriver"
                )
