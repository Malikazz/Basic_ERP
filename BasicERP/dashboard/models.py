from pydoc import describe
from django.db import models

# Create your models here.


class OrderTags(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_name = models.CharField(max_length=255)
    order_tags = models.ManyToManyField(OrderTags)

    def __str__(self):
        return self.order_name
