from django.contrib.auth.models import User
from rest_framework import serializers
from .models import AuthorModel, BookModel, CategoryModel, PublisherModel, BaseModel
from django.contrib.auth import password_validation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate_password(self, value):
        password_validation.validate_password(value)
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)        
            
class LibraryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        exclude = ('is_test_data', 'created_at', 'modified_at', 'created_by', 'modified_by', 'deleted_at', 'deleted_by')
        depth = 1

class AuthorSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = AuthorModel
        
class CategorySerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = CategoryModel

class PublisherSerializer(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = PublisherModel

class BookSerializer(LibraryBaseSerializer):
    # adding serializers manually ensured that base serializer is being called on each request,
    # otherwise every data about the foreign keys are shown
    # this way exclude field on the base is obeyed
    author = AuthorSerializer(many=False, read_only=True) 
    category = CategorySerializer(many=False, read_only=True)
    publisher = PublisherSerializer(many=False, read_only=True)
    class Meta(LibraryBaseSerializer.Meta):
        model = BookModel
