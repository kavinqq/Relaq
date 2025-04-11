from django.db import models
from django.db.models import F, ExpressionWrapper, FloatField, QuerySet
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

from core.models import TimeStamped


class ShopTagType(models.TextChoices):
    STYLE = ("STYLE", "風格類")
    TECHNIQUE = ("TECHNIQUE", "技術類")
    PRICE = ("PRICE", "價格")
    ENVIRONMENT = ("ENVIRONMENT", "環境氛圍")
    TRANSPORTATION = ("TRANSPORTATION", "交通便利")
    TARGET_AUDIENCE = ("TARGET_AUDIENCE", "目標客群")
    
    
class ShopTag(TimeStamped):
    name = models.CharField(max_length=255)
    description = models.TextField(
        verbose_name="描述",
    )
    emoji = models.CharField(
        max_length=255,
        verbose_name="Emoji",
    )
    type = models.CharField(
        max_length=255,
        choices=ShopTagType.choices,
        verbose_name="類型",
        db_index=True,
    )

    class Meta:
        verbose_name = "店家標籤"
        verbose_name_plural = "店家標籤"
        
    def __str__(self):
        return f"{self.emoji} {self.name}({self.get_type_display()})"


class Shop(TimeStamped):
    name = models.CharField(
        verbose_name="店家名稱",
        max_length=255,
    )
    # 查詢用欄位
    city = models.CharField(
        verbose_name="縣市",
        max_length=20,
        help_text="查詢用，例如：台北市、新北市",
        db_index=True,
        null=True,
        blank=True,
    )
    district = models.CharField(
        verbose_name="行政區",
        max_length=20,
        help_text="查詢用，例如：大安區、中山區",
        db_index=True,
        null=True,
        blank=True,
    )
    # 顯示用欄位
    address = models.TextField(
        verbose_name="完整地址",
        help_text="完整地址，用於前端顯示",
    )
    phone = models.CharField(
        verbose_name="電話",
        max_length=255,
    )
    review_count = models.IntegerField(
        verbose_name="總評論數",
        default=0,
    )
    website = models.URLField(
        verbose_name="官方網站",
        null=True,
        blank=True,
    )
    rating = models.DecimalField(
        verbose_name="評分",
        max_digits=3,
        decimal_places=2,
        default=0,
    )
    reviews = RichTextField(
        verbose_name="評論",
        null=True,
        blank=True,
    )
    price_and_service = RichTextField(
        verbose_name="價格與服務",
        null=True,
        blank=True,
    )    
    core_features = RichTextField(
        verbose_name="核心特色",
        null=True,
        blank=True,
    )    
    review_summary = RichTextField(
        verbose_name="評論摘要",
        null=True,
        blank=True,
    )
    recommended_uses = RichTextField(
        verbose_name="推薦用途",
        null=True,
        blank=True,
    )
    price_min = models.IntegerField(
        verbose_name="最低價格",
        null=True,
        blank=True,
    )
    price_max = models.IntegerField(
        verbose_name="最高價格",
        null=True,
        blank=True,
    )
    business_hours = models.CharField(
        verbose_name="營業時間",
        max_length=255,
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField(
        ShopTag,
        verbose_name="店家標籤",
        related_name="shops",
        blank=True,
    )
    
    photos: models.Manager["ShopPhoto"]
    
    @property
    def price_range(self) -> str:
        if self.price_min and self.price_max:
            return f"{self.price_min} - {self.price_max}"
        else:
            return "沒有價格資訊"
        
    @classmethod
    def with_weighted_rating(cls, queryset: QuerySet["Shop"]):
        """
        返回按照評分權重（評分 * 評論數）排序的查詢集
        """
        return queryset.annotate(
            weighted_rating=ExpressionWrapper(
                F('rating') * F('review_count'),
                output_field=FloatField()
            )
        ).order_by("-weighted_rating")
    
    class Meta:
        verbose_name = "店家資訊"
        verbose_name_plural = "店家資訊"
        
    def __str__(self):
        return self.name


class ShopPhoto(TimeStamped):
    image_path = models.TextField(
        verbose_name="圖片路徑",
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="photos",
    )

    class Meta:
        verbose_name = "店家照片"
        verbose_name_plural = "店家照片"
        
    def __str__(self):
        return f"{self.shop.name}_photo"


class HomePageBanner(TimeStamped):
    image_path = models.TextField(
        verbose_name="圖片路徑",
    )
    
    class Meta:
        verbose_name = "首頁Banner"
        verbose_name_plural = "首頁Banner"


class Article(TimeStamped):
    thumbnail = models.TextField(
        verbose_name="縮圖路徑",
        null=True,
        blank=True,
    )
    title = models.CharField(
        verbose_name="標題",
        max_length=255,
        null=True,
        blank=True,
    )
    content = RichTextField(
        verbose_name="內容",
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="建立者",
        related_name="articles",
    )
    url = models.URLField(
        verbose_name="網址",
        null=True,
        blank=True,
    )
    
    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
    
    @property
    def preview_content(self) -> str:
        return self.content[:100]
    
    
class ArticleImage(TimeStamped):
    image_path = models.TextField(
        verbose_name="圖片路徑",
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "文章圖片"
        verbose_name_plural = "文章圖片"
