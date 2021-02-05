import io
from django.conf import settings
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from commercebackend.models import CartModel
from .models import Payment
from .serializers import PaymentSerializer
# qr and bitcoin address generation
from bit import PrivateKeyTestnet
import qrcode
import uuid


class CreateQRPayment(viewsets.GenericViewSet,
                      viewsets.mixins.CreateModelMixin
                      ):
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = PaymentSerializer
    
    def create(self, request):
        # get the cart of the user 
        try:
            cart = CartModel.objects.get(user=request.user, bought=0)
        except CartModel.DoesNotExist:
            return Response(data={"detail" : "Can't create qr code for user's cart, it doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if the user alredy has a payment object created for the cart
        try:
            payment = Payment.objects.get(user=request.user, cart=cart, success=0)
            # if the user already has created a payment, return the payment's qr code
            with open(settings.MEDIA_ROOT / "payment_qr" / str(payment.qr_image), "rb") as img:
                return HttpResponse(img.read(), content_type="image/png")
        except Payment.DoesNotExist: # if there is no payment created
            # create a bitcoin adress for the payment
            key = PrivateKeyTestnet()
            # TODO rather than using 38K$ as the btc price, 
            # get the price from a server
            usd_to_btc = round(cart.total_price / 38000, 8)
            # create the qr code
            qr = qrcode.make(f"bitcoin:{key.address}?amount={usd_to_btc}")
            # save the image to media directory
            img_name = f"{uuid.uuid4().hex}.png"
            dir = settings.MEDIA_ROOT / "payment_qr" / img_name
            qr.save(dir)
            # create the payment
            payment = Payment.objects.create(btc_address_wif=key.to_wif(), 
                               user=request.user, cart=cart, success=0,
                               total_price=cart.total_price, total_price_btc = usd_to_btc,
                               qr_image=str(img_name))
            response = HttpResponse(content_type='image/png')
            qr.save(response, 'PNG')
            return response