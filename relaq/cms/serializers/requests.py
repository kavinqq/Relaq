from rest_framework import serializers
from core.serializers.base import PaginationSerializer


"""


getArticlesList（取文章列表）
request
page      	number		 當前頁面
response
articles	list<obj>	thumbnail	縮圖連結
		title	文章標題
		description	部分內文
		update_time	上傳時間(date time)




getArticle（取單一文章）
request
id	number		 文章ID
response
articles	list<obj>	thumbnail	縮圖連結
		title	文章標題
		content	文章內文
		update_time	上傳時間(date time)
		writer	作者
"""

class ArticleFilterSerializer(PaginationSerializer):    
    class Meta:
        ref_name = "ArticleFilter"
        
        
class ArticleSerializer(serializers.Serializer):
    ...



"""
getShopsList（取搜尋後的店家清單）
request
location_city	string		縣市
location_township	string		鄉鎮
range_from	string		價格區間（起）
range_to	string		價格區間（迄）
keyword	string		關鍵字
response
shops	list<obj>	name	店家名稱
		address	店家地址
		minimum	最低價格
		pictures	店家照片


getShopInfo（取店家資訊）
request
id	number		 店家ID
response
name	string		店家名稱
address	string		店家地址
phone	string		店家電話
business_hours 	string		營業時間
rating	string		價格區間
pictures	string		店家照片
advantages	string		核心特色
comments	string		評論摘要
recommend	string		推薦用途
"""

class ShopFilterSerializer(PaginationSerializer):
    class Meta:
        ref_name = "ShopFilter"
