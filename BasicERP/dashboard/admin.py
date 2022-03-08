from django.contrib import admin
from .models import Order, OrderDocument, OrderImage, Material, Process, Group

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderDocument)
admin.site.register(OrderImage)
admin.site.register(Process)
admin.site.register(Material)
