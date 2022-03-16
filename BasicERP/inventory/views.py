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
from .quieries import (get_all_inventory, get_inventory_by_code)


# Create your views here.
# Create your views here.
@login_required
def index(request):
    return render(request, "index.html")


@login_required
def view_all_inventory(request):
    all_entries = {}
    get_all_inventory(all_entries)
    return render(request, "all_inventory.html", {"material": all_entries})


@login_required
def view_by_material_code(request):
    item = get_inventory_by_code()
    return render(request, "inventory/inventory_by_code.html", {"item": item})


@login_required
def update_inventory(request):
    inventory = get_all_inventory()
    return render(request, "dashboard/", {"inventory": inventory})


@login_required
def remove_inventory(request):
    inventory = get_all_inventory()
    return render(request, "dashboard/index.html", {"inventory": inventory})
