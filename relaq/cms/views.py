from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.utils import APIUtils
from core.constants import ResponseCode
from cms.serializers.requests import (
    ArticleFilterSerializer,
    ShopFilterSerializer,
)
from cms.serializers.response import HomePageResponseSerializer
from cms.models import (
    HomePageBanner,
    Article,
)
from cms.serializers.objs import ArticleObjSerializer

class HomePageBannerAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="獲取首頁數據",
        operation_description="獲取首頁 Banner 和最新文章",
        responses={
            200: openapi.Response(
                description="成功",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'code': openapi.Schema(type=openapi.TYPE_INTEGER, description="狀態碼"),
                        'msg': openapi.Schema(type=openapi.TYPE_STRING, description="狀態消息"),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'banner': openapi.Schema(type=openapi.TYPE_STRING, description="Banner 圖片 URL"),
                                'articles': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                            'thumbnail': openapi.Schema(type=openapi.TYPE_STRING),
                                            'title': openapi.Schema(type=openapi.TYPE_STRING),
                                            'description': openapi.Schema(type=openapi.TYPE_STRING),
                                            'update_time': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                                        }
                                    )
                                )
                            }
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="找不到 Banner",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'code': openapi.Schema(type=openapi.TYPE_INTEGER, description="狀態碼"),
                        'msg': openapi.Schema(type=openapi.TYPE_STRING, description="狀態消息"),
                        'data': openapi.Schema(type=openapi.TYPE_OBJECT, properties={})
                    }
                )
            )
        }
    )
    def get(self, request: Request) -> Response:
        """獲取首頁數據：Banner 和最新文章"""
        # 獲取首頁 Banner
        banner = HomePageBanner.objects.first()
        if not banner:
            return APIUtils.gen_response(
                ResponseCode.NO_DATA,
                msg="找不到 Banner 圖片"
            )
        
        # 獲取最新三篇文章
        articles = Article.objects.order_by("-created_at")[:3]
        
        # 序列化數據
        articles_data = ArticleObjSerializer(articles, many=True).data
        
        # 構建響應
        response_data = {
            "banner": banner.image_path,
            "articles": articles_data
        }
        
        return APIUtils.gen_response(ResponseCode.SUCCESS, data=response_data)
        
    
    
class ArticleFilterAPIView(GenericAPIView):
    serializer_class = ArticleFilterSerializer

    def post(self, request: Request) -> Response:
        ...
        
        
# class ArticleAPIView(GenericAPIView):
#     serializer_class = ArticleSerializer

#     def post(self, request: Request) -> Response:
#         ...


# class ShopFilterAPIView(GenericAPIView):
#     serializer_class = ShopFilterSerializer

#     def post(self, request: Request) -> Response:
#         ...


# class ShopAPIView(GenericAPIView):
#     serializer_class = ShopSerializer

#     def post(self, request: Request) -> Response:
#         ...