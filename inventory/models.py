from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=50)

class StockMovement(models.Model):
    MOVMENT_TYPES = (
        (' ')
    )