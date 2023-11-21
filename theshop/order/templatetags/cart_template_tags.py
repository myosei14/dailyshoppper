from django import template
from order.models import OrderItem

register = template.Library()

@register.filter
def get_cart_count(user):
    
    if user.is_authenticated:
        order_items = OrderItem.objects.filter(user=user, is_ordered=False)
        total_quantity = 0
        if order_items.exists():
            for item in order_items:
                total_quantity += item.quantity
            return total_quantity
    return 0