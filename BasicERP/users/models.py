from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserInfo(User):
    """Used to store addtional info on the users"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
