import json
import datetime
from django.shortcuts import render
from .models import *
from django.http import JsonResponse


def store(request):
    products = Product.objects.all()
    context = is_user_auth(request)
    context['products'] = products
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
        cart_items = order.get_total_data['total_items']
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
            'shipping_info': False,
        }
        cart_items = order['get_cart_items']
    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }
    return context


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1
    order_item.save()

    if order_item.quantity == 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)


def process_order(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = datetime.datetime.now().timestamp()

        if total == float(order.get_total_data['total_price']):
            order.complete = True
        order.save()

        if order.is_need_shipping_info:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping_info']['address'],
                city=data['shipping_info']['city'],
                state=data['shipping_info']['state'],
                zipcode=data['shipping_info']['zipcode'],
            )

    else:
        pass
    return JsonResponse('Payment completed', safe=False)
