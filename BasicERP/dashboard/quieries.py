from typing import List, Dict
from .models import Order, OrderDocument, OrderTag, OrderImage
from django.contrib.auth.models import User
from django.db.models import Q


def _get_order_and_related_data(user: User, orders: dict) -> None:

    order_list = list(
        Order.objects.filter(~Q(order_tags__name="Archive"))
        .prefetch_related("order_documents")
        .prefetch_related("order_images")
        .prefetch_related("order_tags")
    )
    for item in order_list:
        order_documents = list(item.order_documents.all())
        order_images = list(item.order_images.all())
        order_tags = list(item.order_tags.all())
        orders["order_" + str(item.id)] = {
            "order": item,
            "order_documents": order_documents,
            "order_image": order_images,
            "order_tags": order_tags,
        }


def get_orders_by_user_role(user: User) -> Dict[str, Dict[str, object]]:
    orders = {}
    user_groups = get_all_users_groups(user)
    if "Managing Director" in user_groups:
        _get_order_and_related_data(user, orders)
    if "Inventory Manager" in user_groups:
        _get_order_and_related_data(user, orders)
    if "Production Manager" in user_groups:
        _get_order_and_related_data(user, orders)
    if "Sales" in user_groups:
        _get_order_and_related_data(user, orders)
    if "Production Staff" in user_groups:
        _get_order_and_related_data(user, orders)
    if "Designer" in user_groups:
        _get_order_and_related_data(user, orders)

    return orders


def get_all_users_groups(user: User) -> List:
    group_names = []
    groups_list = list(user.groups.all())
    for item in groups_list:
        group_names.append(item.name)
    return group_names
