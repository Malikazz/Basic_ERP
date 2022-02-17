from django.forms import ModelForm
from django import forms
from .models import Order, OrderDocument, OrderImage

## Most basic implementaion of a model form
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["order_name"]


class OrderDocumentForm(forms.Form):
    files = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"multiple": True, "required": False}),
    )


class OrderImageForm(forms.Form):
    images = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"multiple": True, "required": False}),
    )
