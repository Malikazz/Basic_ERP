from email import message
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .quieries import get_orders_by_user_role
from .models import Order, OrderDocument

# Create your views here.
@login_required
def index(request):
    orders = get_orders_by_user_role(request.user)
    messages.add_message(request, messages.INFO, "Hello world.")
    return render(request, "dashboard/index.html", {"json_data": orders})
