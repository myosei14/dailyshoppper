from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Product
from django.contrib import messages


# index class
class Index(View):
    index_template = 'shop/index.html'

    def get(self, request):
        return render(request, self.index_template)


def shop(request):
    shop_template = loader.get_template('shop/shop.html')

    product_category_1 = Product.objects.filter(category='1')
    product_category_2 = Product.objects.filter(category='2')
    product_category_3 = Product.objects.filter(category='3')
    product_category_4 = Product.objects.filter(category='4')

    context = {
        'product_category_1': product_category_1,
        'product_category_2': product_category_2,
        'product_category_3': product_category_3,
        'product_category_4': product_category_4
    }

    return HttpResponse(shop_template.render(context, request))


def product_detail(request, slug):
    try:
        product = Product.objects.get(id=slug)
    except:
        print('No product found')
        messages.error(request, 'No product found')
        product = ''
    context = {
        'product': product,

    }
    product_detail_template = 'shop/product_detail.html'

    return render(request, product_detail_template, context)


