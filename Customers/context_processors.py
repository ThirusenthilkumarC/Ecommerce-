from decimal import Decimal
from django.db.models import Count
from .models import Category, Cart, Wishlist

CURRENCIES = {
    'INR': {'symbol': '₹', 'rate': Decimal('1.0'), 'name': 'INR ₹ (India)', 'flag': '🇮🇳'},
    'USD': {'symbol': '$', 'rate': Decimal('0.012'), 'name': 'USD $ (US Dollar)', 'flag': '🇺🇸'},
    'EUR': {'symbol': '€', 'rate': Decimal('0.011'), 'name': 'EUR € (Euro)', 'flag': '🇪🇺'},
    'GBP': {'symbol': '£', 'rate': Decimal('0.0094'), 'name': 'GBP £ (British Pound)', 'flag': '🇬🇧'},
    'AED': {'symbol': 'د.إ', 'rate': Decimal('0.044'), 'name': 'AED د.إ (UAE Dirham)', 'flag': '🇦🇪'},
    'SGD': {'symbol': 'S$', 'rate': Decimal('0.016'), 'name': 'SGD S$ (Singapore Dollar)', 'flag': '🇸🇬'},
    'AUD': {'symbol': 'A$', 'rate': Decimal('0.018'), 'name': 'AUD A$ (Australian Dollar)', 'flag': '🇦🇺'},
}

LANGUAGES = {
    'en': 'English',
    'ta': 'தமிழ் (Tamil)',
    'hi': 'हिन्दी (Hindi)',
    'ml': 'മലയാളം (Malayalam)',
    'te': 'తెలుగు (Telugu)',
    'kn': 'ಕನ್ನಡ (Kannada)',
}

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

    # Currency selection
    curr_code = request.session.get('currency', 'INR')
    if curr_code not in CURRENCIES:
        curr_code = 'INR'
    curr_info = CURRENCIES[curr_code]

    # Language selection
    lang_code = request.session.get('language', 'en')
    if lang_code not in LANGUAGES:
        lang_code = 'en'
    lang_name = LANGUAGES[lang_code]

    return {
        'nav_categories': categories,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'store_name': 'Nexus Electronics',
        'free_shipping_threshold': 5000,
        'currency_code': curr_code,
        'currency_symbol': curr_info['symbol'],
        'currency_info': curr_info,
        'available_currencies': CURRENCIES,
        'language_code': lang_code,
        'language_name': lang_name,
        'available_languages': LANGUAGES,
    }

