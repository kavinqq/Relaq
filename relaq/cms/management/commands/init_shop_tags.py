from django.core.management.base import BaseCommand
from cms.models import ShopTag, ShopTagType


class Command(BaseCommand):
    help = '初始化店家標籤資料'

    def handle(self, *args, **options):
        # 定義初始資料
        tag_data = {
            ShopTagType.STYLE: [
                {
                    "name": "自然風",
                    "description": "裸色、透明、清新、淡雅",
                    "emoji": "🌿",
                },
                {
                    "name": "優雅風",
                    "description": "法式、漸層",
                    "emoji": "🎀",
                },
                {
                    "name": "華麗風",
                    "description": "金箔、鑽飾、大理石紋",
                    "emoji": "💎",
                },
                {
                    "name": "可愛風",
                    "description": "卡通圖案、粉色系、甜美彩繪",
                    "emoji": "🍭",
                },
                {
                    "name": "個性風",
                    "description": "幾何圖形、撞色、大膽設計",
                    "emoji": "🔹",
                },
                {
                    "name": "季節風",
                    "description": "提供特定季節主題美甲（如櫻花、雪花、夏日水果等）",
                    "emoji": "🍂",
                },
                {
                    "name": "多元風格",
                    "description": "提供多種風格選擇，設計彈性大",
                    "emoji": "✨",
                },
            ],
            ShopTagType.TECHNIQUE: [
                {
                    "name": "基礎修甲",
                    "description": "剪指甲、修型、死皮處理",
                    "emoji": "🏡",
                },
                {
                    "name": "單色光療",
                    "description": "凝膠甲、純色塗抹",
                    "emoji": "💅",
                },
                {
                    "name": "彩繪設計",
                    "description": "手繪圖案、花卉、符號",
                    "emoji": "🎨",
                },
                {
                    "name": "漸層美甲",
                    "description": "手繪漸層、噴霧漸層",
                    "emoji": "🌈",
                },
                {
                    "name": "3D裝飾",
                    "description": "立體雕花、金屬片、鑽飾",
                    "emoji": "💎",
                },
                {
                    "name": "水晶/延長甲",
                    "description": "水晶指甲、凝膠延長",
                    "emoji": "🔮",
                },
                {
                    "name": "光療指甲",
                    "description": "UV 固化美甲",
                    "emoji": "🌟",
                },
                {
                    "name": "指甲修復",
                    "description": "甲片修補、破甲護理",
                    "emoji": "🏥",
                },
                {
                    "name": "美睫服務",
                    "description": "睫毛嫁接、補睫毛、睫毛護理",
                    "emoji": "👀",
                },
            ],
            ShopTagType.PRICE: [
                {
                    "name": "經濟實惠",
                    "description": "基礎款式價格親民，新客優惠多",
                    "emoji": "💰",
                },
                {
                    "name": "高級訂製",
                    "description": "提供獨家設計，材料與手工細節精緻",
                    "emoji": "💎",
                },
                {
                    "name": "奢華尊享",
                    "description": "頂級客製設計，進口材料、高端服務",
                    "emoji": "👑",
                },
                {  
                    "name": "多價位選擇",
                    "description": "提供從基礎到高端不同價位的方案",
                    "emoji": "💳",
                },
            ],
            ShopTagType.ENVIRONMENT: [
                {
                    "name": "溫馨小巧",
                    "description": "空間精緻，氣氛放鬆",
                    "emoji": "🌿",
                }, 
                {
                    "name": "高級舒適",
                    "description": "裝潢高級，設備舒適（如按摩椅）",
                    "emoji": "💎",
                },
                {
                    "name": "明亮簡約",
                    "description": "空間乾淨整潔，風格簡約清新",
                    "emoji": "🌞",
                },
                {
                    "name": "隱密包廂",
                    "description": "提供獨立空間，適合私人放鬆",
                    "emoji": "🏡",
                },
                {
                    "name": "可愛寵物友善",
                    "description": "有貓咪或店內可帶寵物",
                    "emoji": "🐱",
                },
            ],
            ShopTagType.TRANSPORTATION: [
                {
                    "name": "捷運站旁",
                    "description": "步行 5 分鐘內可達捷運站",
                    "emoji": "🚇",
                },
                {
                    "name": "停車方便",
                    "description": "附近有停車場或好停車",
                    "emoji": "🚗",
                },
                {
                    "name": "交通便利",
                    "description": "公車、捷運、機車皆方便",
                    "emoji": "📍",
                },
            ],
            ShopTagType.TARGET_AUDIENCE: [
                {
                    "name": "學生族",   
                    "description": "價格親民，款式耐用",
                    "emoji": "🎓",
                },
                {
                    "name": "上班族",
                    "description": "低調時尚、簡約大方",
                    "emoji": "👩‍💼",
                },
                {
                    "name": "新娘族",
                    "description": "婚禮專屬美甲、美睫設計",
                    "emoji": "👰",
                },
                {
                    "name": "潮流控",
                    "description": "個性前衛、獨特款式多",
                    "emoji": "🔥",
                },
                {
                    "name": "少女系",
                    "description": "可愛粉色、甜美系設計多",
                    "emoji": "🎀",
                },
            ],
        }
        
        
        bulk_create_list = []
        
        for tag_type, tags in tag_data.items():
            for tag in tags:
                bulk_create_list.append(ShopTag(**tag, type=tag_type))
        
        ShopTag.objects.bulk_create(bulk_create_list)
        
        
        
        self.stdout.write(self.style.SUCCESS('初始化店家標籤資料完成'))
