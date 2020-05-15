from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from apps.store.models import Item, OrderItem, Order


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item,
                                                 user=request.user,
                                                 ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            # order_item.quantity += 1
            order_item.quantity = F('quantity') + 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    return redirect("store:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,
                                                  user=request.user,
                                                  ordered=False
                                                  )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")

        else:
            messages.info(request, "This item is not in your cart.")
            return redirect("store:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("store:product", slug=slug)

    return redirect("store:order-summary")


@login_required
def decrease_quantity_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,
                                                  user=request.user,
                                                  ordered=False
                                                  )[0]
            if order_item.quantity > 1:
                order_item.quantity = F('quantity') - 1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
            else:
                order.items.remove(order_item)
                order_item.delete()
                messages.info(request, "This item was removed from your cart.")
            return redirect("store:order-summary")

        else:
            messages.info(request, "This item is not in your cart.")
            return redirect("store:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("store:product", slug=slug)
