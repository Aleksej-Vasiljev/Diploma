from django.contrib import admin
from .models import Product, Cart, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'created_at',
                    'country', 'lifespan', 'warranty')
    list_filter = ('category',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'product', 'quantity')

    def get_user(self, obj):
        return obj.cart.user

    get_user.short_description = 'User'