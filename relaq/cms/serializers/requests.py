from rest_framework import serializers
from core.serializers.base import PaginationSerializer
from cms.serializers.objs import ArticleObjSerializer


class ArticleListReqSerializer(PaginationSerializer):    
    class Meta:
        ref_name = "article_list_req"
        
        
class ArticleReqSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        help_text="文章Model ID"
    )
    
    class Meta:
        ref_name = "article_req"
    

class ShopListReqSerializer(PaginationSerializer):
    city = serializers.CharField(
        help_text="縣市",
        required=False
    )
    township = serializers.CharField(
        help_text="鄉鎮",
        required=False
    )
    price_min = serializers.IntegerField(
        help_text="價格最小值",
        required=False
    )
    price_max = serializers.IntegerField(
        help_text="價格最大值",
        required=False
    )
    keyword = serializers.CharField(
        help_text="關鍵字",
        required=False
    )
    
    
    class Meta:
        ref_name = "shop_list_req"
        

class ShopReqSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        help_text="店家Model ID"
    )
    
    class Meta:
        ref_name = "shop_req"