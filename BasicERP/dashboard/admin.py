from django.contrib import admin

from inventory.models import MaterialInventory
from .models import Order, OrderDocument, OrderImage, Process, Group

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderDocument)
admin.site.register(OrderImage)
admin.site.register(Process)
admin.site.register(MaterialInventory)
