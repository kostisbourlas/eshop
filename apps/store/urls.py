from django.urls import path

from apps.store.services import add_to_cart, remove_from_cart
from apps.store.views import HomeView, ItemDetailView

app_name = 'store'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    # path('checkout/', checkout, name='checkout'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart')
]
