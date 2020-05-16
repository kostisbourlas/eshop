from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View

from apps.store.forms import CheckoutForm
from apps.store.models import Item, Order, BillingAddress


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


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "store/checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')

                # TODO: Add functionality for these fields
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                # payment_option = form.cleaned_data.get('payment_option')

                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip_code=zip_code,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: add redirect to selected payment view

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order.")
            return redirect("store:order-summary")

        return redirect("store:checkout")


class PaymentView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "store/payment.html")
