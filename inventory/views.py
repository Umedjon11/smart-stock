from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, DetailView, CreateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from .models import *
from .forms import *

class MovementsListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = StockMovement
    template_name = 'inventory/movement_list.html'
    context_object_name = 'movements'


class MovementDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = StockMovement
    template_name = 'inventory/movement_detail.html'
    context_object_name = 'movement'


class ReceiptsListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = StockReceipt
    template_name = 'inventory/receipt_list.html'
    context_object_name = 'receipts'


class ReceiptDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = StockReceipt
    template_name = 'inventory/receipt_detail.html'
    context_object_name = 'receipt'


class PostReceiptView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', '')
        receipt = StockReceipt.objects.get(pk = pk)
        if not receipt.is_posted:
            receipt.is_posted = True
            receipt.save()

            StockMovement.objects.create(
                receipt = receipt
            )

        return redirect('receipt_list')


class ReceiptCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = CreateReceiptForm
    template_name = 'inventory/receipt_form.html'
    success_url = reverse_lazy('receipt_list')

    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.method == 'POST':
            data['formset'] = ReceiptItemFormSet(self.request.POST)
        else:
            data['formset'] = ReceiptItemFormSet()

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
        return self.render_to_response(context)


class WriteOffListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = StockWriteOff
    template_name = 'inventory/writeoff_list.html'
    context_object_name = 'writeoffs'


class WriteOffDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = StockWriteOff
    template_name = 'inventory/writeoff_detail.html'
    context_object_name = 'writeoff'


class PostWriteOffView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', '')
        writeoff = StockWriteOff.objects.get(pk = pk)
        
        if not writeoff.is_posted:
            writeoff.is_posted = True
            writeoff.save()

            StockMovement.objects.create(
                write_off = writeoff,
                type = 'out'
            )

        return redirect('writeoff_list')


class WriteOffCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = CreateWriteOffForm
    template_name = 'inventory/writeoff_form.html'
    success_url = reverse_lazy('writeoff_list')

    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if self.request.method == 'POST':
            data['formset'] = CreateWriteOffForm(self.request.POST)
        else:
            data['formset'] = WriteOffItemFormSet()

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
        return self.render_to_response(context)

