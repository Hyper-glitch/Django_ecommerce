from PIL import Image
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_img_url(self):
        try:
            url = self.image.url
        except:
            url = "/static/images/placeholder.png"
        return url

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            if img.height > 640 or img.width > 360:
                output_size = (640, 360)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    data_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    @property
    def get_total_data(self):
        total_data = {
            'total_items': '',
            'total_price': '',
        }
        order_items = self.orderitem_set.all()
        total_data['total_items'] = sum([item.quantity for item in order_items])
        total_data['total_price'] = sum([item.get_total_price for item in order_items])
        return total_data

    @property
    def is_need_shipping_info(self):
        shipping_info = False
        order_items = self.orderitem_set.all()
        for order_item in order_items:
            if not order_item.product.digital:
                shipping_info = True
        return shipping_info

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
