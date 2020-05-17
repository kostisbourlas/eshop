from django.contrib import admin

from apps.store.models import Item, OrderItem, Order, Payment

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)