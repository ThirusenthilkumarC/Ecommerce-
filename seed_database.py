import os
import django
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')
django.setup()

from django.contrib.auth.models import User
from Customers.models import (
    Category, Product, CustomerProfile, Order, OrderItem,
    Testimonial, ContactMessage, NewsletterSubscriber
)

def run_seed():
    print("Seeding database with realistic INR electronics prices & online HD images...")

    # 1. Setup Admin & Demo User
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@nexustech.com', 'is_staff': True, 'is_superuser': True}
    )
    admin_user.set_password('admin123')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    CustomerProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            'phone': '+91 98765 43210',
            'address': '742 Innovation Hub, Bandra Kurla Complex',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'postal_code': '400051',
            'country': 'India'
        }
    )

    demo_user, _ = User.objects.get_or_create(
        username='johndoe',
        defaults={'first_name': 'Rahul', 'last_name': 'Sharma', 'email': 'rahul.sharma@example.com'}
    )
    demo_user.set_password('password123')
    demo_user.save()
    CustomerProfile.objects.get_or_create(
        user=demo_user,
        defaults={
            'phone': '+91 91234 56789',
            'address': '104 Tech Park, Koramangala 5th Block',
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'postal_code': '560095',
            'country': 'India'
        }
    )

    # 2. Setup Categories with online CDN images
    category_data = [
        {"name": "Smartphones", "slug": "smartphones", "icon": "fa-mobile-screen-button", "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&auto=format&fit=crop&q=80", "description": "Latest flagship smartphones and foldable devices with advanced AI capabilities."},
        {"name": "Laptops", "slug": "laptops", "icon": "fa-laptop", "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&auto=format&fit=crop&q=80", "description": "Powerful ultrabooks, creator laptops, and high-performance workstations."},
        {"name": "Audio", "slug": "audio", "icon": "fa-headphones", "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=80", "description": "Studio headphones, true wireless earbuds, and portable surround sound speakers."},
        {"name": "Smartwatches", "slug": "smartwatches", "icon": "fa-clock", "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=80", "description": "Fitness trackers, cellular smartwatches, and luxury health wearables."},
        {"name": "Cameras", "slug": "cameras", "icon": "fa-camera", "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=500&auto=format&fit=crop&q=80", "description": "Mirrorless cameras, 4K drones, cinema lenses, and creator gear."},
        {"name": "Gaming", "slug": "gaming", "icon": "fa-gamepad", "image_url": "https://images.unsplash.com/photo-1606318801954-d46d46d3360a?w=500&auto=format&fit=crop&q=80", "description": "Next-gen consoles, VR headsets, mechanical keyboards, and precision mice."},
        {"name": "Accessories", "slug": "accessories", "icon": "fa-plug", "image_url": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=500&auto=format&fit=crop&q=80", "description": "Fast GaN chargers, braided cables, power banks, and ergonomic docks."},
        {"name": "Tablets", "slug": "tablets", "icon": "fa-tablet-screen-button", "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500&auto=format&fit=crop&q=80", "description": "Lightweight creative tablets with stylus support and vibrant OLED displays."}
    ]

    cat_map = {}
    for cat_item in category_data:
        cat, _ = Category.objects.update_or_create(
            slug=cat_item["slug"],
            defaults={
                "name": cat_item["name"],
                "icon": cat_item["icon"],
                "image_url": cat_item["image_url"],
                "description": cat_item["description"],
                "is_active": True
            }
        )
        cat_map[cat_item["slug"]] = cat

    # 3. Setup Products with high-resolution online product URLs & INR Prices
    products_data = [
        {
            "name": "iPhone 15 Pro Max 256GB",
            "slug": "iphone-15-pro-max-256gb",
            "category": cat_map["smartphones"],
            "brand": "Apple",
            "price": Decimal("159900.00"),
            "discount_price": Decimal("134900.00"),
            "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=700&auto=format&fit=crop&q=80",
            "description": "Aerospace-grade titanium design with A17 Pro chip, customizable Action button, and the most versatile 5x optical zoom camera system.",
            "stock": 25,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 16,
            "rating": Decimal("4.9"),
            "review_count": 345,
            "status": "Available"
        },
        {
            "name": "Apple MacBook Air M2 13-inch",
            "slug": "apple-macbook-air-m2-13-inch",
            "category": cat_map["laptops"],
            "brand": "Apple",
            "price": Decimal("114900.00"),
            "discount_price": Decimal("94990.00"),
            "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=700&auto=format&fit=crop&q=80",
            "description": "Strikingly thin design in Midnight aluminum, 13.6-inch Liquid Retina display, next-gen M2 chip, 1080p FaceTime HD camera, MagSafe 3 charging port.",
            "stock": 16,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 17,
            "rating": Decimal("4.9"),
            "review_count": 180,
            "status": "Available"
        },
        {
            "name": "Dell XPS 13 Plus Laptop",
            "slug": "dell-xps-13-plus-laptop",
            "category": cat_map["laptops"],
            "brand": "Dell",
            "price": Decimal("149990.00"),
            "discount_price": Decimal("129990.00"),
            "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=700&auto=format&fit=crop&q=80",
            "description": "Ultra-sleek edge-to-edge glass touchpad, capacitive touch function row, 13.4-inch 3.5K OLED InfinityEdge touch display, Intel Core i7 13th Gen.",
            "stock": 14,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 13,
            "rating": Decimal("4.8"),
            "review_count": 164,
            "status": "Available"
        },
        {
            "name": "Sony WH-1000XM5 Noise Canceling Headphones",
            "slug": "sony-wh-1000xm5-headphones",
            "category": cat_map["audio"],
            "brand": "Sony",
            "price": Decimal("34990.00"),
            "discount_price": Decimal("26990.00"),
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=700&auto=format&fit=crop&q=80",
            "description": "Industry-leading noise cancellation with 8 microphones, Auto NC Optimizer, crystal clear hands-free calling, and 30-hour battery life with quick charging.",
            "stock": 30,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 23,
            "rating": Decimal("4.9"),
            "review_count": 320,
            "status": "Available"
        },
        {
            "name": "Samsung Galaxy Watch 6 Classic",
            "slug": "samsung-galaxy-watch-6-classic",
            "category": cat_map["smartwatches"],
            "brand": "Samsung",
            "price": Decimal("36999.00"),
            "discount_price": Decimal("28999.00"),
            "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=700&auto=format&fit=crop&q=80",
            "description": "Physical rotating bezel, Advanced Sleep Coaching, ECG monitoring, Sapphire crystal glass display, and durable stainless steel body.",
            "stock": 20,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 22,
            "rating": Decimal("4.7"),
            "review_count": 412,
            "status": "Available"
        },
        {
            "name": "Bose SoundLink Revolve+ II Bluetooth Speaker",
            "slug": "bose-soundlink-revolve-plus-ii",
            "category": cat_map["audio"],
            "brand": "Bose",
            "price": Decimal("24500.00"),
            "discount_price": Decimal("19900.00"),
            "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=700&auto=format&fit=crop&q=80",
            "description": "True 360-degree deep, jaw-dropping sound with uniform coverage. IP55 water- and dust-resistant design with flexible fabric handle.",
            "stock": 18,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 19,
            "rating": Decimal("4.8"),
            "review_count": 153,
            "status": "Available"
        },
        {
            "name": "Canon EOS R50 Mirrorless Camera",
            "slug": "canon-eos-r50-mirrorless-camera",
            "category": cat_map["cameras"],
            "brand": "Canon",
            "price": Decimal("75990.00"),
            "discount_price": Decimal("64990.00"),
            "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=700&auto=format&fit=crop&q=80",
            "description": "Compact and lightweight 24.2 MP APS-C sensor camera with Dual Pixel CMOS AF II, uncropped 4K 30p movie recording, and vari-angle touchscreen LCD.",
            "stock": 10,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 14,
            "rating": Decimal("4.8"),
            "review_count": 215,
            "status": "Available"
        },
        {
            "name": "AirPods Pro (2nd Gen) MagSafe USB-C",
            "slug": "airpods-pro-2nd-gen-usb-c",
            "category": cat_map["audio"],
            "brand": "Apple",
            "price": Decimal("24900.00"),
            "discount_price": Decimal("19990.00"),
            "image_url": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=700&auto=format&fit=crop&q=80",
            "description": "Up to 2x more Active Noise Cancellation, Adaptive Audio, Transparency mode, Personalized Spatial Audio with dynamic head tracking, USB-C MagSafe case.",
            "stock": 40,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 20,
            "rating": Decimal("4.9"),
            "review_count": 512,
            "status": "Available"
        },
        {
            "name": "iPad Air (5th Gen) M1 Chip 64GB",
            "slug": "ipad-air-5th-gen-m1-64gb",
            "category": cat_map["tablets"],
            "brand": "Apple",
            "price": Decimal("59900.00"),
            "discount_price": None,
            "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=700&auto=format&fit=crop&q=80",
            "description": "Immersive 10.9-inch Liquid Retina display with True Tone, Apple M1 chip with 8-core CPU and 8-core GPU, 12MP Ultra Wide front camera with Center Stage.",
            "stock": 22,
            "featured": True,
            "is_deal": False,
            "deal_discount_percent": 0,
            "rating": Decimal("4.8"),
            "review_count": 146,
            "status": "Available"
        },
        {
            "name": "Sony WH-CH720N Wireless Headphones",
            "slug": "sony-wh-ch720n-wireless-headphones",
            "category": cat_map["audio"],
            "brand": "Sony",
            "price": Decimal("14990.00"),
            "discount_price": Decimal("9990.00"),
            "image_url": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=700&auto=format&fit=crop&q=80",
            "description": "Sony's lightest wireless noise-canceling headband ever, with Integrated Processor V1, multipoint connection, and up to 35 hours of battery life.",
            "stock": 25,
            "featured": False,
            "is_deal": False,
            "deal_discount_percent": 33,
            "rating": Decimal("4.6"),
            "review_count": 230,
            "status": "Available"
        },
        {
            "name": "DJI Mini 3 Lightweight Camera Drone",
            "slug": "dji-mini-3-camera-drone",
            "category": cat_map["cameras"],
            "brand": "DJI",
            "price": Decimal("49990.00"),
            "discount_price": Decimal("42990.00"),
            "image_url": "https://images.unsplash.com/photo-1527977966376-1c8408f9f108?w=700&auto=format&fit=crop&q=80",
            "description": "Under 249g ultra-lightweight foldable mini drone with 4K HDR video, True Vertical Shooting for social media, and 38-min extended flight battery.",
            "stock": 9,
            "featured": True,
            "is_deal": False,
            "deal_discount_percent": 14,
            "rating": Decimal("4.9"),
            "review_count": 410,
            "status": "Available"
        },
        {
            "name": "Logitech MX Master 3S Performance Mouse",
            "slug": "logitech-mx-master-3s-mouse",
            "category": cat_map["accessories"],
            "brand": "Logitech",
            "price": Decimal("10995.00"),
            "discount_price": Decimal("8995.00"),
            "image_url": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=700&auto=format&fit=crop&q=80",
            "description": "8K DPI any-surface tracking with quiet clicks, MagSpeed electromagnetic scrolling, ergonomic thumb rest, and multi-device Flow cross-computer control.",
            "stock": 35,
            "featured": False,
            "is_deal": False,
            "deal_discount_percent": 18,
            "rating": Decimal("4.9"),
            "review_count": 270,
            "status": "Available"
        },
        {
            "name": "PlayStation 5 DualSense Wireless Controller",
            "slug": "ps5-dualsense-wireless-controller",
            "category": cat_map["gaming"],
            "brand": "Sony",
            "price": Decimal("6390.00"),
            "discount_price": Decimal("4990.00"),
            "image_url": "https://images.unsplash.com/photo-1606318801954-d46d46d3360a?w=700&auto=format&fit=crop&q=80",
            "description": "Immersive haptic feedback, dynamic adaptive triggers, built-in microphone and headset jack, iconic comfortable ergonomics in Cosmic Red.",
            "stock": 28,
            "featured": True,
            "is_deal": False,
            "deal_discount_percent": 22,
            "rating": Decimal("4.8"),
            "review_count": 188,
            "status": "Available"
        },
        {
            "name": "Samsung Galaxy S24 Ultra 512GB",
            "slug": "samsung-galaxy-s24-ultra-512gb",
            "category": cat_map["smartphones"],
            "brand": "Samsung",
            "price": Decimal("139999.00"),
            "discount_price": Decimal("124999.00"),
            "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=700&auto=format&fit=crop&q=80",
            "description": "Galaxy AI features including Circle to Search, Live Translate, Note Assist, 200MP camera with ProVisual Engine, built-in S Pen, Titanium frame.",
            "stock": 12,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 11,
            "rating": Decimal("4.9"),
            "review_count": 310,
            "status": "Available"
        },
        {
            "name": "Anker 737 Power Bank (PowerCore 24K)",
            "slug": "anker-737-power-bank-24k",
            "category": cat_map["accessories"],
            "brand": "Anker",
            "price": Decimal("14999.00"),
            "discount_price": Decimal("10999.00"),
            "image_url": "https://images.unsplash.com/photo-1609592424364-ffea5e9eb492?w=700&auto=format&fit=crop&q=80",
            "description": "Ultra-powerful 140W two-way fast charging with Power Delivery 3.1, smart digital display showing output/input power, 24,000mAh capacity.",
            "stock": 42,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 27,
            "rating": Decimal("4.8"),
            "review_count": 410,
            "status": "Available"
        },
        {
            "name": "Razer BlackWidow V4 Pro Mechanical Keyboard",
            "slug": "razer-blackwidow-v4-pro-keyboard",
            "category": cat_map["gaming"],
            "brand": "Razer",
            "price": Decimal("22999.00"),
            "discount_price": Decimal("18999.00"),
            "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=700&auto=format&fit=crop&q=80",
            "description": "Razer Command Dial, 8 dedicated macro keys, Green Clicky Mechanical Switches, underglow chroma lighting on 3 sides, plush magnetic wrist rest.",
            "stock": 15,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 17,
            "rating": Decimal("4.7"),
            "review_count": 142,
            "status": "Available"
        }
    ]

    for pdata in products_data:
        p, created = Product.objects.update_or_create(
            slug=pdata["slug"],
            defaults=pdata
        )
        print(f"  {'[+] Created' if created else '[~] Updated'} Product: {p.name}")

    # 4. Setup Testimonials with avatars
    testimonials_data = [
        {
            "name": "Robert Fox",
            "role_or_title": "Verified Buyer",
            "rating": 5,
            "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
            "content": "Nexus has the best collection of gadgets. Fast delivery across India, great prices and amazing customer service! My MacBook Air arrived in pristine condition."
        },
        {
            "name": "Priya Sharma",
            "role_or_title": "Tech Enthusiast",
            "rating": 5,
            "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
            "content": "The checkout process was seamless and the Sony WH-1000XM5 headphones sound unbelievable. 100% recommended for authentic electronics."
        },
        {
            "name": "David D'Souza",
            "role_or_title": "Audio Engineer",
            "rating": 5,
            "avatar_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
            "content": "Extremely satisfied with the delivery speed and warranty support. The real-time tracking made keeping tabs on my order super convenient."
        }
    ]

    for tdata in testimonials_data:
        Testimonial.objects.update_or_create(
            name=tdata["name"],
            defaults=tdata
        )

    # 5. Create Realistic Sample Orders in INR
    sony_headphone = Product.objects.get(slug="sony-wh-1000xm5-headphones")
    macbook = Product.objects.get(slug="apple-macbook-air-m2-13-inch")
    
    order1, _ = Order.objects.get_or_create(
        order_number="NEX-2026-84920",
        defaults={
            "user": demo_user,
            "first_name": "Rahul",
            "last_name": "Sharma",
            "email": "rahul.sharma@example.com",
            "phone": "+91 91234 56789",
            "address": "104 Tech Park, Koramangala 5th Block",
            "city": "Bengaluru",
            "state": "Karnataka",
            "postal_code": "560095",
            "country": "India",
            "subtotal": Decimal("26990.00"),
            "shipping_fee": Decimal("0.00"),
            "total_amount": Decimal("26990.00"),
            "payment_method": "Test Payment",
            "payment_status": "Paid",
            "order_status": "Delivered"
        }
    )
    OrderItem.objects.get_or_create(
        order=order1,
        product=sony_headphone,
        defaults={
            "product_name": sony_headphone.name,
            "price": Decimal("26990.00"),
            "quantity": 1,
            "subtotal": Decimal("26990.00")
        }
    )

    order2, _ = Order.objects.get_or_create(
        order_number="NEX-2026-91823",
        defaults={
            "user": demo_user,
            "first_name": "Rahul",
            "last_name": "Sharma",
            "email": "rahul.sharma@example.com",
            "phone": "+91 91234 56789",
            "address": "104 Tech Park, Koramangala 5th Block",
            "city": "Bengaluru",
            "state": "Karnataka",
            "postal_code": "560095",
            "country": "India",
            "subtotal": Decimal("94990.00"),
            "shipping_fee": Decimal("0.00"),
            "total_amount": Decimal("94990.00"),
            "payment_method": "Cash on Delivery",
            "payment_status": "Pending",
            "order_status": "Processing"
        }
    )
    OrderItem.objects.get_or_create(
        order=order2,
        product=macbook,
        defaults={
            "product_name": macbook.name,
            "price": Decimal("94990.00"),
            "quantity": 1,
            "subtotal": Decimal("94990.00")
        }
    )

    print("\nDatabase seeded with Indian Rupee (INR) pricing and HD image assets successfully!")

if __name__ == '__main__':
    run_seed()
