from django.contrib import admin
from .models import Order, OrderTag, OrderDocument

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderTag)
admin.site.register(OrderDocument)
