import uuid

import qrcode

# qr and bitcoin address generation
from bit import PrivateKeyTestnet
from commercebackend.models import CartModel, ShippingModel
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Payment


class CreateQRPayment(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        # get the cart of the user
        try:
            cart = CartModel.objects.get(user=request.user, bought=0)
        except CartModel.DoesNotExist:
            return Response(
                data={"detail": "Can't create qr code for user's cart, it doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # get the active Shipping address from the user, this is to check if there is a shipping address
        # active for the user, if it is not, user should add a shipping address before creating a payment qr
        # if user doesn't create a shipping address, some weird things might happen in the payment_gateway's create_order function
        try:
            shipping = ShippingModel.objects.get(user=request.user, is_current=1)
        except ShippingModel.DoesNotExist:
            return Response(
                data={
                    "detail": "Can't create qr code for the payment, user doesn't have a shipping address"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # check if the user alredy has a payment object created for the cart
        try:
            payment = Payment.objects.get(user=request.user, cart=cart, success=0)
            # if the user already has created a payment, return the payment's qr code
            with open(settings.MEDIA_ROOT / "payment_qr" / str(payment.qr_image), "rb") as img:
                return HttpResponse(img.read(), content_type="image/png")
        except Payment.DoesNotExist:  # if there is no payment created
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
            payment = Payment.objects.create(
                btc_address_wif=key.to_wif(),
                user=request.user,
                cart=cart,
                success=0,
                total_price=cart.total_price,
                total_price_btc=usd_to_btc,
                qr_image=str(img_name),
                shipping=shipping,
            )
            response = HttpResponse(content_type="image/png")
            qr.save(response, "PNG")
            return response
