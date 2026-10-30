from django.contrib import admin

from .models import Supplier, SupplyOrderItem, SupplyOrder

admin.site.register([Supplier, SupplyOrder, SupplyOrderItem])