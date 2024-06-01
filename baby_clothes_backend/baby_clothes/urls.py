from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name = "index"),
    path('signup',views.sign_in, name = 'signup'),
    path('login',views.log_in, name = 'login'),
    path('logout', views.log_out, name = 'logout'),
    path('contact',views.contact, name = 'contact'),
    path('shop',views.shop, name = 'shop'),
    path('aout',views.about, name = 'about')
]