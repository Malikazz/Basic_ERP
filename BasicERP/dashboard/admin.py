from django.contrib import admin
from .models import Order, OrderDocument, OrderImage, OrderMaterial, OrderProcess, Group

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderDocument)
admin.site.register(OrderImage)
admin.site.register(OrderProcess)
admin.site.register(OrderMaterial)
