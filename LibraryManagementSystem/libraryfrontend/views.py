from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from .models import (
    AuthorModel,
    BookModel,
    BookRatingModel,
    CategoryModel,
    PublisherModel,
)
from .serializers import (
    AuthorSerializer,
    BookRatingSerializer,
    BookSerializer,
    CategorySerializer,
    PublisherSerializer,
    RegisterSerializer,
    UserSerializer,
)

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class AuthorView(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    queryset = AuthorModel.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("name",)
    search_fields = ("name",)
    ordering = ("id",)


class BookView(viewsets.ReadOnlyModelViewSet):
    serializer_class = BookSerializer
    queryset = BookModel.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ("name", "author", "category", "publisher")
    ordering_fields = ("price", "name", "published_date", "store_amount", "pages")
    search_fields = ("name",)
    ordering = ("id",)


class BookRatingView(viewsets.ModelViewSet):
    serializer_class = BookRatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = BookRatingModel.objects.all()
    ordering = ("id",)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = BookModel.objects.get(pk=request.data["book"])
        book_rating, _ = BookRatingModel.objects.get_or_create(book=book, user=request.user)
        book_rating.rating = request.data["rating"]
        book_rating.save()
        return Response(
            data={
                **serializer.data,
                **{"detail": f"Successfully rated {book.name} {book_rating.rating}"},
            }
        )


class CategoryView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("name",)
    search_fields = ("name",)
    ordering = ("id",)


class PublisherView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PublisherSerializer
    queryset = PublisherModel.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("name",)
    search_fields = ("name",)
    ordering = ("id",)


class UserView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
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
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": token,
            }
        )
