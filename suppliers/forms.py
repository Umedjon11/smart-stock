from django import forms
from .models import Supplier, SupplyOrder, SupplyOrderItem



class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone', 'email', 'address']


class SupplyOrderForm(forms.ModelForm):
    class Meta:
        model = SupplyOrder
        fields = ['supplier', 'notes']


class SupplyOrderStatusForm(forms.ModelForm):
    class Meta:
        model = SupplyOrder
        fields = ['status']


class SupplyOrderItemForm(forms.ModelForm):
    class Meta:
        model = SupplyOrderItem
        fields = ['product_name', 'quantity', 'unit_price']