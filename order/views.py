from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from userauth.models import AccountInfo, Customer
from .models import OrderItem, Order
from django.utils.html import escape
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import stripe
import json
from django.http import JsonResponse

# This is your test secret API key.
stripe.api_key = 'sk_test_51MnhhkFJZvKQhNrQgEc0qUvwPdzoa4aPHUX48Qt2eJOT5BZbYdgIslZAE1Zr3Hl1YVS0UeFegh2B4FrfmlvYiUJ400MA4p4STC'

#adds order items to order
def add_items_to_order(request):
    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(user=request.user, ordered=False)
        if order_items:
            order, created = Order.objects.get_or_create(user=request.user, ordered=False, items=order_items)
        
        

#gets current user (registered or guest user)
def get_customer(request):
    customer = request.user
    if request.user.is_anonymous:
        try:
            deviceId = request.COOKIES['deviceId']
            anonymousEmail = deviceId+'@guest.com'
            customer, created = Customer.objects.get_or_create(name=deviceId, email=anonymousEmail)
        except:
            print('Device Id yet to be created')
    return customer

#merges cart items added as a guest user to cart items added a registered user
def merge_guest_registered_cart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            deviceId = request.COOKIES['deviceId']
            customer = deviceId
            guest_user = Customer.objects.get(name=customer)

            #update logged in user's cart
            guest_order_items = OrderItem.objects.filter(user=guest_user, is_ordered=False, guest_registered_merged = False)
            if guest_order_items:
                for item in guest_order_items:
                    item_id = item.product_id
                    print ("item id ...........", item_id)
                    quantity = item.quantity
                    order_exists = OrderItem.objects.filter(product_id=item_id, user=request.user, is_ordered=False)
                    if order_exists:
                        print('order exist')
                        order_item = OrderItem.objects.get(product_id=item_id, user=request.user, is_ordered=False)
                        order_quantity = int(order_item.quantity) + int(quantity)
                        if order_item.quantity >= quantity:
                            order_quantity = int(order_item.quantity)
                        else:
                            order_quantity = int(quantity)
                        order_item.quantity = order_quantity
                        order_item.guest_registered_merged = True
                        order_item.save()

                        guest_order_item = OrderItem.objects.get(product_id=item_id, user=guest_user, is_ordered=False)
                        guest_order_item.quantity = order_quantity
                        guest_order_item.guest_registered_merged = True
                        guest_order_item.save()
                    else:
                        print('order does not exist')
                        order_item = OrderItem.objects.create(product_id=item_id, user=request.user, is_ordered=False, quantity=quantity, guest_registered_merged =True)              

        except:
            print("Merging guest and user carts failed")

def add_to_cart(request, slug):
    if request.method == 'POST':
        quantity = escape(request.POST.get('quantity'))
        
        try:
            customer = get_customer(request)
            order_exists = OrderItem.objects.get(product_id=slug, user=customer, is_ordered=False)
            if order_exists:
            # order_item = OrderItem.objects.get(product_id=slug, user=customer, is_ordered=False)
                order_quantity = int(order_exists.quantity) + int(quantity)
                order_exists.quantity = order_quantity
                order_exists.guest_registered_merged = False
                order_exists.save()
            else:
                pass
        except:
             order_item = OrderItem.objects.create(product_id=slug, user=customer, is_ordered=False, quantity=quantity, guest_registered_merged=False)
            
           
        #updates guest cart when user is logged in
        if request.user.is_authenticated:
            try:
                deviceId = request.COOKIES['deviceId']
                guest_user = Customer.objects.get(name=deviceId)
                order_item = OrderItem.objects.get(product_id=slug, user=request.user, is_ordered=False)
                guest_order_item = OrderItem.objects.get(product_id=slug, user=guest_user, is_ordered=False)
            
                if guest_order_item:
                    guest_order_item.quantity = order_item.quantity
                    guest_order_item.guest_registered_merged = True
                    guest_order_item.save()
                    order_item.guest_registered_merged = True
                    order_item.save()
            except:
                guest_order_item = OrderItem.objects.create(product_id=slug, user=guest_user, is_ordered=False, quantity=order_item.quantity, guest_registered_merged =True)
                order_item.guest_registered_merged = True
                order_item.save()

        return redirect("product_detail", slug=slug)



# load cart
def cart(request):
    cart_template = loader.get_template('order/cart.html')
    customer = get_customer(request)

    order_items = OrderItem.objects.filter(user=customer, is_ordered=False)
    context ={
        'order_items':order_items,
    }

    return HttpResponse(cart_template.render(context, request))
    

#update cart
def update_cart(request, slug):
    cart_template = loader.get_template('order/cart.html') 
    customer = get_customer(request)
    print('customer', customer)
    if request.method == 'POST':
        update_quantity = escape(request.POST.get('update-quantity'))
    order_item = OrderItem.objects.get(product_id=slug, user=customer, is_ordered=False)
    if int(update_quantity) == 0 :
        order_item.delete()
    else:  

        order_item.quantity = update_quantity
        order_item.save()
    return redirect("cart")


def calculate_order_amount(request):
    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(user=request.user, is_ordered=False)
        order_total = 0
        if order_items:
            for item in order_items:
                order_total += item.product.price * item.quantity
                
        return int(order_total * 100 )
    

# checkout 
@login_required()
def checkout(request):
    checkout_template = loader.get_template('order/checkout.html')
    if request.user.is_authenticated:
            accountinfo = AccountInfo.objects.get(customer= request.user)
    order_items = OrderItem.objects.filter(user=request.user, is_ordered=False)
    order_total_price = round(calculate_order_amount(request)/100, 2)
    context = {
        'order_items': order_items,
        'accountinfo': accountinfo,
        'order_total_price' : order_total_price,
    }

    return HttpResponse(checkout_template.render(context, request)) 

@login_required()
def order_status(request):
    order_status_template = loader.get_template('order/order_status.html')
    payment_status = request.GET.get('redirect_status', '')
    context ={
        'payment_status': payment_status
    }
    return HttpResponse(order_status_template.render(context, request))



def create_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount= calculate_order_amount(request),
                currency='gbp',
                # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse(error=str(e)), 403





