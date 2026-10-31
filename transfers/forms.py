from django.forms import ModelForm, Form
from django import forms
from .models import *
from django.forms import inlineformset_factory

class CreateTransferForm(forms.ModelForm):
    class Meta:
        model = StockTransfer
        fields = ['number', 'from_warehouse', 'to_warehouse']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm'}),
            'from_warehouse': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm'}),
            'to_warehouse': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm'}),
        }

TransferItemFormSet = inlineformset_factory(
    StockTransfer,
    TransferItem,
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