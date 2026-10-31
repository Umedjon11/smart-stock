from django.views.generic import (
    ListView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from inventory.models import *
from warehouses.models import *


class HomeListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Product
    template_name = 'base/home.html'
    context_object_name = 'prodcuts'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['products_count'] = Product.objects.count()
        data['warehouses_count'] = Warehouses.objects.count()
        data['receipts_count'] = StockReceipt.objects.count()
        data['transfers_count'] = StockTransfer.objects.count()
        data['recent_movements'] = StockMovement.objects.all()[:5]

        return data