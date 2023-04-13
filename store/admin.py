from django.contrib import admin, messages

from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

from .models import *

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'LOW'),
            ('>=10', 'OK')
        ]

    def queryset(self, request, queryset):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)
        elif self.value() == '>=10':
            return queryset.filter(inventory__gte=10)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # fields = ['title', 'slug']
    search_fields = ['title']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_select_related = ['collection']
    list_per_page = 10
    list_filter = ['collection', 'last_update', InventoryFilter]

    def collection_title(self, product):
        return product.collection.title
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'LOW'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated.",
            messages.SUCCESS
        )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = ( reverse('admin:store_order_changelist') 
               + '?'
               + urlencode({
                'customer__id': customer.id
               }))
        return format_html('<a href={}>{}</a>', url, customer.orders_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = OrderItem
    min_num = 1
    max_num = 10
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    list_editable = ['payment_status']
    list_per_page = 10
    ordering = ['placed_at']
    list_select_related = ['customer']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin): 
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist') 
               + "?"
               + urlencode({
                'collection__id': str(collection.id)
               }))
        return format_html('<a href={}>{}</a>', url, collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )
    