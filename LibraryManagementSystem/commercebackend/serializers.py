from django.contrib.auth.models import Permission, User
from rest_framework import serializers
from libraryfrontend.serializers import LibraryBaseSerializer
from .models import CartItemModel, CartModel, OrderModel, ShippingModel

class ShippingSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = ShippingModel

class OrderSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = OrderModel

class CartSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = CartModel

class CartItemSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = CartItemModel

