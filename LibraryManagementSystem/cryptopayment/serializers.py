from django.db import models
from libraryfrontend.serializers import LibraryBaseSerializer
from .models import Payment, Invoice

class PaymentSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = Payment
        exclude = LibraryBaseSerializer.Meta.exclude + ('btc_address_wif',)
    
class Invoice(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = Invoice