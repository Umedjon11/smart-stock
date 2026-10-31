from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, DetailView, CreateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from .models import *
from .forms import *
from inventory.models import StockMovement
from warehouses.models import Stock

class TranfersListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = StockTransfer
    template_name = 'transfers/transfer_list.html'
    context_object_name = 'transfers'


class TranferDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = StockTransfer
    template_name = 'transfers/transfer_detail.html'
    context_object_name = 'transfer'


class PostTranferView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', '')
        transfer = StockTransfer.objects.get(pk = pk)
        if not transfer.is_posted:
            transfer.is_posted = True
            transfer.save()

            StockMovement.objects.create(
                transfer = transfer,
                type = 'trans_in'
            )
            StockMovement.objects.create(
                            transfer = transfer,
                            type = 'trans_out'
                        )

        return redirect('transfer_list')

class TranferCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = CreateTransferForm
    template_name = 'transfers/transfer_form.html'
    success_url = reverse_lazy('transfer_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.method == 'POST':
            if 'formset' not in data:
                data['formset'] = TransferItemFormSet(self.request.POST)
        else:
            if 'formset' not in data:
                data['formset'] = TransferItemFormSet()

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        form.instance.user = self.request.user

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['formset'] = TransferItemFormSet(self.request.POST, instance=self.object)
        return self.render_to_response(context)