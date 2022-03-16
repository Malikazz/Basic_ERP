from typing import List, Dict, Tuple
from .models import MaterialInventory, Material, MerchantMaterials, Merchant
from django.db.models import Q
from django.db import transaction


def get_all_inventory(all_entries: dict) -> None:
    all_entries = MaterialInventory.objects.all()


def get_inventory_by_code(request_material_code) -> list:
    material_data = list(
        Material.objects.filter(material_code=request_material_code)
        .prefetch_related("MaterialInventory", 'MaterialsOnOrder', 'MerchantMaterials', 'Merchant')
    )
    return material_data
