from rest_framework import serializers
from cms.models import Article


class ArticleObjSerializer(serializers.ModelSerializer):
    preview_content = serializers.CharField()
    update_time = serializers.DateTimeField(
        source="updated_at",
        format="%Y-%m-%d",
    )
    
    class Meta:
        model = Article
        fields = ['id', 'thumbnail', 'title', 'preview_content', 'update_time']
        ref_name = "ArticleObj"
    
    
class ShopObjSerializer(serializers.Serializer):
    name = serializers.CharField(
        help_text="店家名稱"
    )
    address = serializers.CharField(
        help_text="店家地址"
    )
    min_price = serializers.IntegerField(
        help_text="最低價格"
    )
    pictures = serializers.ListField(
        help_text="店家照片",
        child=serializers.CharField(
            help_text="照片連結"
        )
    )
