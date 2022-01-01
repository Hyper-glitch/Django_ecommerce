import datetime
import json
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from .utils import is_user_auth, guest_order


def store(request):
    products = Product.objects.all()
    context = is_user_auth(request)
    context['products'] = products
    return render(request, 'store/store.html', context)


def cart(request):
    context = is_user_auth(request)
    return render(request, 'store/cart.html', context)


def checkout(request):
    context = is_user_auth(request)
    return render(request, 'store/checkout.html', context)


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
    else:
        customer, order = guest_order(request, data)

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

    return JsonResponse('Payment completed', safe=False)
