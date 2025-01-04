import sys
sys.path.append(".")
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from web_scraper.selenium import SeleniumHelper


class FeloScraper:
    
    def __init__(self):
        super().__init__()

        self.driver = SeleniumHelper.init_driver()
        
    def gen_prompt(
        self,
        shop_name: str
    ) -> str:
        return f"請問 {shop_name} 平均價格是多少?又有提供哪些服務呢?"
        
    def get_shop_info(
        self,
        shop_name: str
    ) -> str:
        prompt = self.gen_prompt(shop_name)
        
        self.driver.get('https://felo.ai/zh-Hant/search')

        text_area = self.driver.find_element(By.TAG_NAME, "textarea")
        text_area.send_keys(prompt)

        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # 等待新頁面的特定元素出現
        wait = WebDriverWait(self.driver, 60)
        result = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.prose.prose-md"))
        )
        
        time.sleep(10)
        html_content = result.get_attribute("innerHTML")
        
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 取得純文字，去除 HTML 標籤
        text_content = soup.get_text(separator='\n', strip=True)

        return text_content
