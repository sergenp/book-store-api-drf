from libraryfrontend.models import BaseModel
from commercebackend.models import OrderModel 
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ProtectedError

class Payment(BaseModel):
    transaction = models.TextField() # transaction ID for the blockhain
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL) # user of the payment
    order = models.ForeignKey(OrderModel, on_delete=models.PROTECT)
    success = models.BooleanField()
    
    def delete(self):
        if self.success:
            return super(Payment, self).delete()
        else:
            raise ProtectedError("Can't delete object, Payment isn't completed.")
    
    def hard_delete(self):
        if self.success:
            return super(Payment, self).hard_delete()
        else:
            raise ProtectedError("Can't delete object, Payment isn't completed.")
    
    def __str__(self):
        return f"{self.transaction} for order {self.order}, from user {self.user}"
    
class Invoice(BaseModel):
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT)
    order = models.ForeignKey(OrderModel, on_delete=models.PROTECT)
    status_code = models.CharField(max_length=3)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)    
    
    def __str__(self):
        return f"Order {self.order}'s invoice"