from django.contrib.auth.models import Permission, User
from rest_framework import serializers
from .models import AuthorModel, BookModel, CategoryModel, PublisherModel, BaseModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password','last_login', 'is_active', )

class LibraryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        exclude = ('is_test_data', 'created_on', 'modified_on', 'created_by', 'modified_by', 'deleted')

class BookSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = BookModel
#       exclude = LibraryBaseSerializer.Meta.exclude + ('id',)

class AuthorSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = AuthorModel
        
class CategorySerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = CategoryModel

class PublisherSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = PublisherModel
