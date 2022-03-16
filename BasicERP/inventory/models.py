
import os
from django.db import models
from django.contrib.auth.models import Group
from django.forms import DateField
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.dispatch import receiver
#from dashboard.models import Order
# Create your models here.


class Merchant(models.Model):
    merchant_code = models.IntegerField(unique=True)
    company_name = models.CharField(max_length=75)
    contact_name = models.CharField(max_length=75)
    contact_role = models.CharField(max_length=50)
    contact_email = models.EmailField(null=True, blank=True)
    contact_number = PhoneNumberField()
    address = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.company_name


class Material(models.Model):
    name = models.CharField(max_length=55)
    material_code = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    unit_measurement = models.CharField(max_length=255)
    status = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.name


class MerchantMaterials(models.Model):
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    merchant_id = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    unit_cost = models.DecimalField(max_digits=6, decimal_places=2)
    avg_order_processing_time = models.IntegerField  # weeks
    merchant_material_code = models.CharField(
        max_length=100, blank=True, null=True)
    merchant_unit_measurement = models.CharField(
        max_length=50, blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.material_id


class MaterialsOnOrder(models.Model):
    material_id = models.ForeignKey(
        MerchantMaterials, on_delete=models.CASCADE)
    order_id = models.IntegerField()
    units_on_order = models.IntegerField
    order_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.order_id


class MaterialInventory(models.Model):
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    units_available = models.IntegerField()
    units_reserved_for_orders = models.IntegerField()
    units_defective = models.IntegerField()
    total_units_on_order = models.IntegerField()

    def __str__(self):
        return self.material_id
