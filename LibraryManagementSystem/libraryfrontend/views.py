from django.contrib.auth.models import Permission, User
from django.http.response import JsonResponse
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import AuthorSerializer, BookSerializer, CategorySerializer, PublisherSerializer, UserSerializer
from .models import AuthorModel, BookModel, CategoryModel, PublisherModel

class AuthorView(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    queryset = AuthorModel.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("name",)

class BookView(viewsets.ReadOnlyModelViewSet):
    serializer_class = BookSerializer
    queryset = BookModel.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("name", "author", "category", "publisher")
    
class CategoryView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("name",)

class PublisherView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PublisherSerializer
    queryset = PublisherModel.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("name",)

class UserView(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    
    def get(self, request, format=None):
        content = {
            'user' : unicode(request.user),
            'auth' : unicode(request.auth)
        }
        return JsonResponse(content)
        
        
        
        