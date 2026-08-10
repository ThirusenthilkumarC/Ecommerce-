from django.contrib import admin
from .models import (
    Category, Product, CustomerProfile, Cart, CartItem,
    Wishlist, Order, OrderItem, ContactMessage, NewsletterSubscriber, Testimonial
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "category", "brand", "price",
        "discount_price", "stock", "status", "featured", "is_deal", "is_active"
    )
    list_filter = ("status", "category", "brand", "featured", "is_deal", "is_active")
    search_fields = ("name", "brand", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("price", "discount_price", "stock", "featured", "is_deal", "is_active")
    ordering = ("-id",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "price", "quantity", "subtotal")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number", "full_name", "email", "total_amount",
        "payment_method", "payment_status", "order_status", "created_at"
    )
    list_filter = ("order_status", "payment_status", "payment_method", "created_at")
    search_fields = ("order_number", "first_name", "last_name", "email", "phone")
    list_editable = ("order_status", "payment_status")
    inlines = [OrderItemInline]
    ordering = ("-created_at",)


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "city", "state", "country", "created_at")
    search_fields = ("user__username", "user__email", "phone", "city")


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "session_key", "get_total_items", "get_grand_total", "created_at")
    inlines = [CartItemInline]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "session_key", "product", "created_at")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_editable = ("is_read",)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("email",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role_or_title", "rating", "is_active", "created_at")
    list_filter = ("rating", "is_active")
    list_editable = ("is_active",)