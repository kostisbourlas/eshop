from django.shortcuts import render
from django.views.generic import ListView, DetailView

from apps.store.models import Item, OrderItem, Order


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'store/home.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'store/product.html'


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "../templates/store/product.html", context)


def checkout(request):
    return render(request, "checkout.html")


