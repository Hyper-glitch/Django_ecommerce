import json
from .models import *


def cart_with_cookies(request):
    cart = json.loads(request.COOKIES.get('cart'))
    items = []
    order = {
        'get_cart_total': 0,
        'get_cart_items': 0,
        'is_need_shipping_info': False,
    }
    cart_items = order['get_cart_items']

    for cart_obj in cart:
        cart_items += cart[cart_obj]['quantity']

        is_product_exists = Product.objects.filter(id=cart_obj).exists()

        if is_product_exists:
            product = Product.objects.get(id=cart_obj)

            total_price = (product.price * cart[cart_obj]['quantity'])
            order['get_cart_total'] += total_price
            order['get_cart_items'] += cart[cart_obj]['quantity']

            if not product.digital:
                order['shipping_info'] = True

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'get_img_url': product.get_img_url
                },
                'quantity': cart[cart_obj]['quantity'],
                'get_total_price': total_price,
            }
            items.append(item)
        else:
            pass

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }

    return context


def cart_with_auth_user(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cart_items = order.get_total_data['total_items']
    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items,
    }
    return context


def is_user_auth(request):
    if request.user.is_authenticated:
        context = cart_with_auth_user(request)
    else:
        context = cart_with_cookies(request)
    return context


def guest_order(request, data):
    name = data['form']['name']
    email = data['form']['email']
    cookie = cart_with_cookies(request)
    items = cookie['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return customer, order
