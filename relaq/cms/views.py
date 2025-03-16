from django.core.paginator import Paginator
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.utils import APIUtils
from core.constants import ResponseCode
from cms.serializers.requests import (
    ArticleListReqSerializer,
    ArticleReqSerializer,
    ShopListReqSerializer,
    ShopReqSerializer,
)
from cms.serializers.response import (
    HomePageResponseSerializer,
    ArticleRespSerializer,
)
from cms.models import (
    HomePageBanner,
    Article,
    Shop,
)
from cms.serializers.objs import (
    ArticleObjSerializer,
    ShopObjSerializer,
    ShopListObjSerializer, 
)
from core.constants import ResponseCode


class HomePageBannerAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_summary="Banner 和最新文章",
        operation_description="Banner 和最新文章",
        responses={
            HTTP_200_OK: HomePageResponseSerializer,
        },
        tags=["首頁"]
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
        
    
    
class ArticleListAPIView(GenericAPIView):
    serializer_class = ArticleListReqSerializer
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary="文章列表",
        operation_description="文章列表",
        request_body=ArticleListReqSerializer,
        responses={
            HTTP_200_OK: ArticleObjSerializer(many=True),
        },
        tags=["文章"]
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        page = serializer.validated_data.get("page")
        page_size = serializer.validated_data.get("page_size")
        
        articles = Article.objects.order_by("-created_at")
        paginator = Paginator(articles, page_size)
        articles = paginator.page(page)
        
        articles_data = ArticleObjSerializer(articles, many=True).data
        
        return APIUtils.gen_response(ResponseCode.SUCCESS, data=articles_data)
        
        
        
        
class ArticleAPIView(GenericAPIView):
    serializer_class = ArticleReqSerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_summary="文章詳情",
        operation_description="文章詳情",
        request_body=ArticleReqSerializer,
        responses={
            HTTP_200_OK: ArticleRespSerializer,
            HTTP_404_NOT_FOUND: openapi.Response(
                description="找不到文章",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'code': openapi.Schema(type=openapi.TYPE_STRING, description="狀態碼"),
                        'msg': openapi.Schema(type=openapi.TYPE_STRING, description="錯誤消息"),
                        'data': openapi.Schema(type=openapi.TYPE_OBJECT, description="無數據", nullable=True)
                    }
                ),
                examples={
                    "application/json": {
                        "code": ResponseCode.NO_DATA.code,
                        "msg": "找不到文章",
                        "data": None
                    }
                }
            )
        },
        tags=["文章"]
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        article_id = serializer.validated_data.get("id")
        
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return APIUtils.gen_response(
                ResponseCode.NO_DATA,
                msg="找不到文章",
                status=HTTP_404_NOT_FOUND
            )
        
        article_data = ArticleRespSerializer(article).data
        
        return APIUtils.gen_response(ResponseCode.SUCCESS, data=article_data)


class ShopListAPIView(GenericAPIView):
    serializer_class = ShopListReqSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="店家列表",
        operation_description="店家列表",
        request_body=ShopListReqSerializer,
        responses={
            HTTP_200_OK: ShopListObjSerializer(many=True),    
        },
        tags=["店家"]
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        city = serializer.validated_data.get("city")
        township = serializer.validated_data.get("township")
        price_min = serializer.validated_data.get("price_min")
        price_max = serializer.validated_data.get("price_max")
        keyword = serializer.validated_data.get("keyword")
        page = serializer.validated_data.get("page")
        page_size = serializer.validated_data.get("page_size")
        
        shops = Shop.objects.filter()
        shops_data = ShopListObjSerializer(shops, many=True).data
        
        return APIUtils.gen_response(ResponseCode.SUCCESS, data=shops_data)


class ShopAPIView(GenericAPIView):
    serializer_class = ShopReqSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="店家詳情",
        operation_description="店家詳情",
        request_body=ShopReqSerializer,
        responses={
            HTTP_200_OK: ShopObjSerializer,
            HTTP_404_NOT_FOUND: openapi.Response(
                description="找不到店家",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'code': openapi.Schema(type=openapi.TYPE_STRING, description="狀態碼"),
                        'msg': openapi.Schema(type=openapi.TYPE_STRING, description="錯誤消息"),
                        'data': openapi.Schema(type=openapi.TYPE_OBJECT, description="無數據", nullable=True)
                    }
                ),
                examples={
                    "application/json": {
                        "code": ResponseCode.NO_DATA.code,
                        "msg": "找不到店家",
                        "data": None
                    }
                }
            )
        },
        tags=["店家"]
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        shop_id = serializer.validated_data.get("id")
        
        try:
            shop = Shop.objects.get(id=shop_id)
        except Shop.DoesNotExist:
            return APIUtils.gen_response(
                ResponseCode.NO_DATA,
                msg="找不到店家",
                status=HTTP_404_NOT_FOUND
            )
        
        shop_data = ShopObjSerializer(shop).data
        
        return APIUtils.gen_response(ResponseCode.SUCCESS, data=shop_data)
