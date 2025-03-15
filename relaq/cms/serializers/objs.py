from rest_framework import serializers
from cms.models import Article, Shop


class ArticleObjSerializer(serializers.ModelSerializer):
    preview_content = serializers.CharField()
    update_time = serializers.DateTimeField(
        source="updated_at",
        format="%Y-%m-%d",
    )
    
    class Meta:
        model = Article
        fields = ['id', 'thumbnail', 'title', 'preview_content', 'update_time']
        ref_name = "article_obj"
    

class ShopListObjSerializer(serializers.ModelSerializer):
    pictures = serializers.SerializerMethodField()
    
    class Meta:
        model = Shop
        fields = ['id', 'name', 'address', 'price_min', 'pictures']
        ref_name = "shop_list_obj"
    
        
    def get_pictures(self, obj: Shop):
        pictures = obj.photos.all()
        return [picture.image_path for picture in pictures]
    
    
    
class ShopObjSerializer(ShopListObjSerializer):    
    class Meta(ShopListObjSerializer.Meta):
        fields = ShopListObjSerializer.Meta.fields + [
            'phone',
            'business_hours',
            'price_range',
            'core_features',
            'review_summary',
            'recommended_uses'
        ]
        ref_name = "shop_obj"

    