from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import AuthorSerializer, BookSerializer, CategorySerializer, PublisherSerializer, UserSerializer
from .models import AuthorModel, BookModel, CategoryModel, PublisherModel

class AuthorView(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    queryset = AuthorModel.objects.all().filter(deleted=0)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("name",)

class BookView(viewsets.ReadOnlyModelViewSet):
    serializer_class = BookSerializer
    queryset = BookModel.objects.all().filter(deleted=0)
    filter_backends = (DjangoFilterBackend, OrderingFilter, )
    filterset_fields = ("name", "author", "category", "publisher")
    ordering_fields = ("price", "name", "published_date", "store_amount", "pages")
    
class CategoryView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all().filter(deleted=0)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("name",)

class PublisherView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PublisherSerializer
    queryset = PublisherModel.objects.all().filter(deleted=0)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("name",)

class UserView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = UserSerializer
    pagination_class = None
    
    def get_queryset(self):
        return User.objects.all().filter(pk=self.request.user.id)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)

        return super(UserView, self).get_permissions()
    