from django.db import models

# Create your models here.

# 상품 분류 모델
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = verbose_name_plural = "상품 분류"


# 상품에 대한 정보
# 
class Product(models.Model):
    
    class Status(models.TextChoices):
        ACTIVE = "a", "정상"
        SOLD_OUT = "s", "품절"
        OBSOLETE = "o", "단종"
        INACTIVE = "i", "비활성화"
        
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    price = models.PositiveBigIntegerField() # 0포함
    status = models.CharField(
        choices= Status.choices, default=Status.INACTIVE, max_length=1
    )
    # imagefield는 pillow 설치해야함 의존성있어서
    photo = models.ImageField(
        upload_to="mall/product/photo/%Y/%m/%d",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"<{self.pk}> {self.name}"
    class Meta:
        verbose_name = verbose_name_plural = "상품"
        # pk기준으로 내림차순, default 설정
        ordering = ["-pk"]
    