from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView, CreateView
)
from django.views import View
from django.urls import reverse_lazy
from .models import *

class MovementsListView(ListView):
    model = StockMovement
    template_name = 'inventory/movement_list.html'
    context_object_name = 'movements'


class MovementDetailView(DetailView):
    model = StockMovement
    template_name = 'inventory/movement_detail.html'
    context_object_name = 'movement'