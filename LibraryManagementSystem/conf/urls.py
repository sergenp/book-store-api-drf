from commercebackend import views as commerce_views
from cryptopayment import views as crypto_views
from cryptopayment.payment_gateway import create_payment_checker, move_payments
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from libraryfrontend import views as library_views
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from . import settings

router = routers.DefaultRouter()
router.register(r"author", library_views.AuthorView, "author")
router.register(r"publisher", library_views.PublisherView, "publisher")
router.register(r"book", library_views.BookView, "book")
router.register(r"bookrating", library_views.BookRatingView, "bookrating")
router.register(r"category", library_views.CategoryView, "category")
router.register(r"user", library_views.UserView, "user")
# commerce backend
router.register(r"cart", commerce_views.CartView, "cart")
router.register(r"order", commerce_views.OrderView, "order")
router.register(r"shipping", commerce_views.ShippingView, "shipping")
# payment gate
router.register(r"payment", crypto_views.CreateQRPayment, "payment")

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/", include(router.urls)),
        path("register/", library_views.RegisterView.as_view({"post": "create"})),
        path("login/", obtain_jwt_token),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
