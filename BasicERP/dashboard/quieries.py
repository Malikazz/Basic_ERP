from typing import List, Dict, Tuple
from .models import Order, OrderImage, OrderDocument, Customer
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.db import transaction


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


def create_order_images_from_post(item_list: list) -> List[OrderImage]:
    images = []
    for image in item_list:
        images.append(OrderImage.objects.create(name=image._name, image_location=image))
    return images


def create_order_documents_from_post(item_list: list) -> List[OrderDocument]:
    documents = []
    for image in item_list:
        documents.append(
            OrderDocument.objects.create(name=image._name, file_location=image)
        )
    return documents


def add_images_to_order(order: Order, images: List[OrderImage]) -> None:
    for item in images:
        order.order_images.add(item.pk)
    order.save()


def add_documents_to_order(order: Order, documents: List[OrderDocument]) -> None:
    for item in documents:
        order.order_documents.add(item.pk)
    order.save()


def order_change_groups(order: Order, groups: List[Group]) -> None:
    with transaction.atomic():
        order.order_tags.clear()
        for item in groups:
            order.order_tags.add(item.pk)


def get_new_order_groups() -> List[Group]:
    return list(Group.objects.filter(Q(name="Managing Director") | Q(name="Sales")))


def archive_order(order: Order) -> None:
    order.archived = True
    order.save()


def get_order_by_pk(pk: int) -> Order:
    return Order.objects.get(pk=pk)


def get_order_images_documents(
    order_id: int,
) -> Tuple[Order, OrderImage, OrderDocument]:
    order = Order.objects.get(pk=order_id)
    images = list(order.order_images.all())
    documents = list(order.order_documents.all())
    return (order, images, documents)


def get_order_image(image_id: int) -> OrderImage:
    return OrderImage.objects.get(pk=image_id)


def remove_delete_image(order_id: int, image_id: int) -> None:
    with transaction.atomic():
        order = get_order_by_pk(order_id)
        image = get_order_image(image_id)
        order.order_images.remove(image)
        OrderImage.objects.filter(id=image.pk).delete()
    return None


def get_customer(order_id: int) -> Customer:
    return Order.objects.get(pk=order_id).customer
