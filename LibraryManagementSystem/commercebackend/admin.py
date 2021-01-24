from django.contrib import admin
from .models import CartItemModel, CartModel, OrderModel, ShippingModel

# Register your models here.
admin.site.register(CartItemModel)
admin.site.register(CartModel)
admin.site.register(OrderModel)
admin.site.register(ShippingModel)

