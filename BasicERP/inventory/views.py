from django.shortcuts import render
import base64
from http import HTTPStatus
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from itertools import zip_longest
from .forms import MaterialInventoryForm, MerchantForm, MerchantMaterialsForm, MaterialsOnOrderForm
from .models import MaterialInventory, Merchant, MerchantMaterials, MaterialsOnOrder
from .quieries import (
    get_all_inventory, get_inventory_by_code, material_exists)


# Create your views here.
# Create your views here.
@login_required
def index(request):
    materials = get_all_inventory()
    return render(request, "all_inventory.html", {"material": materials})


@login_required
def view_all_inventory(request):
    materials = get_all_inventory()
    return render(request, "all_inventory.html", {"material": materials})


@login_required
def edit_material(request):
    view_all_inventory()


@login_required
def view_by_material_code(request):

    if request.method == "POST":
        material_code = request.POST.get('material_code')
        Exists = material_exists(material_code)

        if Exists:
            material = get_inventory_by_code(material_code)
            return render(request, "view_material.html", {"material": material})
        else:
            return render(request, "input_materialcode.html", {'Error': 'material not exists'})


@login_required
def get_material_code(request):
    return render(request, "input_materialcode.html")


@login_required
def update_inventory(request, material_code):
    material_data = get_all_inventory(material_code)
    if request.method == "POST":
        MaterialInventory_form = MaterialInventoryForm(
            request.post, instance=material_data)
        if request.POST.get("update_inventory"):
            if (MaterialInventoryForm.is_valid):
                material_data = MaterialInventoryForm.save()
                material_data.save()
                messages.success(
                    request, "Inventory material Updated Successfully")
                return redirect("/")
        elif request.POST.get("archive_material"):
            archive_material(material_data)
            messages.success(request, "Inventory material archived")
    return render(request, "inventory/update_inventory.html", material=material_data)


@login_required
def remove_inventory(request):
    inventory = get_all_inventory()
    return render(request, "/index.html", {"inventory": inventory})


@login_required
def create_material(request):
    material = MaterialInventory()
    material_form = MaterialInventoryForm(instance=material)
    if request.method == "POST":
        material_form = MaterialInventoryForm(request.POST)

        if(MaterialInventoryForm.is_valid):
            material = material_form.save()
            material.save()
            messages.success(
                request, "Inventory material Updated Successfully")
            return redirect("/inventory/create_material")
    return render(request, "create_material.html", {'form': material_form})


login_required


def create_merchant(request):
    merchant = Merchant()
    merchant_form = MerchantForm(instance=merchant)
    if request.method == "POST":
        merchant_form = MerchantForm(request.POST)

        if(MerchantForm.is_valid):
            merchant = merchant_form.save()
            merchant.save()
            messages.success(
                request, "merchant was create Successfully")
            return redirect("/inventory/create_merchant")
    return render(request, "create_merchant.html", {'form': merchant_form})


def add_material_to_merchant(request):
    merchantmaterial = MerchantMaterials()
    merchantmaterial_form = MerchantMaterialsForm(instance=merchantmaterial)
    if request.method == "POST":
        merchantmaterial_form = MerchantMaterialsForm(request.POST)

        if(MerchantMaterialsForm.is_valid):
            merchantmaterial = merchantmaterial_form.save()
            merchantmaterial.save()
            messages.success(
                request, "material added to merchant Successfully")
            return redirect("/inventory/add_material_to_merchant.html")

    return render(request, "add_material_to_merchant.html", {'form': merchantmaterial_form})


def create_material_order(request):
    meterialsonorder = MaterialsOnOrder()
    meterialsonorder_form = MaterialsOnOrderForm(instance=meterialsonorder)
    if request.method == "POST":
        meterialsonorder_form = MaterialsOnOrderForm(request.POST)

        if(MaterialsOnOrderForm.is_valid):
            meterialsonorder = meterialsonorder_form.save()
            meterialsonorder.save()
            messages.success(
                request, "material added to merchant Successfully")
            return redirect("/inventory/create_merchant_order.html")

    return render(request, "create_material_order.html", {'form': meterialsonorder_form})
