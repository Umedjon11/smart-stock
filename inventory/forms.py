from django.forms import ModelForm, Form
from django import forms
from .models import StockReceipt, ReceiptItem
from django.forms import inlineformset_factory

class CreateReceiptForm(ModelForm):
    class Meta:
        model = StockReceipt
        fields = ['number', 'warehouse']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm'}),
            'warehouse': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm'}),
        }

ReceiptItemFormSet = inlineformset_factory(
    StockReceipt,
    ReceiptItem,
    fields=['product', 'quantity'],
    extra=1,
    can_delete=True,
    widgets={
        'product': forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg bg-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500'
        }),
        'quantity': forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
            'min': '1',
            'placeholder': 'Кол-во'
        }),
    }
)