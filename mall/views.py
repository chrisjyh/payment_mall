from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from mall.models import Product, CartProduct
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.forms import modelformset_factory
from .forms import CartProductForm
from django.views.decorators.http import require_POST
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
    queryset = Product.objects.filter(status=Product.Status.ACTIVE).select_related("category")
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

@login_required
def cart_detail(request):
    # select_related를 안하게 되면 조회를 여러번하기때문에 조인을 해서 쿼리조회를 최소화
    cart_product_qs = (CartProduct.objects.filter(
        user=request.user,
    )
    .select_related("product")
    # 이름기준으로 오름차순 
    .order_by("product__name")                  
    )
    
    # 장바구니의 수정 폼셋 설정
    CartProductFormSet = modelformset_factory(
        model=CartProduct,
        form=CartProductForm,
        # 추가적인 줄 필요 x
        extra=0,
        # 삭제 가능
        can_delete=True, 
    )
    if request.method == "POST":
        formset = CartProductFormSet(
            data=request.POST,
            # 상단에 정의된 쿼리 가져옴
            queryset=cart_product_qs,  
        )
        if formset.is_valid():
            formset.save()
            messages.success(request, "장바구니가 수정되었습니다.")
            return redirect("cart_detail")
    else:
        formset = CartProductFormSet(
            queryset=cart_product_qs,
        )
    
    
    return render(request, "mall/cart_detail.html",{
        "formset": formset,
    })

@login_required
@require_POST
# 장바구니에 상품 추가 하는 기능
def add_to_cart(request, product_pk):
    request.user
    # 상품상태가 ACTIVE인 상태를 조회
    product_qs = Product.objects.filter(
        status=Product.Status.ACTIVE
    )
    product = get_object_or_404(product_qs, pk=product_pk)
    quantity = int(request.GET.get("quantity",1))
    
    cart_product, is_created = CartProduct.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": quantity},
    )
    
    if not is_created:
        cart_product.quantity += quantity
        cart_product.save()
    
    # messages.success(request, "장바구니에 추가했습니다.")
    
    # 장바구니 추가될시 페이지가 초기화면으로 이동하는 문제
    # redirect_url = request.META.get("HTTP_REFERER", "product_list")
    # return redirect(redirect_url)
    return HttpResponse("ok")