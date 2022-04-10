import base64
from http import HTTPStatus
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .quieries import (
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
)
from .notifications import new_order_email
from .models import ApplicationSettings, Order, OrderDocument, OrderImage
from itertools import zip_longest
from .forms import OrderForm, OrderImageForm, OrderDocumentForm

# Create your views here.
@login_required
def index(request):
    new_order_email(Order.objects.get(pk=1), request)
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
    context = {
        "customer": customer,
        "order": order,
        "order_images": order_images,
        "order_documents": order_documents,
        "order_creator": order.order_creator,
    }
    return render(request, "dashboard/view_order.html", context=context)
