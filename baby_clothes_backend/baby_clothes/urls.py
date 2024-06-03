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
    path('about',views.about, name = 'about'),
    path('category',views.category, name = 'category'),
    path('add-product',views.product,name = 'add-product')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)