from .models import Order, OrderDocument, OrderTag
from django.contrib.auth.models import User


def get_orders_by_user_role(user: User):
    orders = set()
    user_groups = get_all_users_groups(user)
    if "Managing Director" in user_groups:
        orders.append(
            Order.objects.filter(order_tags != "Archive")
            .prefetch_related("OrderDocument")
            .all()
        )
    if "Inventory Manager" in user_groups:
        orders.append(
            Order.objects.filter(order_tags="Inventory")
            .prefetch_related("OrderDocument")
            .all()
        )
    if "Production Manager" in user_groups:
        orders.append(
            Order.objects.filter(order_tags="Production Review")
            .prefetch_related("OrderDocument")
            .all()
        )
    if "Sales" in user_groups:
        orders.append(
            Order.objects.filter(order_tags="Sales")
            .prefetch_related("OrderDocument")
            .all()
        )
    if "Production Staff" in user_groups:
        orders.append(
            Order.objects.filter(order_tags="Production")
            .prefetch_related("OrderDocument")
            .all()
        )
    if "Designer" in user_groups:
        orders.append(
            Order.objects.filter(order_tags="Design")
            .prefetch_related("OrderDocument")
            .all()
        )
    return orders


def get_all_users_groups(user: User):
    return list(user.groups.objects.all())
