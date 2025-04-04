from django.core.paginator import Paginator
from django.db.models import Q, QuerySet, F
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
    ArticleListRespSerializer,
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
        operation_description="獲取文章列表，支持分頁",
        request_body=ArticleListReqSerializer,
        responses={
            HTTP_200_OK: openapi.Response(
                description="成功",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'code': openapi.Schema(type=openapi.TYPE_STRING, description="響應代碼"),
                        'msg': openapi.Schema(type=openapi.TYPE_STRING, description="響應消息"),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER, description="總頁數"),
                                'total_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="總記錄數"),
                                'items': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="文章ID"),
                                            'thumbnail': openapi.Schema(type=openapi.TYPE_STRING, description="文章縮圖URL"),
                                            'title': openapi.Schema(type=openapi.TYPE_STRING, description="文章標題"),
                                            'update_time': openapi.Schema(type=openapi.TYPE_STRING, description="更新時間，格式：YYYY-MM-DD"),
                                            'preview_content': openapi.Schema(type=openapi.TYPE_STRING, description="文章預覽內容")
                                        }
                                    )
                                )
                            }
                        )
                    }
                )
            )
        },
        tags=["文章"]
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        articles = Article.objects.all().order_by("-created_at")
        articles_data = ArticleListRespSerializer(articles, many=True).data

        paginator = Paginator(
            object_list=articles_data,
            per_page=serializer.validated_data.get("page_size")
        )
        articles = paginator.page(serializer.validated_data.get("page"))

        return APIUtils.gen_response(
            ResponseCode.SUCCESS,
            data={
                "total_pages": paginator.num_pages,
                "total_count": paginator.count,
                "items": articles.object_list
            }
        )


class ArticleAPIView(GenericAPIView):
    serializer_class = ArticleReqSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="文章詳情",
        operation_description="文章詳情",
        request_body=ArticleReqSerializer,
        responses={
            HTTP_200_OK: openapi.Response(
                description="成功",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'code': openapi.Schema(type=openapi.TYPE_STRING, description="響應代碼"),
                        'msg': openapi.Schema(type=openapi.TYPE_STRING, description="響應消息"),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="文章ID"),
                                'thumbnail': openapi.Schema(type=openapi.TYPE_STRING, description="文章縮圖URL"),
                                'title': openapi.Schema(type=openapi.TYPE_STRING, description="文章標題"),
                                'update_time': openapi.Schema(type=openapi.TYPE_STRING, description="更新時間，格式：YYYY-MM-DD"),
                                'created_by': openapi.Schema(type=openapi.TYPE_STRING, description="文章作者"),
                                'content': openapi.Schema(type=openapi.TYPE_STRING, description="文章內容")
                            }
                        )
                    }
                )
            ),
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
        operation_description="獲取店家列表，支持分頁、過濾和排序",
        request_body=ShopListReqSerializer,
        responses={
            HTTP_200_OK: openapi.Response(
                description="成功",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'code': openapi.Schema(type=openapi.TYPE_STRING, description="響應代碼"),
                        'msg': openapi.Schema(type=openapi.TYPE_STRING, description="響應消息"),
                        'data': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER, description="總頁數"),
                                'total_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="總記錄數"),
                                'items': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="店家ID"),
                                            'name': openapi.Schema(type=openapi.TYPE_STRING, description="店家名稱"),
                                            'address': openapi.Schema(type=openapi.TYPE_STRING, description="店家地址"),
                                            'price_min': openapi.Schema(type=openapi.TYPE_INTEGER, description="最低價格"),
                                            'pictures': openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(type=openapi.TYPE_STRING),
                                                description="店家圖片列表"
                                            )
                                        }
                                    )
                                )
                            }
                        )
                    }
                )
            )
        },
        tags=["店家"]
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        shops = self._filter_shops(
            city=validated_data.get("city"),
            township=validated_data.get("township"),
            price_min=validated_data.get("price_min"),
            price_max=validated_data.get("price_max"),
            keyword=validated_data.get("keyword")
        )

        shops = Shop.with_weighted_rating(shops)

        paginator = Paginator(
            object_list=ShopListObjSerializer(shops, many=True).data,
            per_page=validated_data.get("page_size")
        )

        return APIUtils.gen_response(
            ResponseCode.SUCCESS,
            data={
                "total_pages": paginator.num_pages,
                "total_count": paginator.count,
                "items": paginator.page(validated_data.get("page")).object_list
            }
        )

    def _filter_shops(
        self,
        city=None,
        township=None,
        price_min=None,
        price_max=None,
        keyword=None
    ) -> QuerySet[Shop]:
        shops = Shop.objects.all()

        # 地理位置篩選
        if city:
            shops = shops.filter(city__icontains=city)
        if township:
            shops = shops.filter(district__icontains=township)

        # 價格範圍篩選
        if isinstance(price_min, (int, float)):
            shops = shops.filter(price_min__gte=price_min)
        if isinstance(price_max, (int, float)):
            shops = shops.filter(price_max__lte=price_max)

        # 關鍵詞篩選
        if keyword:
            shops = shops.filter(
                Q(reviews__icontains=keyword) |
                Q(core_features__icontains=keyword) |
                Q(review_summary__icontains=keyword) |
                Q(recommended_uses__icontains=keyword)
            )

        return shops





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
