from django.contrib import admin
from .models import (
    Order,
    OrderDocument,
    OrderImage,
    Material,
    Process,
    Group,
    ApplicationSettings,
)

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderDocument)
admin.site.register(OrderImage)
admin.site.register(Process)
admin.site.register(Material)
admin.site.register(ApplicationSettings)
