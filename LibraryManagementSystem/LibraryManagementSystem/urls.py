# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from libraryfrontend import views

router = routers.DefaultRouter()
router.register(r'author', views.AuthorView, 'author')
router.register(r'publisher', views.PublisherView, 'publisher')
router.register(r'book', views.BookView, 'book')
router.register(r'category', views.CategoryView, 'category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
