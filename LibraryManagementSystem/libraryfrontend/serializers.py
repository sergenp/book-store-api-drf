from django.db import models
from django.db.models import base, fields
from rest_framework import serializers
from .models import AuthorModel, BookModel, CategoryModel, PublisherModel, BaseModel

class LibraryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        exclude = ('is_test_data', 'created_on', 'modified_on', 'created_by', 'modified_by', 'deleted')

class AuthorSerializer(LibraryBaseSerializer):
    
    class Meta(LibraryBaseSerializer.Meta):
        model = AuthorModel
#        exclude = LibraryBaseSerializer.Meta.exclude + ('id',)

class BookSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = BookModel

class CategorySerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = CategoryModel

class PublisherSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = PublisherModel
