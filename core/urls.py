from django.urls import path, re_path
from .views import MainPageView, ProductDetailView, CartView, AddToCartView, CartDetailsAPI, ShopView, RemoveFromCartView
from django.conf import settings
from django.conf.urls.static import static
from django.utils.text import slugify

app_name = 'core'
urlpatterns = [
	path('', MainPageView.as_view(), name='main'),
	re_path(r'product/(?P<product_id>[A-Za-z0-9]{20})/[A-Za-z0-9-]+', ProductDetailView.as_view(), name='product-page'),
	path('cart/', CartView.as_view(), name='cart'),
	path('shop/', ShopView.as_view(), name='shop'),

	# API
	path('cart/endpoint', CartDetailsAPI.as_view(), name='cart-details-api'),
	path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
	path('remove-from-cart/', RemoveFromCartView.as_view(), name='remove-from-cart'),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)