from django.urls import path, include
from django.contrib.auth import urls

app_name = "users"
urlpatterns = [path("", include("django.contrib.auth.urls"))]
