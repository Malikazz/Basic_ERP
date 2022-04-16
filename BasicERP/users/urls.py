from django.urls import path, include
from django.contrib.auth import urls
from . import views

app_name = "users"
urlpatterns = [
    path("change-password/", views.user_change_password, name="change-password"),
    path(
        "reset-password",
        views.user_reset_password,
        name="user-reset-password/",
    ),
    path("reset_password/<uid>/<token>", views.user_reset, name="reset"),
]
