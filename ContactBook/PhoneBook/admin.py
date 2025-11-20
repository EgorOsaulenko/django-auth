from django.contrib import admin
from .models import Contact, Product, Basket, FeaturedProduct, TopProduct


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'user')
    list_filter = ('user',)
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'rating', 'count', 'is_new', 'created_at')
    list_filter = ('is_new', 'rating', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_new', 'count', 'rating')


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'product__name')


@admin.register(FeaturedProduct)
class FeaturedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order')
    list_filter = ('order',)
    search_fields = ('product__name',)
    list_editable = ('order',)


@admin.register(TopProduct)
class TopProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order')
    list_filter = ('order',)
    search_fields = ('product__name',)
    list_editable = ('order',)
