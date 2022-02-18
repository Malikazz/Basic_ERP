from django.forms import ModelForm
from django import forms
from .models import Order, OrderDocument, OrderImage
from tinymce.widgets import TinyMCE


class DateInput(forms.DateInput):
    input_type = "date"


## Most basic implementaion of a model form
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            "order_name",
            "customer",
            "order_materials",
            "order_process",
            "due_date",
            "po_number",
            "notes",
        ]
        widgets = {
            "due_date": DateInput(),
            "notes": TinyMCE(attrs={"cols": 80, "rows": 20}),
        }


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
