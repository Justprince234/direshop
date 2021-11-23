from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from .models import Item, OrderItem, Order, CheckoutAddress, Payment
from store.serializers import ItemSerializer, OrderItemSerializer, OrderSerializer, CheckoutAddressSerializer, PaymentSerializer

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from django.http import HttpResponse,JsonResponse
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class ListItemAPI(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = PageNumberPagination


class DetailItemAPI(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# @api_view(['GET'])
# def item_detail_api_view(request, slug):
#     """Lists the items by slug"""
#     if request.method == 'GET':
#         items = Item.objects.get(slug=slug)
#         serializer = ItemSerializer(items, many=True)
#         return JsonResponse(serializer.data, safe =False)

# Add to cart
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug )
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f"{item.item_name} quantity has updated.")
            return redirect("store:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, f"{item.item_name} has added to your cart.")
            return redirect("store:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, f"{item.item_name} has added to your cart")
        return redirect("store:order-summary")

# Remove from cart.
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug )
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            messages.info(request, f"{item.item_name} has been removed from your cart")
            return redirect("store:order-summary")
        else:
            messages.info(request, f"{item.item_name} not in your cart")
            return redirect("store:product", slug=slug)
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("store:product", slug = slug)

# Remove item from cart
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def reduce_quantity_item(request, slug):
    item = get_object_or_404(Item, slug=slug )
    order_qs = Order.objects.filter(
        user = request.user, 
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists() :
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, f"{item.item_name} quantity has updated")
            return redirect("store:order-summary")
        else:
            messages.info(request, f"{item.item_name} not in your cart")
            return redirect("store:order-summary")
    else:
        #add message doesn't have order
        messages.info(request, "You do not have an active order")
        return redirect("store:order-summary")


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def orderitem_api_view(request):
    
    if request.method == 'GET':
        items = OrderItem.objects.filter(owner=request.user,)
        serializer = OrderItemSerializer(items, many=True)
        return JsonResponse(serializer.data, safe =False)
    
    elif request.method == 'POST':
        owner = request.user
        data = JSONParser().parse(request)
        serializer = OrderItemSerializer(data = data)
 
        if serializer.is_valid():
            serializer.save(owner)
            return JsonResponse(serializer.data,status = 201)
        return JsonResponse(serializer.errors,status = 400)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def CheckoutAddress_api_view(request):
    
    if request.method == 'GET':
        items = CheckoutAddress.objects.filter(owner=request.user,)
        serializer = CheckoutAddressSerializer(items, many=True)
        return JsonResponse(serializer.data, safe =False)
    
    elif request.method == 'POST':
        owner = request.user
        data = JSONParser().parse(request)
        serializer = CheckoutAddressSerializer(data = data)
 
        if serializer.is_valid():
            serializer.save(owner)
            return JsonResponse(serializer.data,status = 201)
        return JsonResponse(serializer.errors,status = 400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ordersummary_api_view(request):
    
    if request.method == 'GET':
        items = Order.objects.filter(owner=request.user, ordered=False)
        serializer = OrderSerializer(items, many=True)
        return JsonResponse(serializer.data, safe =False)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def checkout_api_view(request):

    if request.method == 'GET':
        items = Order.objects.filter(owner=request.user, ordered=False)
        serializer = OrderSerializer(items, many=True)
        return JsonResponse(serializer.data, safe =False)
    
    elif request.method == 'POST':
        items = Order.objects.filter(owner=request.user, ordered=False)
        serializer = OrderSerializer(items, many=True)
        owner = request.user
        checkout_address = CheckoutAddress(
            user=request.user,
            street_address=serializer.validated_data['street_address'],
            apartment_address=serializer.validated_data['apartment_address'],
            country=serializer.validated_data['country'],
            zip=serializer.validated_data['zip']
        )
        checkout_address.save()
        items.checkout_address = checkout_address
        items.save()
        data = JSONParser().parse(request)
        serializer =OrderSerializer(data = data)
 
        if serializer.is_valid():
            serializer.save(owner)
            return JsonResponse(serializer.data,status = 201)
        return JsonResponse(serializer.errors,status = 400)
