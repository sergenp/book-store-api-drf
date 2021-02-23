from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import AuthorSerializer, BookSerializer, CategorySerializer, PublisherSerializer, RegisterSerializer, UserSerializer
from .models import AuthorModel, BookModel, CategoryModel, PublisherModel
from rest_framework_jwt.settings import api_settings


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class AuthorView(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    queryset = AuthorModel.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("name",)
    search_fields = ('name',)
    ordering = ("id", )
    
class BookView(viewsets.ReadOnlyModelViewSet):
    serializer_class = BookSerializer
    queryset = BookModel.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ("name", "author", "category", "publisher")
    ordering_fields = ("price", "name", "published_date", "store_amount", "pages")
    search_fields = ('name',)
    ordering = ("id", )
    
class CategoryView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("name",)
    search_fields = ('name',)
    ordering = ("id", )

class PublisherView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PublisherSerializer
    queryset = PublisherModel.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("name",)
    search_fields = ('name',)
    ordering = ("id", )
    
class UserView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = UserSerializer
    pagination_class = None
    
    def get_queryset(self):
        return User.objects.all().filter(pk=self.request.user.id)

class RegisterView(viewsets.ModelViewSet):
   serializer_class = RegisterSerializer
   get_queryset = User.objects.all()
   permission_classes = (AllowAny,)

   def create(self, request, *args, **kwargs):
       serializer = self.get_serializer(data=request.data)
       serializer.is_valid(raise_exception=True)
       user = serializer.save()
       payload = jwt_payload_handler(user)
       token = jwt_encode_handler(payload)
       return Response(
           data={
               "user": UserSerializer(user,context=self.get_serializer_context()).data,
               "token" : token
               })