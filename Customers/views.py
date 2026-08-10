import json
import uuid
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import transaction
from django.db.models import Q, Count, Sum, Avg
from django.core.paginator import Paginator
from django.utils import timezone

from .models import (
    Category, Product, CustomerProfile, Cart, CartItem,
    Wishlist, Order, OrderItem, ContactMessage, NewsletterSubscriber, Testimonial
)
from .forms import (
    UserRegisterForm, UserLoginForm, UserProfileForm,
    ProductForm, CategoryForm, CheckoutForm, ContactForm
)
from .context_processors import get_or_create_cart


# ==========================================
# STOREFRONT VIEWS
# ==========================================

def home(request):
    """
    Renders the modern electronics homepage with hero carousel, category cards,
    promotional bento grid, featured collections, flash deals with live timer,
    new arrivals, best sellers, trust badges, app promo, testimonials, and newsletter.
    """
    categories = Category.objects.filter(is_active=True).annotate(
        total_products=Count('products')
    ).order_by('name')

    # Hero spotlight / carousel products
    hero_products = Product.objects.filter(is_active=True, featured=True)[:3]
    if not hero_products.exists():
        hero_products = Product.objects.filter(is_active=True)[:3]

    # Promotional Grid Items
    promo_macbook = Product.objects.filter(name__icontains="MacBook", is_active=True).first()
    promo_audio = Product.objects.filter(category__slug="audio", is_active=True).first()
    promo_camera = Product.objects.filter(category__slug="cameras", is_active=True).first()
    promo_deal = Product.objects.filter(is_deal=True, is_active=True).first()

    # Flash Deals with discounts
    flash_deals = Product.objects.filter(is_active=True, is_deal=True).order_by('-discount_price')[:6]
    if not flash_deals.exists():
        flash_deals = Product.objects.filter(is_active=True)[:6]

    # New Arrivals
    new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:6]
    new_arrival_hero = new_arrivals.first() if new_arrivals.exists() else None
    new_arrival_sub = new_arrivals[1:5] if new_arrivals.count() > 1 else Product.objects.filter(is_active=True)[1:5]

    # Best Sellers: Top ordered products or highest rated
    best_sellers = Product.objects.filter(is_active=True).order_by('-rating', '-review_count')[:5]

    # Testimonials
    testimonials = Testimonial.objects.filter(is_active=True)[:3]

    # Live Store Statistics
    total_products_count = Product.objects.filter(is_active=True).count()
    total_brands_count = Product.objects.values('brand').distinct().count()

    context = {
        'categories': categories,
        'hero_products': hero_products,
        'promo_macbook': promo_macbook,
        'promo_audio': promo_audio,
        'promo_camera': promo_camera,
        'promo_deal': promo_deal,
        'flash_deals': flash_deals,
        'new_arrival_hero': new_arrival_hero,
        'new_arrival_sub': new_arrival_sub,
        'best_sellers': best_sellers,
        'testimonials': testimonials,
        'total_products_count': total_products_count,
        'total_brands_count': max(total_brands_count, 12),
    }
    return render(request, 'home.html', context)


def products_list(request):
    """
    Full product catalog view with live search, category filter, brand filter,
    price range, rating, stock filter, sorting, and pagination.
    """
    queryset = Product.objects.filter(is_active=True)

    # 1. Search Query
    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__name__icontains=query)
        )

    # 2. Category Filter
    selected_category = request.GET.get('category', '').strip()
    if selected_category:
        queryset = queryset.filter(
            Q(category__slug=selected_category) | Q(category__name__iexact=selected_category)
        )

    # 3. Brand Filter
    selected_brand = request.GET.get('brand', '').strip()
    if selected_brand:
        queryset = queryset.filter(brand__iexact=selected_brand)

    # 4. Price Filter
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    if min_price:
        try:
            queryset = queryset.filter(price__gte=Decimal(min_price))
        except Exception:
            pass
    if max_price:
        try:
            queryset = queryset.filter(price__lte=Decimal(max_price))
        except Exception:
            pass

    # 5. Availability Filter
    in_stock_only = request.GET.get('in_stock', '')
    if in_stock_only == '1' or in_stock_only == 'true':
        queryset = queryset.filter(stock__gt=0, status="Available")

    # 6. Deals Filter
    deals_only = request.GET.get('deals', '')
    if deals_only == '1' or deals_only == 'true':
        queryset = queryset.filter(is_deal=True)

    # 7. Sorting
    sort = request.GET.get('sort', 'featured')
    if sort == 'price_low':
        queryset = queryset.order_by('price')
    elif sort == 'price_high':
        queryset = queryset.order_by('-price')
    elif sort == 'newest':
        queryset = queryset.order_by('-created_at')
    elif sort == 'oldest':
        queryset = queryset.order_by('created_at')
    elif sort == 'name_asc':
        queryset = queryset.order_by('name')
    elif sort == 'rating':
        queryset = queryset.order_by('-rating', '-review_count')
    else:
        # Default: Featured first, then newest
        queryset = queryset.order_by('-featured', '-id')

    # Available Filter metadata
    categories = Category.objects.filter(is_active=True).annotate(total_products=Count('products'))
    brands = Product.objects.filter(is_active=True).values_list('brand', flat=True).distinct().order_by('brand')
    brands = [b for b in brands if b]

    # Pagination (12 items per page)
    paginator = Paginator(queryset, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'total_count': paginator.count,
        'categories': categories,
        'brands': brands,
        'query': query,
        'selected_category': selected_category,
        'selected_brand': selected_brand,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock_only': in_stock_only,
        'deals_only': deals_only,
        'sort': sort,
    }
    return render(request, 'products.html', context)


def category_detail(request, slug):
    """View products in a specific category"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    return redirect(f"/products/?category={category.slug}")


def product_detail(request, slug=None, id=None):
    """
    Detailed product showcase with gallery, price comparisons, stock status,
    quantity picker, Add to Cart, Buy Now, specifications, and related products.
    """
    if slug:
        product = get_object_or_404(Product, slug=slug, is_active=True)
    else:
        product = get_object_or_404(Product, id=id, is_active=True)

    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)


# ==========================================
# CART & WISHLIST VIEWS
# ==========================================

def cart_view(request):
    """Shopping cart page with item quantities, subtotals, shipping, and checkout CTA"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': cart.get_subtotal(),
        'shipping': cart.get_shipping(),
        'grand_total': cart.get_grand_total(),
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, product_id):
    """Adds a product to the cart with quantity validation and stock limit check"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request)

    if not product.in_stock:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Sorry, this product is out of stock.'}, status=400)
        messages.error(request, f"Sorry, '{product.name}' is currently out of stock.")
        return redirect('cart')

    quantity = int(request.POST.get('quantity', request.GET.get('quantity', 1)))
    quantity = max(1, quantity)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock:
            new_quantity = product.stock
            messages.warning(request, f"Quantity adjusted to available stock ({product.stock} units).")
        cart_item.quantity = new_quantity
        cart_item.save()
    else:
        if quantity > product.stock:
            quantity = product.stock
            messages.warning(request, f"Quantity adjusted to available stock ({product.stock} units).")
        cart_item.quantity = quantity
        cart_item.save()

    # If 'buy_now' parameter is passed, redirect straight to checkout
    if request.POST.get('buy_now') == '1' or request.GET.get('buy_now') == '1':
        return redirect('checkout')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"Added '{product.name}' to cart!",
            'cart_count': cart.get_total_items(),
            'cart_subtotal': str(cart.get_subtotal())
        })

    messages.success(request, f"Added '{product.name}' to your cart.")
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


def update_cart_item(request, item_id):
    """Updates quantity of a specific cart item (+1, -1, or explicit amount)"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    action = request.POST.get('action') or request.GET.get('action')
    qty_val = request.POST.get('quantity') or request.GET.get('quantity')

    if action == 'increase':
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"Updated quantity for {cart_item.product.name}.")
        else:
            messages.warning(request, f"Maximum available stock is {cart_item.product.stock}.")
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, f"Updated quantity for {cart_item.product.name}.")
        else:
            cart_item.delete()
            messages.info(request, f"Removed {cart_item.product.name} from cart.")
    elif qty_val is not None:
        try:
            qty = int(qty_val)
            if qty <= 0:
                cart_item.delete()
                messages.info(request, f"Removed {cart_item.product.name} from cart.")
            else:
                cart_item.quantity = min(qty, cart_item.product.stock)
                cart_item.save()
                messages.success(request, "Cart updated.")
        except ValueError:
            pass

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_total_items(),
            'subtotal': str(cart.get_subtotal()),
            'shipping': str(cart.get_shipping()),
            'grand_total': str(cart.get_grand_total())
        })

    return redirect('cart')


def remove_from_cart(request, item_id):
    """Removes an item from the cart"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()

    messages.success(request, f"Removed '{product_name}' from your cart.")
    return redirect('cart')


def clear_cart(request):
    """Clears all items in the current cart"""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.info(request, "Your shopping cart has been cleared.")
    return redirect('cart')


def wishlist_view(request):
    """View saved wishlist products"""
    if request.user.is_authenticated:
        items = Wishlist.objects.filter(user=request.user).select_related('product')
    elif request.session.session_key:
        items = Wishlist.objects.filter(session_key=request.session.session_key).select_related('product')
    else:
        items = []

    return render(request, 'wishlist.html', {'wishlist_items': items})


def toggle_wishlist(request, product_id):
    """Toggle a product in the wishlist"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    user = request.user if request.user.is_authenticated else None
    session_key = None if user else request.session.session_key

    if not user and not session_key:
        request.session.create()
        session_key = request.session.session_key

    if user:
        wishlist_item = Wishlist.objects.filter(user=user, product=product).first()
    else:
        wishlist_item = Wishlist.objects.filter(session_key=session_key, product=product).first()

    if wishlist_item:
        wishlist_item.delete()
        added = False
        msg = f"Removed '{product.name}' from wishlist."
    else:
        Wishlist.objects.create(user=user, session_key=session_key, product=product)
        added = True
        msg = f"Added '{product.name}' to your wishlist."

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        count = Wishlist.objects.filter(user=user).count() if user else Wishlist.objects.filter(session_key=session_key).count()
        return JsonResponse({'success': True, 'added': added, 'message': msg, 'wishlist_count': count})

    messages.success(request, msg)
    return redirect(request.META.get('HTTP_REFERER', 'products'))


# ==========================================
# CHECKOUT & ORDER CREATION
# ==========================================

def checkout_view(request):
    """
    Checkout page: Pre-populates user shipping information, calculates totals,
    and displays order summary with payment options (Cash on Delivery / Test Payment).
    """
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Add products before checking out.")
        return redirect('products')

    # Pre-fill with user profile if authenticated
    initial_data = {}
    if request.user.is_authenticated:
        initial_data['first_name'] = request.user.first_name
        initial_data['last_name'] = request.user.last_name
        initial_data['email'] = request.user.email
        profile = getattr(request.user, 'profile', None)
        if profile:
            initial_data['phone'] = profile.phone
            initial_data['address'] = profile.address
            initial_data['city'] = profile.city
            initial_data['state'] = profile.state
            initial_data['postal_code'] = profile.postal_code
            initial_data['country'] = profile.country

    form = CheckoutForm(initial=initial_data)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': cart.get_subtotal(),
        'shipping': cart.get_shipping(),
        'grand_total': cart.get_grand_total(),
        'form': form,
    }
    return render(request, 'checkout.html', context)


@transaction.atomic
def place_order(request):
    """
    Handles atomic order creation:
    1. Validates form inputs & stock availability
    2. Generates unique order number
    3. Creates Order & OrderItem entries
    4. Deducts stock quantity and updates status
    5. Clears cart
    6. Redirects to Order Confirmation page
    """
    if request.method != 'POST':
        return redirect('checkout')

    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()

    if not cart_items.exists():
        messages.error(request, "Cannot place order: Cart is empty.")
        return redirect('products')

    form = CheckoutForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Please check and correct the information in the checkout form.")
        return render(request, 'checkout.html', {
            'cart': cart,
            'cart_items': cart_items,
            'subtotal': cart.get_subtotal(),
            'shipping': cart.get_shipping(),
            'grand_total': cart.get_grand_total(),
            'form': form,
        })

    # Validate stock for all items before placing order
    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(
                request,
                f"Cannot complete order: '{item.product.name}' has only {item.product.stock} items remaining in stock."
            )
            return redirect('cart')

    # Generate unique order number
    unique_id = uuid.uuid4().hex[:6].upper()
    order_number = f"NEX-{timezone.now().strftime('%Y%m%d')}-{unique_id}"

    order = form.save(commit=False)
    order.user = request.user if request.user.is_authenticated else None
    order.order_number = order_number
    order.subtotal = cart.get_subtotal()
    order.shipping_fee = cart.get_shipping()
    order.discount_amount = Decimal("0.00")
    order.total_amount = cart.get_grand_total()
    
    if order.payment_method == "Test Payment":
        order.payment_status = "Paid"
    else:
        order.payment_status = "Pending"
    
    order.order_status = "Confirmed"
    order.save()

    # Create OrderItems and reduce product stock
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            price=item.product.current_price,
            quantity=item.quantity,
            subtotal=item.get_item_subtotal()
        )
        # Reduce stock
        item.product.stock -= item.quantity
        if item.product.stock <= 0:
            item.product.stock = 0
            item.product.status = "Out of Stock"
        item.product.save()

    # Save shipping info to customer profile if authenticated
    if request.user.is_authenticated:
        profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
        profile.phone = order.phone
        profile.address = order.address
        profile.city = order.city
        profile.state = order.state
        profile.postal_code = order.postal_code
        profile.country = order.country
        profile.save()

    # Clear cart
    cart.items.all().delete()

    messages.success(request, f"Order #{order_number} has been placed successfully!")
    return redirect('order_success', order_number=order.order_number)


def order_success(request, order_number):
    """Displays order success receipt and tracking details"""
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'order_success.html', {'order': order})


@login_required
def my_orders(request):
    """Customer order history page"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})


def order_detail_view(request, order_number):
    """Single order invoice and tracking breakdown"""
    if request.user.is_staff:
        order = get_object_or_404(Order, order_number=order_number)
    elif request.user.is_authenticated:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
    else:
        messages.info(request, "Please log in to view your order details.")
        return redirect('login')

    return render(request, 'order_detail.html', {'order': order})


def track_order_lookup(request):
    """Order tracking query view"""
    order_num = request.GET.get('order_number', '').strip()
    email = request.GET.get('email', '').strip()
    order = None

    if order_num:
        order_query = Order.objects.filter(order_number__iexact=order_num)
        if email:
            order_query = order_query.filter(email__iexact=email)
        order = order_query.first()
        if not order:
            messages.error(request, f"No order found matching #{order_num}.")

    return render(request, 'track_order.html', {'order': order, 'order_num': order_num, 'email': email})


# ==========================================
# AUTHENTICATION & PROFILE
# ==========================================

def register_view(request):
    """Handles new customer account registration with validation and auto-login"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Create empty customer profile
            CustomerProfile.objects.create(user=user)

            # Log user in
            auth_login(request, user)

            # Sync guest session cart to user cart
            if request.session.session_key:
                guest_cart = Cart.objects.filter(session_key=request.session.session_key).first()
                if guest_cart:
                    guest_cart.user = user
                    guest_cart.save()

            messages.success(request, f"Welcome to Nexus, {user.first_name or user.username}! Your account was created successfully.")
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Standard authentication login view"""
    if request.user.is_authenticated:
        return redirect('home')

    error = None
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Allow login with either username or email
            user = authenticate(request, username=username, password=password)
            if user is None and '@' in username:
                user_obj = User.objects.filter(email__iexact=username).first()
                if user_obj:
                    user = authenticate(request, username=user_obj.username, password=password)

            if user is not None:
                auth_login(request, user)

                # Sync guest cart
                if request.session.session_key:
                    guest_cart = Cart.objects.filter(session_key=request.session.session_key).first()
                    if guest_cart:
                        user_cart = Cart.objects.filter(user=user).first()
                        if user_cart and user_cart != guest_cart:
                            for item in guest_cart.items.all():
                                existing_item = user_cart.items.filter(product=item.product).first()
                                if existing_item:
                                    existing_item.quantity += item.quantity
                                    existing_item.save()
                                else:
                                    item.cart = user_cart
                                    item.save()
                            guest_cart.delete()
                        else:
                            guest_cart.user = user
                            guest_cart.save()

                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next') or 'home'
                return redirect(next_url)
            else:
                error = "Invalid username/email or password. Please try again."
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form, 'error': error})


def logout_view(request):
    """Logs the user out securely"""
    auth_logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def profile_view(request):
    """Customer profile and shipping details management"""
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Update User fields
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name = request.POST.get('last_name', '').strip()
        request.user.email = request.POST.get('email', '').strip()
        request.user.save()

        # Update Profile fields
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile details have been updated successfully.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    return render(request, 'profile.html', {'form': form, 'profile': profile})


# ==========================================
# STATIC / INFORMATIONAL & INTERACTIONS
# ==========================================

def about_view(request):
    """Modern company About page"""
    total_products = Product.objects.filter(is_active=True).count()
    total_customers = User.objects.count()
    return render(request, 'about.html', {
        'total_products': total_products,
        'total_customers': total_customers,
    })


def contact_view(request):
    """Contact page: Saves messages directly to database and shows feedback"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been received. Our team will get back to you shortly.")
            return redirect('contact')
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['name'] = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            initial_data['email'] = request.user.email
        form = ContactForm(initial=initial_data)

    return render(request, 'contact.html', {'form': form})


def newsletter_subscribe(request):
    """Newsletter subscription handler"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            sub, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Thank you for subscribing to Nexus Club! Check your inbox for exclusive offers.")
            else:
                messages.info(request, "You are already subscribed to our newsletter.")
        else:
            messages.error(request, "Please enter a valid email address.")

    return redirect(request.META.get('HTTP_REFERER', 'home'))


# ==========================================
# CUSTOM ADMIN MANAGEMENT DASHBOARD
# ==========================================

def is_staff_check(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff_check, login_url='login')
def admin_dashboard(request):
    """
    Live Administrative Overview:
    - Real computed metrics: Total Products, Customers, Orders, Revenue, Pending, Delivered, Out of Stock
    - Recent Orders table with instant status management
    - Low stock alerts
    - Category sales breakdown
    """
    products = Product.objects.all()
    orders = Order.objects.all()
    customers = User.objects.filter(is_staff=False)

    total_products = products.count()
    total_customers = customers.count()
    total_orders = orders.count()

    total_sales = orders.filter(payment_status="Paid").aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal("0.00")
    pending_orders = orders.filter(order_status="Pending").count()
    delivered_orders = orders.filter(order_status="Delivered").count()
    out_of_stock = products.filter(stock__lte=0).count()
    low_stock_products = products.filter(stock__gt=0, stock__lte=5)[:5]
    recent_orders = orders.order_by('-created_at')[:8]
    recent_messages = ContactMessage.objects.filter(is_read=False)[:5]

    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'total_sales': total_sales,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'out_of_stock': out_of_stock,
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
        'recent_messages': recent_messages,
    }
    return render(request, 'dashboard.html', context)


@user_passes_test(is_staff_check, login_url='login')
def admin_products_list(request):
    """Admin product catalog table with search, filter, and CRUD links"""
    products = Product.objects.select_related('category').all().order_by('-id')
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(brand__icontains=query))

    paginator = Paginator(products, 15)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'admin/products.html', {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'query': query,
    })


@user_passes_test(is_staff_check, login_url='login')
def admin_product_add(request):
    """Admin: Add a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' created successfully.")
            return redirect('admin_products')
    else:
        form = ProductForm()

    return render(request, 'admin/product_form.html', {'form': form, 'title': 'Add New Product'})


@user_passes_test(is_staff_check, login_url='login')
def admin_product_edit(request, product_id):
    """Admin: Edit an existing product"""
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated successfully.")
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'admin/product_form.html', {'form': form, 'product': product, 'title': f"Edit Product: {product.name}"})


@user_passes_test(is_staff_check, login_url='login')
def admin_product_delete(request, product_id):
    """Admin: Delete a product"""
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"Product '{name}' was deleted.")
        return redirect('admin_products')

    return render(request, 'admin/confirm_delete.html', {
        'object': product,
        'object_type': 'Product',
        'cancel_url': 'admin_products'
    })


@user_passes_test(is_staff_check, login_url='login')
def admin_categories_list(request):
    """Admin: Manage product categories"""
    categories = Category.objects.annotate(total_products=Count('products')).order_by('name')
    return render(request, 'admin/categories.html', {'categories': categories})


@user_passes_test(is_staff_check, login_url='login')
def admin_category_add(request):
    """Admin: Add new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f"Category '{cat.name}' created.")
            return redirect('admin_categories')
    else:
        form = CategoryForm()
    return render(request, 'admin/category_form.html', {'form': form, 'title': 'Add Category'})


@user_passes_test(is_staff_check, login_url='login')
def admin_category_edit(request, category_id):
    """Admin: Edit category"""
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{category.name}' updated.")
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin/category_form.html', {'form': form, 'category': category, 'title': f"Edit Category: {category.name}"})


@user_passes_test(is_staff_check, login_url='login')
def admin_category_delete(request, category_id):
    """Admin: Delete category"""
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f"Category '{name}' deleted.")
        return redirect('admin_categories')
    return render(request, 'admin/confirm_delete.html', {'object': category, 'object_type': 'Category', 'cancel_url': 'admin_categories'})


@user_passes_test(is_staff_check, login_url='login')
def admin_orders_list(request):
    """Admin: Order management and live status changes"""
    orders = Order.objects.select_related('user').all().order_by('-created_at')
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        orders = orders.filter(order_status=status_filter)

    query = request.GET.get('q', '').strip()
    if query:
        orders = orders.filter(Q(order_number__icontains=query) | Q(first_name__icontains=query) | Q(email__icontains=query))

    paginator = Paginator(orders, 15)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'admin/orders.html', {
        'page_obj': page_obj,
        'orders': page_obj.object_list,
        'status_filter': status_filter,
        'query': query,
    })


@user_passes_test(is_staff_check, login_url='login')
def admin_order_update(request, order_number):
    """Admin: Update order status & payment status"""
    order = get_object_or_404(Order, order_number=order_number)
    if request.method == 'POST':
        new_status = request.POST.get('order_status')
        new_payment = request.POST.get('payment_status')
        if new_status in dict(Order.ORDER_STATUS_CHOICES):
            order.order_status = new_status
        if new_payment in dict(Order.PAYMENT_STATUS_CHOICES):
            order.payment_status = new_payment
        order.save()
        messages.success(request, f"Order #{order.order_number} status updated to '{order.order_status}'.")
    return redirect('admin_orders')


@user_passes_test(is_staff_check, login_url='login')
def admin_customers_list(request):
    """Admin: View registered customer accounts and order spending totals"""
    customers = User.objects.filter(is_staff=False).annotate(
        order_count=Count('orders'),
        total_spent=Sum('orders__total_amount')
    ).order_by('-date_joined')

    return render(request, 'admin/customers.html', {'customers': customers})


@user_passes_test(is_staff_check, login_url='login')
def admin_messages_list(request):
    """Admin: View and manage customer inquiries"""
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'admin/messages.html', {'messages_list': messages_list})


@user_passes_test(is_staff_check, login_url='login')
def admin_message_mark_read(request, message_id):
    """Mark contact message as read"""
    msg = get_object_or_404(ContactMessage, id=message_id)
    msg.is_read = True
    msg.save()
    messages.success(request, "Message marked as read.")
    return redirect('admin_messages')