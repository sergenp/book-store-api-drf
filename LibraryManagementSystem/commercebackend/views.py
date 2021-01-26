from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .models import CartItemModel, CartModel, OrderModel, ShippingModel, BookModel
from .serializers import CartItemSerializer, CartSerializer, OrderSerializer, ShippingSerializer

class CartView(viewsets.ModelViewSet):

    serializer_class = CartSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    pagination_class = None
    
    def get_queryset(self):
        return CartModel.objects.all().filter(user=self.request.user.id, deleted=0, bought=0)

    def create(self, request, *args, **kwargs):
        # get the cart of the user from the database if it exists, or create a new one
        cart, _ = CartModel.objects.get_or_create(user=self.request.user.id, deleted=0, bought=0)
        cart_item_serializer = CartItemSerializer(data=request.data)
        cart_item_serializer.is_valid(raise_exception=True)
        # if the item_serializer is valid, let's create a cart item and add it to our cart
        # get the requested book
        try:
            book = BookModel.objects.get(pk=request.data["book"])
        except BookModel.DoesNotExist:
            raise ParseError(detail=f"Book with id {request.data['book']} couldn't be found")
        
        cart_item, created = CartItemModel.objects.get_or_create(cart=cart, book=book)
        if not created:
            # if the cart item isn't created, and there is enough book in the store increase the amount of it
            if book.store_amount > cart_item.amount:
                cart_item.amount += 1
                book.store_amount -= 1
                book.save()
                cart_item.save()
                cart.items.add(book.id) # add immediately updates the database
                return Response(data={"detail" : f"Increased {book} amount to {cart_item.amount}"}, status=status.HTTP_201_CREATED, headers=self.headers)
            else:
                return Response(data={"detail" : f"There is no more {book} left in the store"}, status=status.HTTP_400_BAD_REQUEST, headers=self.headers)                
        else:
            cart.items.add(book.id) # add function immediately updates the database
            return Response(data={"detail" : f"Added {book} to {cart}"}, status=status.HTTP_201_CREATED, headers=self.headers)
            
        
class OrderView(viewsets.GenericViewSet,
                viewsets.mixins.CreateModelMixin,
                viewsets.mixins.RetrieveModelMixin,
                viewsets.mixins.ListModelMixin):
    
    serializer_class = OrderSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    pagination_class = None
    
    def get_queryset(self):
        return OrderModel.objects.all().filter(user=self.request.user.id, deleted=0)
    
class ShippingView(viewsets.GenericViewSet,
                   viewsets.mixins.CreateModelMixin,
                   viewsets.mixins.DestroyModelMixin,
                   viewsets.mixins.RetrieveModelMixin,
                   viewsets.mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = ShippingSerializer
    pagination_class = None
    
    def get_queryset(self):
        return ShippingModel.objects.all().filter(user=self.request.user.id, deleted=0)