from django.db import models

# Create your models here.
class Item(models.Model):
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    tags = models.TextField()
    stock_status = models.CharField(max_length=50)
    available_stock = models.IntegerField()
