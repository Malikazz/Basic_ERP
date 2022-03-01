from django.forms import ModelForm
from django import forms
from .models import Order, OrderDocument, OrderImage
from django.contrib.auth.models import Group
from tinymce.widgets import TinyMCE


class DateInput(forms.DateInput):
    input_type = "date"


## Most basic implementaion of a model form
class OrderForm(ModelForm):
    def clean(self):
        self.cleaned_data = super().clean()
        managing_group = Group.objects.filter(name="Managing Director")
        ## always keeps managing_group in the order tags regardless of choices
        if list(managing_group)[0] not in list(self.cleaned_data["order_tags"]):
            self.cleaned_data["order_tags"] = (
                self.cleaned_data["order_tags"] | managing_group
            )

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
            "order_tags",
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
