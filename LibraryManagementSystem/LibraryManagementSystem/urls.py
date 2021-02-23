from django.contrib import admin
from django.urls import path, include 
from rest_framework import routers
from django.conf.urls.static import static
from libraryfrontend import views as library_views
from commercebackend import views as commerce_views
from cryptopayment import views as crypto_views
from cryptopayment.payment_gateway import create_payment_checker, move_payments

from . import settings
from rest_framework_jwt.views import obtain_jwt_token


router = routers.DefaultRouter()
router.register(r'author', library_views.AuthorView, 'author')
router.register(r'publisher', library_views.PublisherView, 'publisher')
router.register(r'book', library_views.BookView, 'book')
router.register(r'category', library_views.CategoryView, 'category')
router.register(r'user', library_views.UserView, 'user')
# commerce backend
router.register(r'cart', commerce_views.CartView, 'cart')
router.register(r'order', commerce_views.OrderView, 'order')
router.register(r'shipping', commerce_views.ShippingView, 'shipping')
# payment gate
router.register(r'payment', crypto_views.CreateQRPayment, 'payment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('register/',  library_views.RegisterView.as_view({'post' : 'create'})),
    path('login/', obtain_jwt_token)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# create the payment checker thread
create_payment_checker()
# move the payments back to my testnet wallet
#move_payments('tb1qe4f69mm056hqhhagphfqe5qp0wnggrxz3rn3nz')