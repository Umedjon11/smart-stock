from django.shortcuts import render
from django.views.generic import TemplateView
from products.models import Product
from suppliers.models import SupplyOrder


class Dashboard(TemplateView):
    template_name = 'reports/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['products_count'] = Product.objects.filter(is_active=True).count()
        context['orders_count'] = SupplyOrder.objects.count()

        return context