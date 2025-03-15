from rest_framework import serializers
from cms.serializers.objs import ArticleObjSerializer, ShopListObjSerializer
from cms.models import Article

class HomePageResponseSerializer(serializers.Serializer):
    banner = serializers.CharField(
        help_text="首頁Banner大圖URL"
    )
    articles = ArticleObjSerializer(
        help_text="最新文章列表",
        many=True,
    )
    
    class Meta:
        ref_name = "home_page_resp"
        
        
class ArticleRespSerializer(ArticleObjSerializer):
    created_by = serializers.SerializerMethodField()
        
    class Meta(ArticleObjSerializer.Meta):
        ref_name = "article_resp"
        fields = ArticleObjSerializer.Meta.fields + ['created_by']          
        
    def get_created_by(self, obj: Article):
        return obj.created_by.username
