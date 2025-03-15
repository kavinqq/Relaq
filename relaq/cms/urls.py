from django.urls import path, include   
from cms.views import (
    HomePageBannerAPIView,
    ArticleListAPIView,
    ArticleAPIView,
    ShopListAPIView,
    ShopAPIView,
)

app_name = 'cms'


api_patterns = [
    path('homepage/', HomePageBannerAPIView.as_view(), name='homepage'),
    path('article_list/', ArticleListAPIView.as_view(), name='article_list'),
    path('article/', ArticleAPIView.as_view(), name='article'),
    path('shop_list/', ShopListAPIView.as_view(), name='shop_list'),
    path('shop/', ShopAPIView.as_view(), name='shop'),
]


urlpatterns = [
    path('api/', include(api_patterns)),
]
