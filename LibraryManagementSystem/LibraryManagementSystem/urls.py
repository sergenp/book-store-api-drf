from django.contrib import admin
from django.urls import path, include 
from rest_framework import routers
from django.conf.urls.static import static
from libraryfrontend import views as library_views
from commercebackend import views as commerce_views

from . import settings
from rest_framework_jwt.views import obtain_jwt_token


router = routers.DefaultRouter()
router.register(r'author', library_views.AuthorView, 'author')
router.register(r'publisher', library_views.PublisherView, 'publisher')
router.register(r'book', library_views.BookView, 'book')
router.register(r'category', library_views.CategoryView, 'category')
router.register(r'user', library_views.UserView, 'user')
router.register(r'cart', commerce_views.CartView, 'cart')
router.register(r'order', commerce_views.OrderView, 'order')
router.register(r'shipping', commerce_views.ShippingView, 'shipping')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('login/', obtain_jwt_token)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

