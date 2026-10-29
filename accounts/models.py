from django.db import models
from django.contrib.auth.models import User


class EmployeeProfile(models.Model):
    POSITION_CHOICES = [
        ('manager', 'Менеджер'),
        ('warehouse_worker', 'Работник склада'),
        ('accountant', 'Бухгалтер'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    phone = models.CharField(max_length=17, blank=True)
    position = models.CharField(max_length=100, choices=POSITION_CHOICES, default='warehouse_worker')
    photo = models.ImageField(upload_to='employees/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username