import os
from django.db import models
from django.contrib.auth.models import Group
from django.forms import DateField
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.dispatch import receiver

# TODO: Need to test the one drive api to see how this works
# https://docs.microsoft.com/en-us/graph/api/resources/onedrive?view=graph-rest-1.0
class OrderDocument(models.Model):
    name = models.CharField(max_length=255)
    file_location = models.FileField()

    def __str__(self):
        return self.name


class OrderImage(models.Model):
    name = models.CharField(max_length=255)
    alt_description = models.CharField(max_length=255, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    image_location = models.ImageField()

    def __str__(self):
        return self.name


class Merchant(models.Model):
    company_name = models.CharField(max_length=75)
    contact_name = models.CharField(max_length=75)
    contact_email = models.EmailField(null=True, blank=True)
    contact_number = PhoneNumberField()
    address = models.CharField(max_length=255)

    def __str__(self):
        self.company_name


class Material(models.Model):
    name = models.CharField(max_length=55)
    material_code = models.CharField(max_length=255, unique=True)
    units = models.IntegerField()
    unit_measurement = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class MerchantMaterials(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    merchant_id = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    unit_cost = models.DecimalField(max_digits=6, decimal_places=2)
    purchase_date = models.DateField()
    units_on_order = models.IntegerField
    po = models.CharField(max_length=100)
    merchant_material_code = models.CharField(max_length=100, blank=True, null=True)
    merchant_unit_measurement = models.CharField(max_length=50, blank=True, null=True)


class Process(models.Model):
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    customer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = PhoneNumberField()
    email_contact = models.EmailField()
    fax = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return self.customer_name


class Order(models.Model):
    order_name = models.CharField(max_length=255)
    order_materials = models.ForeignKey(Material, on_delete=models.PROTECT, null=True)
    order_process = models.ForeignKey(Process, on_delete=models.PROTECT, null=True)
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
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order_creator = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.order_name


@receiver(models.signals.post_delete, sender=OrderImage)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem when
    model instance is deleted.
    """
    if instance.image_location:
        if os.path.isfile(instance.image_location.path):
            os.remove(instance.image_location.path)


@receiver(models.signals.post_delete, sender=OrderDocument)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when
    model instance is deleted.
    """
    if instance.file_location:
        if os.path.isfile(instance.file_location.path):
            os.remove(instance.file_location.path)


class ApplicationSettings(models.Model):
    """Stores application wide settings"""

    send_new_order_emails = models.BooleanField(default=True)
