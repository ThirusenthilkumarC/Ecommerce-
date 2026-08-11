from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from decimal import Decimal
import uuid


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, default="fa-mobile-screen", help_text="FontAwesome icon class")
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    image_url = models.URLField(max_length=800, blank=True, null=True)
    description = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure unique slug
            orig_slug = self.slug
            count = 1
            while Category.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{orig_slug}-{count}"
                count += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def product_count(self):
        return self.products.filter(is_active=True).count()

    @property
    def get_image_url(self):
        if self.image_url:
            return self.image_url
        if self.image:
            return self.image.url
        return "https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=500&auto=format&fit=crop&q=80"


class Product(models.Model):
    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Out of Stock", "Out of Stock"),
    ]

    # Core existing fields
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default="No Description")
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    image_url = models.URLField(max_length=800, blank=True, null=True, help_text="Direct online image URL (Unsplash, CDN, etc.)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Available")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Enhanced fields
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    brand = models.CharField(max_length=100, blank=True, default="TechBrand")
    stock = models.IntegerField(default=15)
    featured = models.BooleanField(default=False)
    is_deal = models.BooleanField(default=False)
    deal_discount_percent = models.IntegerField(default=0, blank=True, null=True, help_text="Optional override percentage")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.9, blank=True)
    review_count = models.IntegerField(default=38, blank=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) if self.name else "product"
            candidate = base_slug
            count = 1
            while Product.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug}-{count}"
                count += 1
            self.slug = candidate

        # Automatically synchronize status with stock quantity
        if self.stock <= 0:
            self.status = "Out of Stock"
        elif self.status == "Out of Stock" and self.stock > 0:
            self.status = "Available"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def get_image_url(self):
        if self.image_url:
            return self.image_url
        if self.image:
            return self.image.url
        return "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80"

    @property
    def current_price(self):
        if self.discount_price and self.discount_price > 0 and self.discount_price < self.price:
            return self.discount_price
        return self.price

    @property
    def discount_percent(self):
        if self.deal_discount_percent > 0:
            return self.deal_discount_percent
        if self.discount_price and self.discount_price > 0 and self.discount_price < self.price:
            saving = self.price - self.discount_price
            percent = int((saving / self.price) * 100)
            return percent
        return 0

    @property
    def in_stock(self):
        return self.stock > 0 and self.status == "Available"


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=25, blank=True, default="")
    address = models.TextField(blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    state = models.CharField(max_length=100, blank=True, default="")
    postal_code = models.CharField(max_length=20, blank=True, default="")
    country = models.CharField(max_length=100, blank=True, default="India")
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="carts")
    session_key = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart #{self.id} ({self.user.username if self.user else 'Guest'})"

    def get_subtotal(self):
        total = Decimal("0.00")
        for item in self.items.all():
            total += item.get_item_subtotal()
        return total

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

    def get_shipping(self):
        subtotal = self.get_subtotal()
        if subtotal == Decimal("0.00"):
            return Decimal("0.00")
        if subtotal >= Decimal("5000.00"):
            return Decimal("0.00")
        return Decimal("99.00")

    def get_grand_total(self):
        return self.get_subtotal() + self.get_shipping()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Cart #{self.cart_id})"

    def get_item_subtotal(self):
        return self.product.current_price * self.quantity


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="wishlist_items")
    session_key = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlisted_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "product"), ("session_key", "product")]
        ordering = ["-id"]

    def __str__(self):
        return f"Wishlist item: {self.product.name}"


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("Cash on Delivery", "Cash on Delivery"),
        ("Test Payment", "Test Payment"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    order_number = models.CharField(max_length=50, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=25)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="India")
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default="Cash on Delivery")
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default="Pending")
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default="Pending")
    order_notes = models.TextField(blank=True, default="")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.order_number} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def total_items_count(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in #{self.order.order_number}"

    @property
    def get_image_url(self):
        if self.product:
            return self.product.get_image_url
        return "https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=500&auto=format&fit=crop&q=80"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role_or_title = models.CharField(max_length=100, default="Verified Buyer")
    avatar = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    avatar_url = models.URLField(max_length=800, blank=True, null=True)
    rating = models.IntegerField(default=5)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Testimonial by {self.name}"

    @property
    def get_avatar_url(self):
        if self.avatar_url:
            return self.avatar_url
        if self.avatar:
            return self.avatar.url
        return "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80"