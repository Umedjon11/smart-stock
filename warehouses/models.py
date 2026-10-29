from django.db import models
from products.models import Product

class Warehouses(models.Model):
    name=models.CharField(max_length=255)
    address=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Stock(models.Model):
    warehouse=models.ForeignKey(Warehouses,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)

    class Meta:
        unique_together = ('warehouse', 'product')

    def __str__(self):
        return f"{self.product.name} — {self.warehouse.name}: {self.quantity} {self.product.unit.short_name if self.product.unit else ''}"

