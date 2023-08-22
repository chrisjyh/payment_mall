# from typing import Any, Optional
import requests
from django.core.management import BaseCommand
from dataclasses import dataclass, asdict
from django.core.files.base import ContentFile
from mall.models import Category, Product
from tqdm import tqdm

BASE_URL = "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/django-shopping-with-iamport/"

@dataclass
class Item:
    category_name: str
    name: str
    price: int
    priceUnit: str
    desc: str
    photo_path: str


class Command(BaseCommand):
    help = "Load products from JSON file."
    
    def handle(self, *args, **options):
        json_url = BASE_URL + "product-list.json"
        item_dict_list = requests.get(json_url).json()
        
        # for item_dict in item_dict_list:
        #     # **item_dict은 unpack문법   =====  category_name="", name="" 이런식으로해도됨
        #     item = Item(**item_dict)
        #  수정
        item_list = [Item(**item_dict) for item_dict in item_dict_list]
        # 집합은 중복제거 - 카테고리 추출
        category_name_set = {item.category_name for item in item_list}
        
        category_dict = {}
        
        # 카테고리 추출
        for category_name in category_name_set:
            # get_or_create는 첫번째 값은 획득 or 생성한 카테고리 인스턴스
            # 두번째는 생성 여부값
            # 두번째는 안받을 것 그래서 __
           category, __ = Category.objects.get_or_create(name=category_name or "미분류")
           category_dict[category.name] = category
        
        
        #  tqdm 진행사항을 볼수있음
        for item in tqdm(item_list):
            # 타입 까먹을것 같으면 써주기
            category: Category = category_dict[item.category_name or "미분류"]
            product, is_created = Product.objects.get_or_create(
                category=category,
                name=item.name,
                defaults={
                    "description": item.desc,
                    "price": item.price,
                },  
            )
            if is_created:
                # 
                photo_url = BASE_URL + item.photo_path
                filename = photo_url.rsplit("/",1)[-1]
                # 추후 이미지는 링크로 걸고 
                # 이미지 로딩은 cpu계산이 아니라 외부 네트워크 i/o이기 때문에
                # 멀티쓰레딩 코드로 다수의 이미지를 동시에 받도록할예정
                photo_data = requests.get(photo_url).content # raw data
                product.photo.save(
                    name=filename,
                    content=ContentFile(photo_data),
                    save=True,
                )