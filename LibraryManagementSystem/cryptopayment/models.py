from commercebackend.models import CartModel, OrderModel, ShippingModel
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ProtectedError
from libraryfrontend.models import BaseModel


class Payment(BaseModel):
    btc_address_wif = models.TextField()  # created wif of the btc adress for the payment
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL
    )  # user of the payment
    cart = models.ForeignKey(CartModel, on_delete=models.PROTECT)  # cart of the user
    shipping = models.ForeignKey(ShippingModel, on_delete=models.PROTECT)  # shipping address
    success = models.BooleanField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price_btc = models.DecimalField(max_digits=10, decimal_places=8)
    qr_image = models.ImageField()

    def delete(self):
        if self.success:
            return super(Payment, self).delete()
        else:
            raise ProtectedError("Can't delete object, Payment isn't completed.")

    def hard_delete(self):
        raise ProtectedError(
            "Payment objects must not be hard deleted, they include the wif of the bitcoin address, doing so might lose you access to the wallet"
        )

    def __str__(self):
        return f"Payment created for {self.cart} for user {self.user}"


class Invoice(BaseModel):
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT)
    order = models.ForeignKey(OrderModel, on_delete=models.PROTECT)
    status_code = models.CharField(max_length=3)

    def __str__(self):
        return f"Order {self.order}'s invoice"
