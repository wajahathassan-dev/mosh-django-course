from django.shortcuts import render
from django.db.models import Q, F
from store.models import Product, OrderItem

def say_hello(request):
    query_set = OrderItem.objects.values_list('product_id', 'product__title').order_by('product__title')
    return render(request, 'hello.html', {'name': 'Wajahat', 'products': list(query_set)}) 
 