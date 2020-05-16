from django.urls import path

from apps.store.services import add_to_cart, remove_from_cart, decrease_quantity_from_cart
from apps.store.views import HomeView, ItemDetailView, OrderSummaryView, CheckoutView, PaymentView

app_name = 'store'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('decrease-quantity/<slug>', decrease_quantity_from_cart, name='decrease-quantity-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name="payment"),
]
