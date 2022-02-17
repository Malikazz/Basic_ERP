from email import message
from black import re
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .quieries import (
    get_orders_by_user_role,
    create_order_images_from_post,
    create_order_documents_from_post,
    add_images_to_order,
    add_documents_to_order,
    order_change_groups,
    get_new_order_groups,
)
from .models import Order, OrderDocument, OrderImage
from itertools import zip_longest
from .forms import OrderForm, OrderImageForm, OrderDocumentForm

# Create your views here.
@login_required
def index(request):
    send_mail(
        "This is a subject",
        "Message",
        "admin@admin.com",
        ["user@user.com"],
        True,
        None,
        None,
        None,
        "<h1>This is a message</h1>",
    )
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
    order_form = OrderForm()
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
            group_list = get_new_order_groups()
            order_change_groups(order, group_list)
            breakpoint()
            order.save()
            ##TODO: After making view order have this route to the view order page with the newly created order
            messages.success(request, "Order Added Successfully")
            return redirect("dashboard/create-order")
    return render(
        request,
        "dashboard/create_order.html",
        context={
            "order_form": order_form,
            "image_form": order_image_form,
            "document_form": order_document_form,
        },
    )
