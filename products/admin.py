from django.contrib import admin

from products.models import Category,Unit,Product

admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Product)
