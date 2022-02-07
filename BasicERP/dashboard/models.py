from pydoc import describe
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.


class OrderTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# TODO: Need to test the one drive api to see how this works
# https://docs.microsoft.com/en-us/graph/api/resources/onedrive?view=graph-rest-1.0
class OrderDocument(models.Model):
    name = models.CharField(max_length=255)
    download_url = models.TextField()
    drive_id = models.CharField(max_length=255)


class Order(models.Model):
    order_name = models.CharField(max_length=255)
    order_tags = models.ManyToManyField(OrderTag)
    order_documents = models.ManyToManyField(OrderDocument)

    def __str__(self):
        return self.order_name
