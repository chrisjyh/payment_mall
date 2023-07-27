from .models import Payment
from django import forms

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["name", "amount"] # fix: 텍스트로 모든 필드 입력받음