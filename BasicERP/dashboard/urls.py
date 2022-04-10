from django.urls import path, include
from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.index, name="index"),
    path("create-order", views.create_order, name="create-order"),
    path("edit-order/<order_id>", views.edit_order, name="edit-order"),
    path("view-order/<order_id>", views.view_order, name="view-order"),
    path("remove-image/", views.remove_image, name="remove-image"),
    path("remove-document/", views.remove_document, name="remove-document"),
    path("create-material/", views.create_material, name="create-material"),
    path("edit-material/<material_id>", views.edit_material, name="edit-material"),
    path("view-materials/", views.view_materials, name="view-materials"),
    path("create-process/", views.create_material, name="create-process"),
    path("create-merchant/", views.create_material, name="create-merchant"),
]
