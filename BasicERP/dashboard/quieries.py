from typing import List, Dict
from .models import Order, OrderDocument, OrderTag, OrderImage
from django.contrib.auth.models import User
from django.db.models import Q

##TODO: can currently return duplicates looking into how to prevent this
def get_orders_by_user_role(user: User) -> List[Dict[str, object]]:
    orders = []
    user_groups = get_all_users_groups(user)
    if "Managing Director" in user_groups:

        order_list = list(
            Order.objects.filter(~Q(order_tags__name="Archive"))
            .prefetch_related("order_documents")
            .prefetch_related("order_images")
            .prefetch_related("order_tags")
        )
        for item in order_list:
            order_documents = list(item.order_documents.all())
            order_images = list(item.order_images.all())
            orders.append(
                {
                    "order": item,
                    "order_documents": order_documents,
                    "order_image": order_images,
                }
            )
    if "Inventory Manager" in user_groups:
        orders.append(
            Order.objects.filter(order_tags__name="Inventory")
            .values_list()
            .prefetch_related("order_documents")
            .prefetch_related("order_tags")
        )
    if "Production Manager" in user_groups:
        orders.append(
            Order.objects.filter(order_tags__name="Production Review")
            .values_list()
            .prefetch_related("order_documents")
            .prefetch_related("order_tags")
        )
    if "Sales" in user_groups:
        orders.append(
            Order.objects.filter(order_tags__name="Sales")
            .values_list()
            .prefetch_related("order_documents")
            .prefetch_related("order_tags")
        )
    if "Production Staff" in user_groups:
        orders.append(
            Order.objects.filter(order_tags__name="Production")
            .values_list()
            .prefetch_related("order_documents")
            .prefetch_related("order_tags")
        )
    if "Designer" in user_groups:
        orders.append(
            Order.objects.filter(order_tags__name="Design")
            .values_list()
            .prefetch_related("order_documents")
            .prefetch_related("order_tags")
        )

    return orders


def get_all_users_groups(user: User) -> List:
    group_names = []
    groups_list = list(user.groups.all())
    for item in groups_list:
        group_names.append(item.name)
    return group_names
