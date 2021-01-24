from django.db import models
from django.conf import settings
from django.utils.timezone import now
from libraryfrontend.models import BookModel, BaseModel

class ShippingModel(BaseModel):
    address = models.TextField() # address of the shipping
    city = models.CharField(max_length=85) # city
    country = models.CharField(max_length=74) # country
    zipcode = models.CharField(max_length=12) # zipcode

class CartModel(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    shipping = models.ForeignKey(ShippingModel, on_delete=models.CASCADE)
    items = models.ManyToManyField(BookModel, through="CartItemModel")
    bought = models.BooleanField() # if the cart has been checkout

    def __str__(self):
        return f"User {self.user}'s Cart {self.id}"

class CartItemModel(BaseModel):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart {self.cart}'s Item {self.id} (Book {self.book})"

class OrderModel(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Order {self.id} of {self.cart}"
    