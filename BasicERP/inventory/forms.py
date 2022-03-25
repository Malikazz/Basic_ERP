from django import forms
from django.forms import ModelForm
from .models import MaterialInventory, Merchant,  MerchantMaterials, MaterialsOnOrder
from tinymce.widgets import TinyMCE
from django.forms import CharField, HiddenInput, ModelForm
from django import forms
from django.contrib.auth.models import Group


# class materialInventoryForm(forms.Form):
#units_available = forms.IntegerField()
#units_reserved_for_orders = forms.IntegerField()
#units_defective = forms.IntegerField()
#total_units_on_order = forms.IntegerField()


class MaterialInventoryForm(ModelForm):
    class Meta:
        model = MaterialInventory
        fields = [
            "name",
            "material_code",
            "description",
            "unit_measurement",
            "units_available",
            "units_reserved_for_orders",
            "units_defective",
            "total_units_on_order",
        ]
        widgets = {
            "description": TinyMCE(attrs={"cols": 80, "rows": 20}),
        }


class MerchantForm(ModelForm):
    class Meta:
        model = Merchant
        fields = [
            "merchant_code",
            "company_name",
            "contact_name",
            "contact_email",
            "contact_number",
            "address",
        ]


class MerchantMaterialsForm(ModelForm):
    class Meta:
        model = MerchantMaterials
        fields = [
            "material_id",
            "merchant_id",
            "unit_cost",
            "avg_order_processing_time",
            "merchant_material_code",
            "merchant_unit_measurement"
        ]


class MaterialsOnOrderForm(ModelForm):
    class Meta:
        model = MaterialsOnOrder
        fields = [
            "MaterialsOnOrder",
            "order_id",
            "units_on_order",
        ]
