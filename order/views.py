from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from userauth.models import AccountInfo
from .models import OrderItem, Order
from django.utils.html import escape
from django.template import loader
from django.http import HttpResponse



def add_to_cart(request, slug):
    # user = get_object_or_404(User, user=request.user)
    # product = Products.objects.filter(id=kwargs.get('item_id', "")).first()
    # product = get_object_or_404(Product, id=slug)
    # quantity = 0
    if request.method == 'POST':
        quantity = escape(request.POST.get('quantity'))
        order_exists = OrderItem.objects.filter(product_id=slug, user=request.user, is_ordered=False)

        if order_exists:
            order_item = OrderItem.objects.get(product_id=slug, user=request.user, is_ordered=False)
            order_quantity = int(order_item.quantity) + int(quantity)
            order_item.quantity = order_quantity
            order_item.save()
        else:
            order_item = OrderItem.objects.create(product_id=slug, user=request.user, is_ordered=False, quantity=quantity)

        return redirect("product_detail", slug=slug)


# load cart
def cart(request):
    cart_template = loader.get_template('order/cart.html')
    order_items = OrderItem.objects.filter(user=request.user, is_ordered=False)
    context ={
        'order_items':order_items,
    }

    return HttpResponse(cart_template.render(context, request))
    

#update cart
def update_cart(request, slug):
    cart_template = loader.get_template('order/cart.html') 
    if request.method == 'POST':
        update_quantity = escape(request.POST.get('update-quantity'))
    order_item = OrderItem.objects.get(product_id=slug, user=request.user, is_ordered=False)
    if int(update_quantity) == 0 :
        order_item.delete()
    else:  

        order_item.quantity = update_quantity
        order_item.save()
    return redirect("cart")

# checkout 
def checkout(request):
    checkout_template = loader.get_template('order/checkout.html')
    if request.user.is_authenticated:
            accountinfo = AccountInfo.objects.get(customer= request.user)
    order_items = OrderItem.objects.filter(user=request.user, is_ordered=False)
    order_total = 0
    if order_items:
        for item in order_items:
            order_total += item.product.price * item.quantity
    context = {
        'order_items': order_items,
        'order_total': order_total,
        'accountinfo': accountinfo,
    }

    return HttpResponse(checkout_template.render(context, request))