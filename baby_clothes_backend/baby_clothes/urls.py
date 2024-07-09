from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name = "index"),
    path('signup',views.sign_in, name = 'signup'),
    path('login',views.log_in, name = 'login'),
    path('logout', views.log_out, name = 'logout'),
    path('contact',views.contact, name = 'contact'),
    path('shop',views.shop, name = 'shop'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('update_cart/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('about',views.about, name = 'about'),
    path('category',views.category, name = 'category'),
    path('add-product',views.product,name = 'add-product')
]
