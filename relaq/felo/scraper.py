import re
import time
import logging

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.utils import SeleniumHelper


logger = logging.getLogger(__name__)


class FeloScraper:
    FELO_URL = "https://felo.ai/zh-Hant/search"
    LINE_END_CITATION_REGEX = r'\s*\d+(\s+\d+)*\s*$'
    SENTENCE_END_CITATION_REGEX = r'\s*\d+(\s+\d+)*\s*。'

    def __init__(self):
        super().__init__()

        logger.info("[Felo] 初始化 Selenium driver")
        self.driver = SeleniumHelper.init_driver()
        logger.info("[Felo] 初始化 Selenium driver 完成")

    def gen_price_and_service_prompt(
        self,
        shop_name: str
    ) -> str:
        return f"請問台灣美甲店 '{shop_name}' 提供哪些服務? 每種服務的價格又是多少?"

    def search(
        self,
        prompt: str
    ) -> str:
        logger.info(f"[Felo] 開始抓取資料")
        
        self.driver.get(self.FELO_URL)

        text_area = self.driver.find_element(By.TAG_NAME, "textarea")
        text_area.send_keys(prompt)

        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # 等待新頁面的特定元素出現
        wait = WebDriverWait(self.driver, 60)
        result = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.prose.prose-md"))
        )

        for sec in range(1, 11):
            logger.info(f"[Felo] 等待資料完成... {sec} 秒")
            time.sleep(1)

        html_content = result.get_attribute("innerHTML")

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 取得純文字，去除 HTML 標籤
        text_content = soup.get_text(separator='\n', strip=True)
        text_content = self._clean_data(text_content)

        logger.info(f"[Felo] 抓取資料完成")

        return text_content

    def _clean_data(self, text: str) -> str:
        """清理從 Felo 抓取的數據，移除引用標記

        Args:
            text (str): 從 Felo 抓取的數據

        Returns:
            str: 清理後的數據
        """

        cleaned_text = re.sub(self.LINE_END_CITATION_REGEX, '', text, flags=re.MULTILINE)
        cleaned_text = re.sub(self.SENTENCE_END_CITATION_REGEX, '。', cleaned_text)

        return cleaned_text
