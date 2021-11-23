from django.urls import path
from .views import (
    ListItemAPI,
    DetailItemAPI,
    remove_from_cart,
    reduce_quantity_item,
    add_to_cart,
    ordersummary_api_view,
    orderitem_api_view,
    CheckoutAddress_api_view,
    checkout_api_view,
)

app_name = 'store'

urlpatterns = [
    path('items/', ListItemAPI.as_view()),
    path('order-summary/', ordersummary_api_view,name='order-summary'),
    path('item/<str:slug>/', DetailItemAPI.as_view()),
    path('add-to-cart/<str:slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<str:slug>/', remove_from_cart, name='remove-from-cart'),
    path('reduce-quantity-item/<str:slug>/', reduce_quantity_item, name='reduce-quantity-item'),
    path('ordered-item/<str:slug>/', orderitem_api_view, name='ordered-item'),
    path('checkout/<str:slug>/',checkout_api_view, name='checkout'),
    path('checkout-address/<str:slug>/', CheckoutAddress_api_view, name='checkout-address'),
]