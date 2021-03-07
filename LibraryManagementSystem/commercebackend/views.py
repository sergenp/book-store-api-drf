from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from .models import CartItemModel, CartModel, OrderModel, ShippingModel, BookModel
from .serializers import CartSerializer, OrderSerializer, ShippingSerializer
from libraryfrontend.serializers import BookSerializer

class CartView(viewsets.GenericViewSet,
               viewsets.mixins.RetrieveModelMixin,
               viewsets.mixins.CreateModelMixin,
               viewsets.mixins.DestroyModelMixin):

    serializer_class = CartSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    pagination_class = None
    
    def get(self, request):
        try:
            serialized = CartSerializer(CartModel.objects.get(user=request.user, bought=0), context={'request': request})
            return Response(data=serialized.data, status=status.HTTP_200_OK)
        except CartModel.DoesNotExist:
            return Response(data={"detail" : "There is no active cart of the user"}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        # get the cart of the user from the database if it exists, or create a new one
        cart, _ = CartModel.objects.get_or_create(user=request.user, bought=0)
        # if the item_serializer is valid, let's create a cart item and add it to our cart
        # get the requested book
        try:
            book = BookModel.objects.get(pk=request.data.get("book", -1))
        except BookModel.DoesNotExist:
            return Response(data={'detail' : f"Book couldn't be found"}, status=status.HTTP_400_BAD_REQUEST)
        
        serialized_book = BookSerializer(book, context={'request': request}).data
        cart_item, created = CartItemModel.objects.get_or_create(cart=cart, book=book)
        
        if not created:
            # if the cart item isn't created, and there is enough book in the store increase the amount of it
            if book.store_amount > 0:
                cart_item.amount += 1
                book.store_amount -= 1
                book.save()
                cart_item.save()
                cart.items.add(cart_item.id) # add func immediately updates the database
                return Response(data={"detail" : f"Increased {book} amount to {cart_item.amount}"},
                                status=status.HTTP_201_CREATED, headers=self.headers)
            else:
                return Response(data={"detail" : f"There is no more {book} left in the store"},
                                status=status.HTTP_400_BAD_REQUEST, headers=self.headers)                
        else:
            cart.items.add(cart_item.id) # add function immediately updates the database
            return Response(data={"detail" : f"Added {book} to Cart"},
                            status=status.HTTP_201_CREATED, headers=self.headers)
    
    def delete(self, request):
        try:
            cart = CartModel.objects.get(user=request.user.id, bought=0)
        except CartModel.DoesNotExist:
            return Response(data={"detail" : "There is no active cart of the user"}, status=status.HTTP_400_BAD_REQUEST)
            
        #if the request has book id attached to it, remove X amount of books from the cart
        if request.data.get("book", ""):
            book_id = request.data["book"]
            try:
                book = BookModel.objects.get(pk=book_id) 
            except BookModel.DoesNotExist:
                return Response(data={"detail" : f"Book {book_id} is not found"})
            
            serialized_book = BookSerializer(book, context={'request': request}).data
            try:
                cart_item = CartItemModel.objects.get(cart=cart, book=book_id)
                delete_amount = int(request.data.get("delete_amount", 1))
                # if the amount of cart_item is bigger than zero and delete_amount,
                # reduce the item amount in the cart, otherwise delete the cart_item 
                if cart_item.amount > 0 and cart_item.amount > delete_amount:
                    cart_item.amount -= delete_amount
                    book.store_amount += delete_amount
                    cart_item.save()
                    book.save()
                    return Response(data={"detail" : f"Removed {delete_amount} {book.name} from Cart"})
                else:
                    cart_item.delete(request.user) # deleting the cart item restores book's store amount
                    return Response(data={"detail" : f"Removed {book.name} from Cart"})
                    
            except CartItemModel.DoesNotExist:
                return Response(data={"detail" : f"Book {book_id} is not in the Cart"}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            #otherwise delete the cart entirely
            cart.delete(request.user) # this soft deletes the card because of the basemanager
            return Response(data={"detail" : "Cart has been deleted"}, status=status.HTTP_200_OK)
        
        
class OrderView(viewsets.GenericViewSet,
                viewsets.mixins.RetrieveModelMixin,
                viewsets.mixins.ListModelMixin):
    
    serializer_class = OrderSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    pagination_class = None
    
    def get_queryset(self):
        return OrderModel.objects.all().filter(user=self.request.user.id)

    
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
        return ShippingModel.objects.all().filter(user=self.request.user.id, is_current=1)