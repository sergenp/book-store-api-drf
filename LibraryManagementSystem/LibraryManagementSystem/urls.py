# backend/urls.py
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include 
from rest_framework import routers
from libraryfrontend import views

from rest_framework_jwt.views import obtain_jwt_token


router = routers.DefaultRouter()
router.register(r'author', views.AuthorView, 'author')
router.register(r'publisher', views.PublisherView, 'publisher')
router.register(r'book', views.BookView, 'book')
router.register(r'category', views.CategoryView, 'category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    url(r'^api-token-auth/', obtain_jwt_token)
]
