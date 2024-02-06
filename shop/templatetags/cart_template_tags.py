from django import template
from urllib3 import request
from order.models import OrderItem
from order.views import get_customer
from django.template import RequestContext    



register = template.Library()

@register.filter
@register.simple_tag(takes_context = True)
def get_cart_count(context):
    request = context['request']
    customer = get_customer(request)
    
    order_items = OrderItem.objects.filter(user=customer, is_ordered=False)
    total_quantity = 0
    if order_items.exists():
        for item in order_items:
            total_quantity += item.quantity
    return total_quantity



    # return render_to_response(context_instance = RequestContext(request))