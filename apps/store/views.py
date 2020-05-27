from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View

from apps.store.forms import CheckoutForm, CouponForm
from apps.store.models import Item, Order, BillingAddress, Payment

import stripe

# stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


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
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

        return render(self.request, 'store/order_summary.html', context)


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "../templates/store/product.html", context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect(self.request, "store/checkout.html")

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
                payment_option = form.cleaned_data.get('payment_option')

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

                if payment_option == 'S':
                    return redirect("store:payment", payment_option='stripe')

                if payment_option == 'P':
                    return redirect("store:payment", payment_option='paypal')

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order.")
            return redirect("store:order-summary")

        messages.warning(self.request, "Invalid payment option selected")
        return redirect("store:checkout")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, "store/payment.html", context)

        messages.warning(self.request, "You have not added a billing address")
        return redirect("store:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get("stripeToken")
        payment_amount_in_cents = int(order.get_total_cost_order() * 100)

        try:
            charge = stripe.Charge.create(
                amount=payment_amount_in_cents,
                currency="eur",
                source="tok_visa",
                # source=token,
            )

            # create payment
            payment = Payment()
            payment.stripe_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total_cost_order()
            payment.save()

            # assign payment to the order

            order_items = order.items.all()
            order_items.update(ordered=True)

            for order_item in order_items:
                order_item.save()

            order.ordered = True
            order.payment = payment
            order.save()

        except stripe.error.CardError as e:
            messages.warning(self.request, f"{e.error.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Too many requests made to the API too quickly")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(self.request, "Invalid parameters were supplied.")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "You are not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Network communication with Stripe failed")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect("/")

        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.warning(self.request, "A serious error occurred. We have been notified and try to solve it.")
            return redirect("/")

        messages.success(self.request, "Your order was successful")
        return redirect("/")
