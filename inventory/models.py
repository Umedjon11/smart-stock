from django.db import models
from products.models import Product
from warehouses.models import Warehouses
from transfers.models import StockTransfer
from django.contrib.auth.models import User


class StockReceipt(models.Model):
    number = models.CharField(max_length=100, unique=True)
    warehouse = models.ForeignKey(Warehouses, on_delete=models.CASCADE, related_name='ware_rec')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_mov')
    is_posted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{ self.rec_mov } - №{ self.number }'


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(StockReceipt, on_delete=models.CASCADE, related_name='rec_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prod_rec')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{ self.product.name } - №{ self.receipt.number }'


class StockWriteOff(models.Model):
    number = models.CharField(max_length=100, unique=True)
    warehouse = models.ForeignKey(Warehouses, on_delete=models.CASCADE, related_name='ware_offs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_off')
    is_posted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{ self.movment } - №{ self.number }'


class WriteOffItem(models.Model):
    writeoff = models.ForeignKey(StockWriteOff, on_delete=models.CASCADE, related_name='off_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='mov')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{ self.product.name } - №{ self.writeoff.number }'


class StockMovement(models.Model):
    MOVMENT_TYPES = (
        ('in', 'Приход'),
        ('out', 'Уход'),
        ('trans_in', 'Перемещение (приход)'),
        ('trans_out', 'Перемещение (уход)')
    )

    type = models.CharField(choices=MOVMENT_TYPES, default='in', max_length=50)
    receipt = models.ForeignKey(StockReceipt, on_delete=models.CASCADE, related_name='rec_mov', null=True, blank=True)
    write_off = models.ForeignKey(StockWriteOff, on_delete=models.CASCADE, related_name='off_mov', null=True, blank=True)
    transfer = models.ForeignKey(StockTransfer, on_delete=models.CASCADE, related_name='trans_mov', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{ self.receipt.warehouse.name if self.receipt else self.write_off.warehouse.name if self.write_off else self.transfer.warehouse.name } - { self.type }'
