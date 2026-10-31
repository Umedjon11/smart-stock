from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from products.models import Product
from inventory.models import StockReceipt, StockWriteOff
from transfers.models import StockTransfer, TransferItem

from django.db.models import Sum, F
from warehouses.models import Warehouses, Stock
from inventory.models import ReceiptItem, WriteOffItem, StockReceipt, StockWriteOff


class Dashboard(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'reports/dashboard.html'

    def test_func(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return True

        if hasattr(user, 'employee_profile'):
            return user.employee_profile.position in [
                'manager', 'accountant'
            ]
        return False
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['products_count'] = Product.objects.filter(is_active=True).count()
        context['receipts_count'] = StockReceipt.objects.filter(is_posted=True).count()
        context['writeoffs_count'] = StockWriteOff.objects.filter(is_posted=True).count()
        context['transfers_count'] = StockTransfer.objects.filter(is_posted=True).count()

        return context


class StockReportView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'reports/stock.html'

    def test_func(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return True

        if hasattr(user, 'employee_profile'):
            return user.employee_profile.position in [
                'manager', 'accountant'
            ]
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stocks = Stock.objects.filter(
            warehouse__is_active=True, product__is_active=True
        ).select_related('product', 'warehouse', 'product__unit')

        
        context['stock_data'] = stocks
        context['total_positions'] = stocks.count()
        context['empty_count'] = stocks.filter(quantity=0).count()
        context['low_count'] = stocks.filter(quantity__gt=0, 
                            quantity__lte=F('product__min_stock_level')).count()

        return context


class MovementReportView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'reports/movements.html'

    def test_func(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return True

        if hasattr(user, 'employee_profile'):
            return user.employee_profile.position in [
                'manager', 'accountant'
            ]
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        receipts = ReceiptItem.objects.filter(receipt__is_posted=True
                ).select_related('product', 'receipt', 'receipt__warehouse')

        writeoffs = WriteOffItem.objects.filter(writeoff__is_posted=True
                ).select_related('product', 'writeoff', 'writeoff__warehouse')

        transfers = TransferItem.objects.filter(writeoff__is_posted=True
                ).select_related('product', 'writeoff', 'writeoff__warehouse')

        context['receipts'] = receipts
        context['writeoffs'] = writeoffs
        context['transfers'] = transfers

        context['receipts_count'] = receipts.count()
        context['writeoffs_count'] = writeoffs.count()
        context['transfers_count'] = transfers.count()

        return context


class LowStockReportView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'reports/low_stock.html'

    def test_func(self):
        user = self.request.user

        if user.is_superuser or user.is_staff:
            return True

        if hasattr(user, 'employee_profile'):
            return user.employee_profile.position in [
                'manager', 'accountant'
            ]
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        low_stocks = Stock.objects.filter(
            warehouse__is_active=True, 
            product__is_active=True,
            quantity__gt=0,
            quantity__lte=F('product__min_stock_level')
        ).select_related('product', 'warehouse', 'product__unit')

        context['low_stocks'] = low_stocks
        context['low_count'] = low_stocks.count()

        return context