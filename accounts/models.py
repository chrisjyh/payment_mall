from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# 커스텀 유저모델을 위해 기존 유저모델 상속 자세한내용을 원하면 AbstractUser 컨트롤 클릭
class User(AbstractUser):
    pass