from django.shortcuts import render
from .models import *


def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


def cart(request):
    return render(request, 'store/cart.html', is_user_auth(request))


def checkout(request):
    return render(request, 'store/checkout.html', is_user_auth(request))


def is_user_auth(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
        }
    context = {'items': items, 'order': order}
    return context
