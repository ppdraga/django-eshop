from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from catalog.models import GoodItem

# Create your views here.

class GoodItemListView(ListView):
    model = GoodItem
    template_name = 'catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        return GoodItem.objects.all()

class GoodItemDetailView(DetailView):
    model = GoodItem

class GoodItemCreateView(CreateView):
    model = GoodItem
    fields = ['title', 'vendor', 'price', 'unit_of_measure']

class GoodItemUpdateView(UpdateView):
    model = GoodItem

class GoodItemDeleteView(DeleteView):
    model = GoodItem