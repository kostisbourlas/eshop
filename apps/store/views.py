from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View

from apps.store.models import Item, Order


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'store/home.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'store/product.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")

        return render(self.request, 'store/order_summary.html', context)


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "../templates/store/product.html", context)


def checkout(request):
    return render(request, "checkout.html")
