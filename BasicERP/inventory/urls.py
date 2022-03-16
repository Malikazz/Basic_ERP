from django.urls import path
from . import views

# URLCONF
urlpatterns = [
    path("index/", views.index),
    path("all_inventory/", views.view_all_inventory, name="view_inventory"),
    path("view_material", views.view_by_material_code, name="view_inventory"),
    #path("update-inventory/<material_code>", views.update_inventory, name="update_inventory"),
    #path("remove-inventory/<material_code>", views.remove_inventory, name="remove_inventory")
]
