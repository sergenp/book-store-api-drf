from django.shortcuts import render
from rest_framework import viewsets
from .serializers import AuthorSerializer, BookSerializer, CategorySerializer, PublisherSerializer
from .models import AuthorModel, BookModel, CategoryModel, PublisherModel

class AuthorView(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = AuthorModel.objects.all()

class BookView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = BookModel.objects.all()

class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()

class PublisherView(viewsets.ModelViewSet):
    serializer_class = PublisherSerializer
    queryset = PublisherModel.objects.all()