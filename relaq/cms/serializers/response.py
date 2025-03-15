from rest_framework import serializers
from cms.serializers.objs import ArticleObjSerializer


class HomePageResponseSerializer(serializers.Serializer):
    banner = serializers.CharField(
        help_text="首頁Banner大圖URL"
    )
    articles = ArticleObjSerializer(
        help_text="最新文章列表",
        many=True,
    )
