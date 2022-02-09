from django.contrib import admin
from .models import Order, OrderDocument, OrderImage

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderDocument)
admin.site.register(OrderImage)
