from django.urls import path, include
from django.contrib.auth import urls
from . import views

app_name = "users"
urlpatterns = [
    path("change_password", views.user_change_password, name="user_change_password"),
    path(
        "reset_password",
        views.user_reset_password,
        name="user_reset_password",
    ),
    path("reset_password/<uid>/<token>/", views.user_reset, name="reset"),
]
