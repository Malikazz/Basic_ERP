from django.db import models
from django.contrib.auth.models import Group
from phonenumber_field.modelfields import PhoneNumberField

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


class OrderMaterial(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name


class OrderProcess(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name


class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = PhoneNumberField()
    email_contact = models.EmailField()
    fax = PhoneNumberField(blank=True, null=True)


class Order(models.Model):
    order_name = models.CharField(max_length=255)
    order_materials = models.ForeignKey(
        OrderMaterial, on_delete=models.CASCADE, null=True
    )
    order_process = models.ForeignKey(OrderProcess, on_delete=models.CASCADE, null=True)
    order_tags = models.ManyToManyField(Group)
    order_documents = models.ManyToManyField(OrderDocument, blank=True)
    order_images = models.ManyToManyField(OrderImage, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    approved_by = models.CharField(max_length=80, blank=True, null=True)
    approval_date = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    quote = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    po_number = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.order_name
