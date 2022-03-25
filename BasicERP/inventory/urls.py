from django.urls import path
from . import views

# URLCONF
app_name = "inventory"
urlpatterns = [
    path("index/", views.index, name="index"),
    path("all_inventory/", views.view_all_inventory, name="view_inventory"),
    path("input_material_code/", views.get_material_code,
         name="input_material_code"),
    path("view_material/",
         views.view_by_material_code, name="view_material"),
    path("create_material/", views.create_material, name="create_materiall"),
    path("create_merchant/", views.create_merchant, name="create_merchant"),
    path("add_material_to_merchant/",
         views.add_material_to_merchant, name="merchant_material"),
    path("create_material_order/",
         views.create_material_order, name="material_order"),
    path("edit_material/<material_code>",
         views.edit_material, name="edit_material"),
    path("archive_material/<material_code>",
         views.edit_material, name="edit_material"),


]
