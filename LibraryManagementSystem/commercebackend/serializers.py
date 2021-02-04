from libraryfrontend.serializers import LibraryBaseSerializer
from .models import CartItemModel, CartModel, OrderModel, ShippingModel

class ShippingSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = ShippingModel
        depth = 0

class OrderSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = OrderModel
        depth = 0

class CartSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = CartModel
        depth = 0
        
class CartItemSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = CartItemModel
        depth = 0
