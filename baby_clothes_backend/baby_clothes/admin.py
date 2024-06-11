from django.contrib import admin
from .models import Person, Category, Product, Customer, Order, OrderItem, Review, Cart, CartItem

# Register your models here.
admin.site.register(Person)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
