from django.db import models

# Create your models here.
class DiseaseDb(models.Model):
    diseasename = models.CharField(max_length=30, null=True, blank=True)
    plant = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    symptoms = models.CharField(max_length=30, null=True, blank=True)
    treatment = models.CharField(max_length=100, null=True, blank=True)
    experience = models.CharField(max_length=30, null=True, blank=True)
    image = models.ImageField(upload_to="image",null=True, blank=True)

class ProductDb(models.Model):
    productname = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="image",null=True, blank=True)