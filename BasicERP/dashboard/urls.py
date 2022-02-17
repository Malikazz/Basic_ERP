from django.urls import path, include
from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.index, name="index"),
    path("create-order", views.create_order, name="create-order"),
]
