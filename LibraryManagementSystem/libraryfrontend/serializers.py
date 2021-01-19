from rest_framework import serializers
from .models import AuthorModel, BookModel, CategoryModel, PublisherModel

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorModel
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublisherModel
        fields = '__all__'
