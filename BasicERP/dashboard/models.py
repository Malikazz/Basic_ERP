from django.db import models
from django.contrib.auth.models import Group

# Create your models here.

# TODO: Need to test the one drive api to see how this works
# https://docs.microsoft.com/en-us/graph/api/resources/onedrive?view=graph-rest-1.0
class OrderDocument(models.Model):
    name = models.CharField(max_length=255)
    file_location = models.FileField()

    def __str__(self):
        return self.name


class OrderImage(models.Model):
    name = models.CharField(max_length=255)
    image_location = models.ImageField()

    def __str__(self):
        return self.name


class Order(models.Model):
    order_name = models.CharField(max_length=255)
    order_tags = models.ManyToManyField(Group)
    order_documents = models.ManyToManyField(OrderDocument, blank=True)
    order_images = models.ManyToManyField(OrderImage, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.order_name
