from django.conf import settings
from django.db import models
from shop.models import Product


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    guest_registered_merged = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    # date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.product}"


class Order(models.Model):
    ref_code = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True, blank=True)
    order_cost = models.FloatField(null=True, blank=True)
    paid = models.BooleanField(default=False)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])


    def __str__(self):
        return '{0} - {1}'.format(self.user.name, self.ref_code)
