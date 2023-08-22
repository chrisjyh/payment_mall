from django.contrib import admin
from .models import Category, Product
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    list_display_links = ["name"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # where or 조건으로 데이터베이스 select 함
    search_fields = ["name"]
    # 알아서 조인도해줌
    list_display = ["category", "name", "price", "status"]
    list_display_links = ["name"]
    list_filter = ["category", "status", "created_at"]
    date_hierarchy = "updated_at"
    actions = ["make_active","make_INACTIVE"]
    
    @admin.display(description=f"지정상품을 {Product.Status.ACTIVE.label}로 변경합니다.")
    def make_active(self, request, queryset):
        count = queryset.update(status=Product.Status.ACTIVE)
        self.message_user(request, f"{count}개의 상품을 {Product.Status.ACTIVE.label}상태로 변경하였습니다.")
            
    @admin.display(description=f"지정상품을 {Product.Status.INACTIVE.label}로 변경합니다.")
    def make_INACTIVE(self, request, queryset):
        count = queryset.update(status=Product.Status.INACTIVE)
        self.message_user(request, f"{count}개의 상품을 {Product.Status.INACTIVE.label}상태로 변경하였습니다.")