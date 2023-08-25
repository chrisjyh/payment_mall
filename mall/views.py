from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from mall.models import Product
from django.views.generic import ListView

# Create your views here.
# def product_list(request):
#     # select_related 하면 category과 관련된것을 조회해서 데이터를 불러줌
#     product_qs = Product.objects.all().select_related("category")
#     return render(
#         request,
#         "mall/product_list.html",
#         {
#             "product_list": product_qs,       
#         }
#     )
    
# 페이징기능을 장고에서 제공함 listview 
class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all().select_related("category")
    # 페이징 갯수
    paginate_by = 12
    
    # 동적으로 상품을 조회하기 위해
    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        query = self.request.GET.get("query","")
        
        if query:
            qs = qs.filter(name__icontains=query)
        return qs

#  클래스일때 url에서 view로 연결할때
product_list = ProductListView.as_view()