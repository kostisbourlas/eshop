from django.urls import path

from apps.store.views import HomeView, ItemDetailView

app_name = 'store'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
]
