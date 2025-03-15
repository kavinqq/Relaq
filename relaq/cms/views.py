from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


class HomePageBannerAPIView(GenericAPIView):
    def get(self, request: Request) -> Response:
        ...
    
    
class ArticleAPIView(GenericAPIView):
    def post(self, request: Request) -> Response:
        ...


class ShopAPIView(GenericAPIView):
    def post(self, request: Request) -> Response:
        ...
