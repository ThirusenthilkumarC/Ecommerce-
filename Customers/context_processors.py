from django.db.models import Count
from .models import Category, Cart, Wishlist

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            if request.session.session_key:
                cart = Cart.objects.filter(session_key=request.session.session_key).first()
                if cart:
                    cart.user = request.user
                    cart.save()
            if not cart:
                cart = Cart.objects.create(user=request.user)
        return cart
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
        return cart

def ecommerce_context(request):
    # Categories for header navigation & mega menus
    categories = Category.objects.filter(is_active=True).annotate(
        total_products=Count('products')
    ).order_by('name')

    # Cart item count
    cart_count = 0
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                cart_count = cart.get_total_items()
        elif request.session.session_key:
            cart = Cart.objects.filter(session_key=request.session.session_key).first()
            if cart:
                cart_count = cart.get_total_items()
    except Exception:
        cart_count = 0

    # Wishlist item count
    wishlist_count = 0
    try:
        if request.user.is_authenticated:
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
        elif request.session.session_key:
            wishlist_count = Wishlist.objects.filter(session_key=request.session.session_key).count()
    except Exception:
        wishlist_count = 0

    return {
        'nav_categories': categories,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'store_name': 'Nexus Electronics',
        'free_shipping_threshold': 100,
    }
