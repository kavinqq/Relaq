from django.contrib import admin
from django.db.models import Count
from django.contrib.admin import SimpleListFilter
from cms.models import (
    Shop,
    ShopTag,
    Article,
    ArticleImage,
    HomePageBanner
)


class HomePageBannerAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    search_fields = ("image_path",)


class ShopAdmin(admin.ModelAdmin):  
    list_display = ("name", "address", "phone", "rating", "review_count", "created_at", "updated_at", "display_tags")
    search_fields = ("name", "address", "phone")
    list_filter = ("rating", "created_at", "updated_at")
    filter_horizontal = ("tags",)
    
    def get_queryset(self, request):
        return Shop.with_weighted_rating(super().get_queryset(request))
    
    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    
    display_tags.short_description = "標籤"


class UsageCountFilter(SimpleListFilter):
    title = '使用數量'
    parameter_name = 'usage_count'

    def lookups(self, request, model_admin):
        return (
            ('0', '未使用'),
            ('1-5', '1-5次'),
            ('6-10', '6-10次'),
            ('11+', '11次以上'),
        )

    def queryset(self, request, queryset):
        queryset = queryset.annotate(usage_count=Count('shops'))
        
        if self.value() == '0':
            return queryset.filter(usage_count=0)
        elif self.value() == '1-5':
            return queryset.filter(usage_count__gte=1, usage_count__lte=5)
        elif self.value() == '6-10':
            return queryset.filter(usage_count__gte=6, usage_count__lte=10)
        elif self.value() == '11+':
            return queryset.filter(usage_count__gte=11)
        return queryset


class ShopTagAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "emoji", "get_usage_count", "created_at", "updated_at")
    search_fields = ("name", "type")
    list_filter = ("type", "created_at", "updated_at", UsageCountFilter)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(usage_count=Count('shops'))
        return queryset
    
    def get_usage_count(self, obj):
        return obj.usage_count
    
    get_usage_count.short_description = "使用數量"
    get_usage_count.admin_order_field = 'usage_count'


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "created_by", "created_at", "updated_at")
    list_filter = ("created_by", "updated_at")
    search_fields = ("content",)
    inlines = [ArticleImageInline]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(Shop, ShopAdmin)
admin.site.register(ShopTag, ShopTagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(HomePageBanner, HomePageBannerAdmin)