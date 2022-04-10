from django.core.mail import send_mail
from django.contrib.auth.models import User
from dashboard.models import Order
from dashboard.quieries import get_application_settings, get_users_by_order
from django.template.loader import render_to_string

## TODO: This module should be setup with tasks once a task system is created
## As it could hang the application in large volumns


def new_user_email(user: User) -> None:
    """Sends a email to the new users registered email welcoming them"""
    return 0


def email_order_groups(order: Order, hostname: str) -> None:
    """emails all members in the orders groups"""
    subject = "New Order in Domain"
    message = render_to_string(
        "dashboard/email/order_in_domain.html", {"order": order, "uri": hostname}
    )
    from_sender = "test@test.com"
    users = get_users_by_order(order)
    email_list = []
    for user in users:
        email_list.append(user.email)
    send_mail(subject, message, from_sender, email_list)


def new_order_email(order: Order, hostname: str) -> None:
    """Send an email to all users in the groups asigned to the new order"""
    app_settings = get_application_settings()
    if app_settings.send_new_order_emails:
        email_order_groups(order, hostname)
