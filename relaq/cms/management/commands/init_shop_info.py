import pandas as pd
from django.core.management.base import BaseCommand

from cms.models import Shop


class Command(BaseCommand):
    help = "初始化店家資訊"
    
    def handle(self, *args, **options):
        df = pd.read_excel("test_summary2.xlsx")
        
        bulk_create_list = []
        
        for _, row in df.iterrows():
            shop_info: str = row["店家資訊"]
            
            name = shop_info.split("店家名稱: ")[1].split("\n")[0]
            address = shop_info.split("地址: ")[1].split("\n")[0]
            rating = shop_info.split("評分: ")[1].split("\n")[0]
            website = shop_info.split("網站: ")[1].split("\n")[0]
            phone = shop_info.split("店家電話: ")[1].split("\n")[0].replace(" ", "")
            review_count = shop_info.split("總評論數: ")[1].split("\n")[0]
            
            bulk_create_list.append(
                Shop(
                    name=name,
                    address=address,
                    rating=rating,
                    website=website,
                    phone=phone,
                    review_count=review_count,
                    ai_summary=row["AI_summary"],
                )
            )
            
        Shop.objects.bulk_create(bulk_create_list)

        self.stdout.write(self.style.SUCCESS("初始化店家資訊完成"))
            
            
            
            
            