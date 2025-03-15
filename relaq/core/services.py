import time
import logging
import re
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from enum import Enum

from cms.models import Shop, ShopTag
from cms.constants import CITY_PATTERN, DISTRICT_PATTERN
from chatgpt.services import ChatGPTHelper
from chatgpt.constants import SUMMARY_PROMPT, TAG_PROMPT
from felo.scraper import FeloScraper
from googlemap.services import GoogleMapHelper
from googlemap.models import PlaceDetail
from outscrapers.services import OutscraperHelper

logger = logging.getLogger(__name__)

class SummarySection(Enum):
    CORE_FEATURES = 'B. 核心特色'
    REVIEW_SUMMARY = 'C. 評價摘要'
    RECOMMENDED_USES = 'D. 推薦用途'
    BASIC_INFO = 'A.'

@dataclass
class ShopSummary:
    core_features: str
    review_summary: str
    recommended_uses: str

    @classmethod
    def empty(cls) -> 'ShopSummary':
        return cls(core_features="", review_summary="", recommended_uses="")

class AISummaryParser:
    @staticmethod
    def parse_summary(ai_response: str) -> ShopSummary:
        """Parse AI response into structured shop summary.
        
        Args:
            ai_response: Raw AI response text
            
        Returns:
            ShopSummary object containing parsed sections
        """
        sections = {
            'core_features': [],
            'review_summary': [],
            'recommended_uses': []
        }
        
        current_section = None
        
        for line in ai_response.splitlines():
            line = line.strip()
            if not line:
                continue
                
            # Determine current section
            if line.startswith(SummarySection.CORE_FEATURES.value):
                current_section = 'core_features'
            elif line.startswith(SummarySection.REVIEW_SUMMARY.value):
                current_section = 'review_summary'
            elif line.startswith(SummarySection.RECOMMENDED_USES.value):
                current_section = 'recommended_uses'
            elif line.startswith(SummarySection.BASIC_INFO.value):
                current_section = None
            elif current_section:
                sections[current_section].append(line)
        
        return ShopSummary(
            core_features='\n'.join(sections['core_features']).strip(),
            review_summary='\n'.join(sections['review_summary']).strip(),
            recommended_uses='\n'.join(sections['recommended_uses']).strip()
        )

class CoreService:
    def __init__(self, catch_limit: int = 10):
        self.catch_limit = catch_limit
        self.search_keyword = "美甲"
        
        self.google_map_helper = GoogleMapHelper()
        self.outscraper_helper = OutscraperHelper()
        self.felo_scraper = FeloScraper()
        self.chatgpt_helper = ChatGPTHelper()
        self.summary_parser = AISummaryParser()
        
    def _parse_address(self, address: str) -> Tuple[str, str]:
        """解析地址，將其分為縣市和行政區。
        
        Args:
            address: 完整地址字串，例如：
                    "106231台灣台北市大安區信義路四段265巷24號"
                    "106台灣台北市大安區敦化南路二段11巷7號1樓"
            
        Returns:
            Tuple[str, str]: (縣市, 行政區)，若無法解析則返回空字串
        """
        # 移除郵遞區號（3-6位數字）和「台灣」
        clean_address = re.sub(r'^\d{3,6}|台灣', '', address)
        
        # 尋找縣市
        city_match = re.search(CITY_PATTERN, clean_address)
        city = city_match.group(1) if city_match else ""
        
        # 移除縣市名稱，只留下地址後半部
        if city:
            clean_address = clean_address.replace(city, '')
        
        # 尋找行政區
        district_match = re.search(DISTRICT_PATTERN, clean_address)
        district = district_match.group(1) if district_match else ""
        
        return city, district

    def _get_all_shop_data(self, search_query: str) -> List[PlaceDetail]:
        """Fetch shop data from Google Maps API."""
        return self.google_map_helper.search_places(query=search_query)

    def _get_shop_review(self, shop_name: str) -> str:
        """Fetch and process shop reviews."""
        try:
            _, data = self.outscraper_helper.get_map_review(shop_name)
            reviews: List[Dict] = data.get("留言", [])
            return "\n".join(review.get("評論", "") for review in reviews if review.get("評論"))
        except Exception as e:
            logger.error(f"Error fetching reviews for {shop_name}: {str(e)}")
            return ""

    def _get_shop_price_and_service(self, shop_name: str) -> str:
        """Fetch shop price and service information."""
        try:
            content = self.felo_scraper.get_shop_info(shop_name)
            
            # 1. 處理換行+冒號的問題
            content = re.sub(r'\n\s*：', '：', content)  # 處理換行後的冒號
            content = re.sub(r'：\s*\n', '：', content)  # 處理冒號後的換行
            
            # 2. 處理不完整的價格資訊
            content = re.sub(r'\$\d+,(?=\s|\n|$)', lambda m: m.group() + '000', content)  # 補完價格
            
            # 3. 確保段落之間有適當的換行
            content = re.sub(r'。\s*([^。\n])', r'。\n\1', content)  # 在句號後加換行
            
            return content
        except Exception as e:
            logger.error(f"Error fetching price and service for {shop_name}: {str(e)}")
            return ""

    def _gen_shop_basic_info(self, shop_data: PlaceDetail) -> str:
        """Generate formatted shop basic information."""
        return f"""
            店家名稱: {shop_data.name}
            地址: {shop_data.address}
            評分: {shop_data.rating}
            網站: {shop_data.website}
            店家電話: {shop_data.phone}
            總評論數: {shop_data.user_ratings_total}
        """

    def _process_shop_tags(self, ai_tag_response: str) -> List[ShopTag]:
        """Process and create shop tags from AI response."""
        tags = self.chatgpt_helper.convert_tag_response(ai_tag_response)
        shop_tags = []
        
        for tag_data in tags:
            try:
                tag, _ = ShopTag.objects.get_or_create(
                    name=tag_data['name'],
                    type=tag_data['type'],
                    defaults={
                        'emoji': tag_data['emoji'],
                        'description': tag_data['description']
                    }
                )
                shop_tags.append(tag)
            except Exception as e:
                logger.error(f"Error creating tag {tag_data['name']}: {str(e)}")
                
        return shop_tags

    def _create_shop_entry(
        self,
        shop_data: PlaceDetail,
        shop_review: str,
        price_and_service: str,
        summary: ShopSummary,
        tags: List[ShopTag]
    ) -> Shop:
        """Create shop database entry with all collected information."""
        # 解析地址
        city, district = self._parse_address(shop_data.address)
        
        shop = Shop.objects.create(
            name=shop_data.name,
            address=shop_data.address,
            city=city,
            district=district,
            phone=shop_data.phone,
            website=shop_data.website,
            rating=shop_data.rating,
            review_count=shop_data.user_ratings_total,
            reviews=shop_review,
            price_and_service=price_and_service,
            core_features=summary.core_features,
            review_summary=summary.review_summary,
            recommended_uses=summary.recommended_uses,
        )
        shop.tags.set(tags)
        return shop

    def _process_single_shop(
        self,
        shop_data: PlaceDetail,
        index: int,
        total: int
    ) -> Optional[Shop]:
        """Process a single shop's data collection and storage."""
        try:
            # Collect shop information
            shop_basic_info = self._gen_shop_basic_info(shop_data)
            shop_review = self._get_shop_review(shop_data.name)
            price_and_service = self._get_shop_price_and_service(shop_data.name)
            
            # Generate AI summaries
            shop_info = f"""
                店家基本資訊:{shop_basic_info},
                店家評論:{shop_review},
                店家價格與服務:{price_and_service},
            """
            
            ai_summary = self.chatgpt_helper.chat(
                user_input=shop_info,
                system_setting=SUMMARY_PROMPT,
            )
            summary = self.summary_parser.parse_summary(ai_summary)
            
            ai_tag = self.chatgpt_helper.chat(
                user_input=shop_info,
                system_setting=TAG_PROMPT,
            )
            shop_tags = self._process_shop_tags(ai_tag)
            
            # Create shop entry
            shop = self._create_shop_entry(
                shop_data=shop_data,
                shop_review=shop_review,
                price_and_service=price_and_service,
                summary=summary,
                tags=shop_tags
            )
            
            logger.info(f"\033[92m 店家資訊: {shop.name} 抓取成功! 進度: {index}/{total} \033[0m")
            return shop
            
        except Exception as e:
            logger.error(f"Error processing shop {shop_data.name}: {str(e)}")
            return None

    def main(self, search_region: str) -> None:
        """Main execution flow for shop data collection."""
        start_time = time.time()
        logger.info(f"[Core] 開始抓取 {search_region} 的店家資訊")
        
        try:
            # Get all shop data
            search_query = f"{search_region} {self.search_keyword}"
            all_shop_data = self._get_all_shop_data(search_query=search_query)
            total_progress = len(all_shop_data)
            
            if total_progress <= 0:
                logger.warning(f"[Core] 找不到任何店家資訊")
                return None
                
            logger.info(f"[Core] 共找到 {total_progress} 家店家")
            
            # Process shops
            for index, shop_data in enumerate(all_shop_data[:self.catch_limit], start=1):
                self._process_single_shop(shop_data, index, total_progress)
                
                break
                
            execution_time = time.time() - start_time
            logger.info(f"[Core] 抓取 {search_query} 的店家資訊完成, 共花費 {execution_time:.2f} 秒")
            
        except Exception as e:
            logger.error(f"[Core] 處理過程發生錯誤: {str(e)}")
            raise
