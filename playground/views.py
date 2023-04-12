from django.shortcuts import render
from django.db.models import Q, F
from store.models import Collection, Product

def say_hello(request):
    # collection = Collection.objects.create(title='Lemon', featured_product_id=1)
    # collection = Collection.objects.filter(title='Lemon').update(featured_product_id=2)
    # collection = Collection.objects.filter(featured_product_id__isnull = True).update(featured_product_id=1)
    # Collection.objects.filter(featured_product_id=2).delete()

    query_set = Collection.objects.raw('SELECT * FROM store_product')
    return render(request, 'hello.html', {'name': 'Wajahat', 'products': query_set })
 