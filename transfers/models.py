from django.db import models
from products.models import Product
from warehouses.models import Warehouses
from django.contrib.auth.models import User


class StockTransfer(models.Model):
    number = models.CharField(max_length=100, unique=True)
    to_warehouse = models.ForeignKey(Warehouses, on_delete=models.CASCADE, related_name='to_ware_trans')
    from_warehouse = models.ForeignKey(Warehouses, on_delete=models.CASCADE, related_name='from_ware_trans')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_trans')
    is_posted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{ self.from_warehouse.name } > { self.to_warehouse.name } - №{ self.number }'


class TransferItem(models.Model):
    trasfer = models.ForeignKey(StockTransfer, on_delete=models.CASCADE, related_name='off_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='trans')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{ self.product.name } - №{ self.writeoff.number }'
