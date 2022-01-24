from email import message
from django.shortcuts import render
from django.contrib import messages


# Create your views here.
def index(request):
    messages.add_message(request, messages.INFO, "Hello world.")
    return render(request, "dashboard/index.html")
