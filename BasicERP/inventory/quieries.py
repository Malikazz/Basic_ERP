from typing import List, Dict, Tuple
from xmlrpc.client import boolean
from .models import MaterialInventory, MerchantMaterials, Merchant
from django.db.models import Q
from django.db import transaction


def get_all_inventory() -> list:
    all_inventory = MaterialInventory.objects.all()
    return all_inventory


def get_inventory_by_code(request_material_code) -> list:
    material = list(
        MaterialInventory.objects.filter(material_code=request_material_code)
    )
    return material


def material_exists(request_material_code) -> boolean:
    returncode = MaterialInventory.objects.filter(
        material_code=request_material_code).exists()
    return returncode
