from django_filters import rest_framework as filters
from rest_framework import viewsets
from .serializers import AuthorSerializer, BookSerializer, CategorySerializer, PublisherSerializer
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
