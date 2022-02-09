from typing import List, Dict
from .models import Order
from django.contrib.auth.models import User
from django.db.models import Q


def _get_order_and_related_data(user: User, orders: dict) -> None:
    """Adds any orders and related data found to orders dict uses the `order.id` to prevent duplicate data"""
    user_groups = _get_all_users_groups(user)
    order_list = list(
        Order.objects.filter(Q(order_tags__pk__in=user_groups) & Q(archived=False))
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
            "order_images": order_images,
            "order_tags": order_tags,
        }


def _get_all_users_groups(user: User) -> List:
    """Returns list of users groups"""
    group_names = []
    groups_list = list(user.groups.all())
    for item in groups_list:
        group_names.append(item.pk)
    return group_names


def get_orders_by_user_role(user: User) -> Dict[str, Dict[str, object]]:
    """Will use the users groups to determine what orders to return, return will include {order, order_documents, order_images, order_tags}"""
    orders = {}
    _get_order_and_related_data(user, orders)
    return orders
