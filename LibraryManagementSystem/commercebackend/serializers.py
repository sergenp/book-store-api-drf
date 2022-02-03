from libraryfrontend.serializers import BookSerializer, LibraryBaseSerializer
from rest_framework import serializers

from .models import CartItemModel, CartModel, OrderModel, ShippingModel


class ShippingSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = ShippingModel
        depth = 0


class CartItemSerializer(LibraryBaseSerializer):
    book = BookSerializer(many=False)

    class Meta(LibraryBaseSerializer.Meta):
        model = CartItemModel
        depth = 0


class CartSerializer(LibraryBaseSerializer):
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    class Meta(LibraryBaseSerializer.Meta):
        model = CartModel
        depth = 0

    def get_total_price(self, obj):
        return obj.total_price


class OrderSerializer(LibraryBaseSerializer):
    cart = CartSerializer(many=False)
    shipping = ShippingSerializer(many=False)

    class Meta(LibraryBaseSerializer.Meta):
        model = OrderModel
        depth = 0
