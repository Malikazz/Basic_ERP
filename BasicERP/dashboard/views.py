from email import message
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    messages.add_message(request, messages.INFO, "Hello world.")
    return render(request, "dashboard/index.html")
