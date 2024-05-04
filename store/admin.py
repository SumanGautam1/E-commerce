from django.contrib import admin

# Register your models here.
from .models import Product, CartItem, Category, Customer

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Category)
admin.site.register(Customer)