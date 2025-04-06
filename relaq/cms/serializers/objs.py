from rest_framework import serializers
from cms.models import Article, Shop


class ArticleObjSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        label="ID",
        help_text="文章唯一識別碼"
    )
    thumbnail = serializers.CharField(
        label="縮圖",
        help_text="文章縮圖URL"
    )
    title = serializers.CharField(
        label="標題",
        help_text="文章標題"
    )
    update_time = serializers.DateTimeField(
        source="updated_at",
        format="%Y-%m-%d",
        label="更新時間",
        help_text="文章最後更新時間，格式：YYYY-MM-DD"
    )
    
    class Meta:
        model = Article
        fields = ['id', 'thumbnail', 'title', 'update_time']
        ref_name = "article_obj"
    

class ShopListObjSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        label="ID",
        help_text="店家Model ID"
    )
    name = serializers.CharField(
        label="名稱",
        help_text="店家名稱"
    )
    address = serializers.CharField(
        label="地址",
        help_text="店家完整地址"
    )
    price_min = serializers.IntegerField(
        label="最低價格",
        help_text="店家最低消費價格"
    )
    pictures = serializers.SerializerMethodField(
        label="圖片",
        help_text="店家圖片列表"
    )
    
    class Meta:
        model = Shop
        fields = ['id', 'name', 'address', 'price_min', 'pictures']
        ref_name = "shop_list_obj"
    
        
    def get_pictures(self, obj: Shop):
        pictures = obj.photos.all()
        return [picture.image_path for picture in pictures]
    
    
    
class ShopObjSerializer(ShopListObjSerializer):    
    phone = serializers.CharField(
        label="電話",
        help_text="店家聯絡電話"
    )
    business_hours = serializers.CharField(
        label="營業時間",
        help_text="店家營業時間"
    )
    price_range = serializers.CharField(
        label="價格範圍",
        help_text="店家價格範圍，例如：500-1000"
    )
    core_features = serializers.CharField(
        label="核心特色",
        help_text="店家核心特色描述"
    )
    review_summary = serializers.CharField(
        label="評論摘要",
        help_text="店家評論摘要"
    )
    recommended_uses = serializers.CharField(
        label="推薦用途",
        help_text="店家推薦用途"
    )
    tags = serializers.SerializerMethodField(
        label="標籤",
        help_text="店家標籤列表"
    )
    
    
    class Meta(ShopListObjSerializer.Meta):
        fields = ShopListObjSerializer.Meta.fields + [
            'phone',
            'business_hours',
            'price_range',
            'core_features',
            'review_summary',
            'recommended_uses',
            'tags'
        ]
        ref_name = "shop_obj"
    
    def get_tags(self, obj: Shop):
        return [tag.name for tag in obj.tags.all()]
    