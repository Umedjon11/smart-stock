from django.db import models
from django.contrib.auth.models import User


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=17)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class SupplyOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('received', 'Получен'),
        ('cancelled', 'Отменён'),
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='orders')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='supply_orders')
    order_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    received_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'Заказ #{self.pk} - {self.supplier.name}'



class SupplyOrderItem(models.Model):
    order = models.ForeignKey(SupplyOrder, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def total_price(self):
        return self.quantity * self.unit_price  

    def __str__(self):
        return f'{self.product_name} - {self.quantity}'
