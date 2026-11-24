from django.db import models
from LeafBack.models import ProductDb

class LeafImage(models.Model):
    image = models.ImageField(upload_to='leaf_images/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.image.name}"
    
class CreateAccountDb(models.Model):
    username = models.CharField(max_length=30, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=30, null=True, blank=True)

class cartdb(models.Model):
    username = models.CharField(max_length=30, null=True, blank=True)
    product = models.ForeignKey(ProductDb, on_delete=models.CASCADE)
    productname = models.CharField(max_length=30, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    totalprice = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="cart_images/", null=True, blank=True)

class orderdb(models.Model):
    username = models.CharField(max_length=30, null=True, blank=True)
    productname = models.CharField(max_length=30, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    totalprice = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)