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
        prompt: str,
        max_retries: int = 3,
        retry_delay: int = 5
    ) -> str:
        """搜尋 Felo 並返回結果
        
        Args:
            prompt: 搜尋提示
            max_retries: 最大重試次數
            retry_delay: 重試間隔（秒）
            
        Returns:
            str: 搜尋結果
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"[Felo] 開始抓取資料 (嘗試 {attempt + 1}/{max_retries})")
                
                # 確保頁面完全加載
                self.driver.get(self.FELO_URL)
                time.sleep(3)  # 等待頁面初始加載
                
                # 等待搜尋框出現並可交互
                try:
                    text_area = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.TAG_NAME, "textarea"))
                    )
                    WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.TAG_NAME, "textarea"))
                    )
                except Exception as e:
                    logger.error(f"[Felo] 等待搜尋框失敗: {str(e)}")
                    raise
                
                print("[Felo] 輸入搜尋條件...")
                text_area.clear()  # 清除可能的舊內容
                text_area.send_keys(prompt)
                
                # 等待並點擊提交按鈕
                try:
                    submit_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
                    )
                    submit_button.click()
                except Exception as e:
                    logger.error(f"[Felo] 點擊提交按鈕失敗: {str(e)}")
                    raise
                
                # 等待結果出現
                print("[Felo] 等待資料完成...")
                try:
                    wait = WebDriverWait(self.driver, 160)  # 增加等待時間到 160 秒
                    result = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.prose.prose-md"))
                    )
                    # 確保內容已經完全加載
                    wait.until(
                        lambda driver: len(result.text.strip()) > 0
                    )
                except Exception as e:
                    logger.error(f"[Felo] 等待結果出現失敗: {str(e)}")
                    raise
                
                # 額外等待確保內容完全加載
                time.sleep(5)  # 固定等待 5 秒
                
                html_content = result.get_attribute("innerHTML")
                if not html_content.strip():
                    raise Exception("獲取到的內容為空")
                
                # 使用 BeautifulSoup 解析 HTML
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # 取得純文字，去除 HTML 標籤
                text_content = soup.get_text(separator='\n', strip=True)
                if not text_content.strip():
                    raise Exception("解析後的內容為空")
                    
                text_content = self._clean_data(text_content)
                
                logger.info(f"[Felo] 抓取資料完成")
                return text_content
                
            except Exception as e:
                logger.error(f"[Felo] 抓取失敗 (嘗試 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    logger.info(f"[Felo] 等待 {retry_delay} 秒後重試...")
                    time.sleep(retry_delay)
                    # 重新初始化 driver
                    try:
                        self.driver.quit()
                    except:
                        pass
                    self.driver = SeleniumHelper.init_driver()
                else:
                    logger.error("[Felo] 達到最大重試次數，放棄抓取")
                    return ""

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
