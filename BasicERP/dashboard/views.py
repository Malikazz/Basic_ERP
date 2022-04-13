import base64
from django.utils import timezone
from http import HTTPStatus
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .quieries import (
    get_all_merchants,
    get_all_process,
    get_merchant_by_id,
    get_orders_by_user_role,
    create_order_images_from_post,
    create_order_documents_from_post,
    add_images_to_order,
    add_documents_to_order,
    order_change_groups,
    get_new_order_groups,
    archive_order,
    get_order_by_pk,
    get_order_images_documents,
    remove_delete_image,
    get_customer,
    archive_material,
    get_material_by_id,
    get_all_materials,
    get_process_by_id,
    archive_process,
)
from dashboard.models import (
    ApplicationSettings,
    MerchantMaterials,
    Order,
    OrderDocument,
    OrderImage,
    Material,
    Process,
    Merchant,
)
from itertools import zip_longest
from dashboard.forms import (
    MaterialForm,
    MerchantForm,
    OrderForm,
    OrderImageForm,
    OrderDocumentForm,
    ProcessForm,
)


@login_required
def index(request):
    orders_list = get_orders_by_user_role(request.user)
    orders = []
    for order in orders_list:
        order_tags = []
        order_images = []
        order_documents = []
        zipped = zip_longest(
            orders_list[order]["order_tags"],
            orders_list[order]["order_images"],
            orders_list[order]["order_documents"],
        )
        zipped = list(zipped)
        for tag, image, document in zipped:
            if tag is not None and tag.name != "Managing Director":
                order_tags.append(tag.name)
            if image is not None:
                order_images.append(image)
            if document is not None:
                order_documents.append(document)
        orders.append(
            {
                "id": orders_list[order]["order"].id,
                "name": orders_list[order]["order"].order_name,
                "order_tags": order_tags,
                "order_images": order_images,
                "order_documents": order_documents,
                "updated_at": orders_list[order]["order"].updated_at,
                "created_at": orders_list[order]["order"].created_at,
            }
        )
    return render(request, "dashboard/index.html", {"orders": orders})


@login_required
def create_order(request):
    order = Order()
    order.order_creator = request.user
    order_form = OrderForm(instance=order)
    order_document_form = OrderDocumentForm()
    order_image_form = OrderImageForm()

    if request.method == "POST":
        order_form = OrderForm(request.POST)
        order_document_form = OrderDocumentForm(request.POST)
        order_image_form = OrderImageForm(request.POST)
        if (
            order_form.is_valid
            and order_document_form.is_valid
            and order_image_form.is_valid
        ):
            order_documents = []
            image_documents = []
            image_documents = create_order_images_from_post(
                request.FILES.getlist("images")
            )
            order_documents = create_order_documents_from_post(
                request.FILES.getlist("files")
            )
            order = order_form.save()
            add_images_to_order(order, image_documents)
            add_documents_to_order(order, order_documents)
            order.save()
            messages.success(request, "Order Added Successfully")
            return redirect("/")
    return render(
        request,
        "dashboard/create_order.html",
        context={
            "order_form": order_form,
            "image_form": order_image_form,
            "document_form": order_document_form,
        },
    )


@login_required
def edit_order(request, order_id):
    order, images, documents = get_order_images_documents(order_id)
    if request.method == "POST":
        order_form = OrderForm(request.POST, instance=order)
        order_image_form = OrderImageForm(request.POST)
        order_document_form = OrderDocumentForm(request.POST)
        if request.POST.get("update_order"):
            if (
                order_form.is_valid
                and order_document_form.is_valid
                and order_image_form.is_valid
            ):
                order_documents = []
                image_documents = []
                image_documents = create_order_images_from_post(
                    request.FILES.getlist("images")
                )
                order_documents = create_order_documents_from_post(
                    request.FILES.getlist("files")
                )
                order = order_form.save()
                add_images_to_order(order, image_documents)
                add_documents_to_order(order, order_documents)
                order.save()
                messages.success(request, "Order Updated Successfully")
                return redirect("/")
        elif request.POST.get("archive_order"):
            archive_order(order)
            messages.success(request, "Order archived")
    order_form = OrderForm(instance=order)
    order_image_form = OrderImageForm()
    order_document_form = OrderDocumentForm()
    context = {
        "order_form": order_form,
        "order_id": order_id,
        "image_form": order_image_form,
        "document_form": order_document_form,
        "images": images,
        "documents": documents,
    }
    return render(request, "dashboard/edit_order.html", context=context)


@login_required
def remove_image(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        image_id = request.POST.get("image_id")
        remove_delete_image(order_id, image_id)
        return HttpResponse(status=201)
    return HttpResponse(HttpResponseNotAllowed)


@login_required
def remove_document(request):
    if request.method == "POST":
        print(request.POST)
        return HttpResponse(status=201)
    return HttpResponse(HttpResponseNotAllowed)


@login_required
def view_order(request, order_id):
    order, order_images, order_documents = get_order_images_documents(order_id)
    customer = get_customer(order_id)
    materials = list(order.order_materials.all())
    context = {
        "customer": customer,
        "order": order,
        "materials": materials,
        "order_images": order_images,
        "order_documents": order_documents,
        "order_creator": order.order_creator,
    }
    return render(request, "dashboard/view_order.html", context=context)


@login_required
def create_material(request):
    if request.method == "POST":
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Material has been added")
    else:
        form = MaterialForm()
    return render(request, "dashboard/create_material.html", {"form": form})


@login_required
def view_materials(request):
    materials = get_all_materials()
    return render(request, "dashboard/view_materials.html", {"materials": materials})


@login_required
def edit_material(request, material_id):
    try:
        material = get_material_by_id(material_id)
        if request.method == "POST":
            if request.POST.get("update_material"):
                form = MaterialForm(request.POST, instance=material)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Material updated")
                    return redirect("/inventory/")
            elif request.POST.get("archive_material"):
                archive_material(material)
                messages.success(request, "Material Archived")
                return redirect("/inventory/")
        else:
            form = MaterialForm(instance=material)

    except Material.DoesNotExist:
        messages.warning(request, "that material does not exsist")
        return redirect("/inventory/")
    return render(request, "dashboard/edit_material.html", {"form": form})


@login_required
def create_process(request):
    if request.method == "POST":
        form = ProcessForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Process has been added")
    else:
        form = MaterialForm()
    return render(request, "dashboard/create_process.html", {"form": form})


@login_required
def view_processes(request):
    processes = get_all_process()
    return render(request, "dashboard/view_processes.html", {"processes": processes})


@login_required
def edit_process(request, process_id):
    try:
        process = get_process_by_id(process_id)
        if request.method == "POST":
            if request.POST.get("update"):
                form = ProcessForm(request.POST, instance=process)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Process Updated")
                    return redirect("/view-processes/")
            elif request.POST.get("archive"):
                archive_process(process)
                messages.success(request, "Process Archived")
                return redirect("/view-processes/")
        else:
            form = ProcessForm(instance=process)

    except Material.DoesNotExist:
        messages.warning(request, "that prcoess does not exsist")
        return redirect("/view-processes/")
    return render(request, "dashboard/edit_process.html", {"form": form})


@login_required
def create_merchant(request):
    if request.method == "POST":
        form = MerchantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Merchant Created")
            return redirect("/view-merchants/")
    else:
        form = MerchantForm()

    return render(request, "dashboard/create_merchant.html", {"form": form})


@login_required
def edit_merchant(request, merchant_id):
    try:
        merchant = get_merchant_by_id(merchant_id)
        if request.method == "POST":
            form = MerchantForm(request.POST, instance=merchant)
            if request.POST.get("update"):
                if form.is_valid():
                    form.save()
                    messages.success(request, "Merchant updated")
                    return redirect("/view-merchants/")
            elif request.POST.get("archive"):
                ## TODO: finish this
                print("archive merchant")
        else:
            form = MerchantForm(instance=merchant)
    except Merchant.DoesNotExist:
        messages.warning(request, "Merchant does not exsist")
        return redirect("/view-merchants/")
    return render(request, "dashboard/edit_merchant.html", {"form": form})


@login_required
def view_merchants(request):
    merchants = get_all_merchants()
    return render(request, "dashboard/view_merchants.html", {"merchants": merchants})


@login_required
def view_merchant_materials(request, material_id):
    material = get_material_by_id(material_id)
    merchant_materials = list(MerchantMaterials.objects.filter(material=material))
    return render(
        request,
        "dashboard/view_material_merchant.html",
        {"merchant_materials": merchant_materials, "material": material},
    )


def order_report(request):

    current_datetime = timezone.now()
    week = current_datetime.isocalendar()[1]
    weeks_orders = list(Order.objects.filter(created_at__week=week))
    months_orders = list(Order.objects.filter(created_at__month=current_datetime.month))
    weekly_count = len(weeks_orders)
    monthly_count = len(months_orders)
    weekly_completed = 0
    monthly_completed = 0
    for item in weeks_orders:
        if item.archived == True:
            weekly_completed = weekly_completed + 1
    for item in months_orders:
        if item.archived == True:
            monthly_completed = monthly_completed + 1

    return render(
        request,
        "dashboard/order_report.html",
        {
            "week": weekly_count,
            "month": monthly_count,
            "week_done": weekly_completed,
            "month_done": monthly_completed,
        },
    )
