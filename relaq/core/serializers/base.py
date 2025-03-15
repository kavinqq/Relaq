from rest_framework import serializers


class PaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(
        required=False,
        default=1,
        help_text="當前頁面"
    )
    page_size = serializers.IntegerField(
        required=False,
        default=10,
        help_text="每頁數量"
    )
    
    