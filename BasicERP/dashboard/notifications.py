from django.core.mail import send_mail
from django.contrib.auth.models import User
from dashboard.models import Order
from dashboard.quieries import get_application_settings, get_users_by_order
from django.template.loader import render_to_string
from django.http import request

## TODO: This module should be setup with tasks once a task system is created
## As it could hang the application in large volumns


def new_user_email(user: User) -> None:
    """Sends a email to the new users registered email welcoming them"""
    return 0


def email_order_groups(order: Order, request: request) -> None:
    """emails all members in the orders groups"""
    # Drops the / so we dont end up with //
    uri = request.build_absolute_uri("/")[:-1]
    subject = "New Order in Domain"
    message = render_to_string(
        "dashboard/email/new_order.html", {"order": order, "uri": uri}
    )
    from_sender = "test@test.com"
    users = get_users_by_order(order)
    email_list = []
    for user in users:
        email_list.append(user.email)
    send_mail(subject, message, from_sender, email_list)


def new_order_email(order: Order, request) -> None:
    """Send an email to all users in the groups asigned to the new order"""
    app_settings = get_application_settings()
    if app_settings.send_new_order_emails:
        email_order_groups(order, request)
