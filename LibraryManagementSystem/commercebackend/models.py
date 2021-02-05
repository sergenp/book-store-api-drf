from django.utils.timezone import now
from django.db import models
from django.conf import settings
from libraryfrontend.models import BookModel, BaseModel

class ShippingModel(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField() # address of the shipping
    city = models.CharField(max_length=85) # city
    country = models.CharField(max_length=74) # country
    zipcode = models.CharField(max_length=12) # zipcode
    is_current = models.BooleanField(default=1)
    
    class Meta:
        unique_together = ('user', 'is_current') # a user can only have one current address
        

class CartModel(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField("CartItemModel")
    bought = models.BooleanField(default=0) # if the cart has been checkedout
    
    @property
    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.total_price
        return total
    
    def __str__(self):
        return f"User {self.user}'s Cart {self.id}"

class CartItemModel(BaseModel):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    
    @property
    def total_price(self):
        return self.book.price * self.amount
    
    def delete(self):
        # when deleting a cart item, we need to restore the store_amount of the book
        book = BookModel.objects.get(pk=self.book.id)
        book.store_amount += self.amount
        book.save()
        super(CartItemModel, self).delete()
        
    def __str__(self):
        return f"Cart {self.cart}'s Item {self.id} (Book {self.book})"

class OrderModel(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    shipping = models.ForeignKey(ShippingModel, on_delete=models.CASCADE)
    ordered_at = models.DateField(default=now)
    
    def __str__(self):
        return f"Order {self.id} of {self.cart}"
    