from django.contrib import admin

from store.admin import ProductAdmin
from tags.models import TaggedItem
from store.models import Product
from django.contrib.contenttypes.admin import GenericTabularInline

class TagInLine(GenericTabularInline):
    model = TaggedItem
    extra = 0
    min_num = 1
    autocomplete_fields = ['tag']


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInLine]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)