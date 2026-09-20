from django.contrib import admin
from .models import (
    Category, Product, ProductImage, ProductAttribute,
    Coupon, ProductCoupon, CategoryCoupon,
    Review, Cart, CartItem,
    Order, OrderItem, Payment
)
from taggit.admin import TagAdmin


# Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


# Product & Related
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_feature')


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1
    fields = ('key', 'value')


@admin.register(Product)
class ProductAdmin(TagAdmin):
    list_display = ('name', 'sku', 'category', 'price',
                    'stock', 'is_available', 'created_at')
    list_filter = ('is_available', 'category', 'tags')
    search_fields = ('name', 'sku', 'description')
    inlines = [ProductImageInline, ProductAttributeInline]
    prepopulated_fields = {'slug': ('name',)}


# Coupon
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value',
                    'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'discount_type', 'start_date')
    search_fields = ('code', 'description')


@admin.register(ProductCoupon)
class ProductCouponAdmin(admin.ModelAdmin):
    list_display = ('product', 'coupon')
    search_fields = ('product__name', 'coupon__code')


@admin.register(CategoryCoupon)
class CategoryCouponAdmin(admin.ModelAdmin):
    list_display = ('category', 'coupon')
    search_fields = ('category__name', 'coupon__code')


# Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at', 'updated_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__email', 'comment')


# Cart
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'updated_at')
    inlines = [CartItemInline]
    list_filter = ('updated_at',)
    search_fields = ('user__email',)


# Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'id')
    inlines = [OrderItemInline]


# Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'method',
                    'status', 'transaction_id', 'created_at')
    list_filter = ('status', 'method', 'created_at')
    search_fields = ('order__id', 'transaction_id')
