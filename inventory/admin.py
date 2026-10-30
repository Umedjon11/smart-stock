from django.contrib import admin
from .models import *

admin.site.register([StockMovement, StockReceipt, StockWriteOff, ReceiptItem, WriteOffItem])