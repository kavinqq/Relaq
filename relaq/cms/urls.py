from django.urls import path
from cms.views import HomePageBannerAPIView

app_name = 'cms'

urlpatterns = [
    path('api/homepage/', HomePageBannerAPIView.as_view(), name='homepage'),
]
