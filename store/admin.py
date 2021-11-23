from django.contrib import admin

from .models import (
    Item, 
    OrderItem, 
    Order,
    CheckoutAddress,
    Payment
)

admin.site.site_header = 'Direshop777'
admin.site.site_title = 'Direshop777'
admin.site.index_title = 'Direshop777 Admin'

class ItemAdmin(admin.ModelAdmin):

    list_display = ('id', 'item_name', 'category', 'description', 'price', 'membership_price')
    prepopulated_fields = {"slug": ("item_name",)}
    list_display_links = ('id', 'item_name')
    search_fields = ('item_name',)
    list_per_page = 25

admin.site.register(Item, ItemAdmin)

class OrderItemAdmin(admin.ModelAdmin):

    list_display = ('id', 'owner', 'item', 'quantity', 'ordered')
    list_display_links = ('id', 'owner')
    search_fields = ('owner',)
    list_per_page = 25

admin.site.register(OrderItem, OrderItemAdmin)

class OrderAdmin(admin.ModelAdmin):

    list_display = ('id', 'owner', 'ordered_date', 'ordered', 'checkout_address', 'payment')
    list_display_links = ('id', 'owner')
    search_fields = ('owner',)
    list_per_page = 25

admin.site.register(Order, OrderAdmin)

class CheckoutAddressAdmin(admin.ModelAdmin):

    list_display = ('id', 'owner', 'apartment_address', 'street_address', 'state', 'country', 'zip')
    list_display_links = ('id', 'owner')
    search_fields = ('owner',)
    list_per_page = 25

admin.site.register(CheckoutAddress, CheckoutAddressAdmin)

class PaymentAdmin(admin.ModelAdmin):

    list_display = ('id', 'owner', 'paypal_id', 'amount')
    list_display_links = ('id', 'owner')
    search_fields = ('owner',)
    list_per_page = 25

admin.site.register(Payment, PaymentAdmin)