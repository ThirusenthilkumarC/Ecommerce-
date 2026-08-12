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
    print("Seeding database with 50+ rich electronics products, INR prices & HD images...")

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

    # 2. Setup 8 Categories
    categories = {
        "smartphones": Category.objects.get_or_create(
            slug="smartphones",
            defaults={
                "name": "Smartphones",
                "icon": "fa-mobile-screen-button",
                "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&auto=format&fit=crop&q=80",
                "description": "Latest flagship smartphones and foldable devices with advanced computational camera systems."
            }
        )[0],
        "laptops": Category.objects.get_or_create(
            slug="laptops",
            defaults={
                "name": "Laptops",
                "icon": "fa-laptop",
                "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop&q=80",
                "description": "High-performance ultrabooks, creator laptops, and AI workstation machines."
            }
        )[0],
        "audio": Category.objects.get_or_create(
            slug="audio",
            defaults={
                "name": "Audio",
                "icon": "fa-headphones-simple",
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80",
                "description": "Audiophile studio headphones, active noise-cancelling earbuds, and wireless speakers."
            }
        )[0],
        "smartwatches": Category.objects.get_or_create(
            slug="smartwatches",
            defaults={
                "name": "Smartwatches",
                "icon": "fa-clock",
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80",
                "description": "Precision wellness trackers, cellular smartwatches, and titanium sport editions."
            }
        )[0],
        "cameras": Category.objects.get_or_create(
            slug="cameras",
            defaults={
                "name": "Cameras",
                "icon": "fa-camera",
                "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=600&auto=format&fit=crop&q=80",
                "description": "Full-frame mirrorless cameras, 4K vlog rigs, and professional cinematic glass."
            }
        )[0],
        "gaming": Category.objects.get_or_create(
            slug="gaming",
            defaults={
                "name": "Gaming",
                "icon": "fa-gamepad",
                "image_url": "https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?w=600&auto=format&fit=crop&q=80",
                "description": "Next-gen consoles, esports mechanical peripherals, and ergonomic gaming gear."
            }
        )[0],
        "accessories": Category.objects.get_or_create(
            slug="accessories",
            defaults={
                "name": "Accessories",
                "icon": "fa-plug",
                "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&auto=format&fit=crop&q=80",
                "description": "GaN fast chargers, magnetic docks, high-speed Thunderbolt hubs, and cables."
            }
        )[0],
        "tablets": Category.objects.get_or_create(
            slug="tablets",
            defaults={
                "name": "Tablets",
                "icon": "fa-tablet-screen-button",
                "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&auto=format&fit=crop&q=80",
                "description": "Pro digital drawing tablets, lightweight reading slates, and productivity pads."
            }
        )[0],
        "smart-home": Category.objects.get_or_create(
            slug="smart-home",
            defaults={
                "name": "Smart Home",
                "icon": "fa-house-signal",
                "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?w=600&auto=format&fit=crop&q=80",
                "description": "Intelligent voice assistants, smart lighting hubs, and connected security cameras."
            }
        )[0],
        "monitors": Category.objects.get_or_create(
            slug="monitors",
            defaults={
                "name": "Monitors",
                "icon": "fa-desktop",
                "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&auto=format&fit=crop&q=80",
                "description": "4K UHD creator monitors, ultra-wide curved OLED panels, and high-refresh esports displays."
            }
        )[0],
        "storage": Category.objects.get_or_create(
            slug="storage",
            defaults={
                "name": "Storage & Networking",
                "icon": "fa-hard-drive",
                "image_url": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=600&auto=format&fit=crop&q=80",
                "description": "Blazing fast PCIe 4.0 NVMe SSDs, rugged external drives, and WiFi 6E mesh routers."
            }
        )[0],
    }

    # 3. 52 Realistic Electronics Products
    raw_products = [
        # Smartphones (8)
        {
            "name": "Apple iPhone 15 Pro Max 256GB",
            "slug": "apple-iphone-15-pro-max-256gb",
            "brand": "Apple",
            "category": categories["smartphones"],
            "description": "Forged in aerospace-grade titanium with the groundbreaking A17 Pro chip, customizable Action button, and the most powerful 5x telephoto optical zoom system on iPhone.",
            "price": Decimal("159900.00"),
            "discount_price": Decimal("148999.00"),
            "stock": 25,
            "rating": Decimal("4.9"),
            "review_count": 142,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 7,
            "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Samsung Galaxy S24 Ultra 512GB",
            "slug": "samsung-galaxy-s24-ultra-512gb",
            "brand": "Samsung",
            "category": categories["smartphones"],
            "description": "Unleash Galaxy AI with Circle to Search, Live Translate, Note Assist, 200MP camera with ProVisual Engine, and an integrated S Pen nestled in a sleek titanium frame.",
            "price": Decimal("139999.00"),
            "discount_price": Decimal("129999.00"),
            "stock": 20,
            "rating": Decimal("4.8"),
            "review_count": 98,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 7,
            "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Google Pixel 8 Pro 128GB",
            "slug": "google-pixel-8-pro-128gb",
            "brand": "Google",
            "category": categories["smartphones"],
            "description": "Powered by Google Tensor G3 with advanced machine learning, Super Actua display, pro-level camera controls, and 7 years of OS upgrades.",
            "price": Decimal("106999.00"),
            "discount_price": Decimal("93999.00"),
            "stock": 18,
            "rating": Decimal("4.7"),
            "review_count": 64,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 12,
            "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "OnePlus 12 5G (Flowy Emerald)",
            "slug": "oneplus-12-5g-flowy-emerald",
            "brand": "OnePlus",
            "category": categories["smartphones"],
            "description": "Snapdragon 8 Gen 3 flagship with 4th Gen Hasselblad Camera, 2K 120Hz ProXDR display, and 100W SUPERVOOC flash fast charging.",
            "price": Decimal("69999.00"),
            "discount_price": Decimal("64999.00"),
            "stock": 22,
            "rating": Decimal("4.7"),
            "review_count": 52,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 7,
            "image_url": "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Nothing Phone (2) 256GB Dark Grey",
            "slug": "nothing-phone-2-256gb",
            "brand": "Nothing",
            "category": categories["smartphones"],
            "description": "Unique Glyph Interface with interactive LED light sequences, Nothing OS 2.5, dual 50MP Sony camera array, and Snapdragon 8+ Gen 1 efficiency.",
            "price": Decimal("44999.00"),
            "discount_price": Decimal("39999.00"),
            "stock": 15,
            "rating": Decimal("4.6"),
            "review_count": 48,
            "featured": False,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02560?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Samsung Galaxy Z Fold 5 512GB",
            "slug": "samsung-galaxy-z-fold-5-512gb",
            "brand": "Samsung",
            "category": categories["smartphones"],
            "description": "Transformative 7.6-inch Dynamic AMOLED 2X folding workspace with zero-gap Flex Hinge, multitasking taskbar, and robust IPX8 water resistance.",
            "price": Decimal("164999.00"),
            "discount_price": Decimal("154999.00"),
            "stock": 12,
            "rating": Decimal("4.8"),
            "review_count": 36,
            "featured": True,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Apple iPhone 15 128GB Black",
            "slug": "apple-iphone-15-128gb-black",
            "brand": "Apple",
            "category": categories["smartphones"],
            "description": "Dynamic Island arrives on iPhone 15 with a 48MP Main camera, 2x telephoto crop, color-infused back glass, and universal USB-C connectivity.",
            "price": Decimal("79900.00"),
            "discount_price": Decimal("71999.00"),
            "stock": 30,
            "rating": Decimal("4.8"),
            "review_count": 88,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 10,
            "image_url": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Sony Xperia 1 V 5G",
            "slug": "sony-xperia-1-v-5g",
            "brand": "Sony",
            "category": categories["smartphones"],
            "description": "Engineered for creators with next-generation Exmor T for mobile sensor, 4K 120Hz OLED 21:9 display, and dedicated Alpha camera manual controls.",
            "price": Decimal("119999.00"),
            "discount_price": Decimal("109999.00"),
            "stock": 8,
            "rating": Decimal("4.6"),
            "review_count": 22,
            "featured": False,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Google Pixel 9 Pro 256GB (Obsidian)",
            "slug": "google-pixel-9-pro-256gb",
            "brand": "Google",
            "category": categories["smartphones"],
            "description": "Google Tensor G4 processor with Gemini Nano AI, Super Actua LTPO display, and studio-grade 50MP triple camera system with 8K video.",
            "price": Decimal("109999.00"),
            "discount_price": Decimal("99999.00"),
            "stock": 16,
            "rating": Decimal("4.9"),
            "review_count": 35,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 9,
            "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "OnePlus 13 5G 512GB (Midnight Black)",
            "slug": "oneplus-13-5g-512gb",
            "brand": "OnePlus",
            "category": categories["smartphones"],
            "description": "Next-gen Snapdragon 8 Elite platform, 6000mAh Glacier battery with 100W charging, and 50MP Hasselblad Master Triple Camera.",
            "price": Decimal("74999.00"),
            "discount_price": Decimal("69999.00"),
            "stock": 20,
            "rating": Decimal("4.8"),
            "review_count": 41,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 7,
            "image_url": "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Xiaomi 15 Pro 5G Leica Edition",
            "slug": "xiaomi-15-pro-5g-leica",
            "brand": "Xiaomi",
            "category": categories["smartphones"],
            "description": "Co-engineered with Leica featuring Summilux optical lenses, 2K quad-curved AMOLED display, and HyperOS 2.0 performance.",
            "price": Decimal("79999.00"),
            "discount_price": Decimal("72999.00"),
            "stock": 15,
            "rating": Decimal("4.7"),
            "review_count": 29,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 9,
            "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02560?w=600&auto=format&fit=crop&q=80"
        },

        # Laptops (8)
        {
            "name": "Apple MacBook Pro 16-inch M3 Max (36GB/1TB)",
            "slug": "apple-macbook-pro-16-m3-max",
            "brand": "Apple",
            "category": categories["laptops"],
            "description": "Extreme performance with 14-core CPU, 30-core GPU, Liquid Retina XDR 120Hz ProMotion display, and up to 22 hours of battery life in Space Black.",
            "price": Decimal("349900.00"),
            "discount_price": Decimal("329990.00"),
            "stock": 10,
            "rating": Decimal("5.0"),
            "review_count": 45,
            "featured": True,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Apple MacBook Air 15-inch M3 (16GB/512GB)",
            "slug": "apple-macbook-air-15-m3",
            "brand": "Apple",
            "category": categories["laptops"],
            "description": "Impossibly thin, blazing fast M3 architecture, expansive 15.3-inch Liquid Retina display, silent fanless thermal system, and MagSafe 3 charging.",
            "price": Decimal("154900.00"),
            "discount_price": Decimal("142990.00"),
            "stock": 18,
            "rating": Decimal("4.9"),
            "review_count": 68,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 8,
            "image_url": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Dell XPS 16 OLED (Intel Core Ultra 9, RTX 4070)",
            "slug": "dell-xps-16-oled-core-ultra-9",
            "brand": "Dell",
            "category": categories["laptops"],
            "description": "Futuristic CNC machined aluminum chassis with zero-lattice keyboard, invisible glass haptic touchpad, and 4K+ InfinityEdge OLED display.",
            "price": Decimal("289990.00"),
            "discount_price": Decimal("269990.00"),
            "stock": 12,
            "rating": Decimal("4.8"),
            "review_count": 34,
            "featured": True,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "HP Spectre x360 2-in-1 14-inch OLED",
            "slug": "hp-spectre-x360-14-oled",
            "brand": "HP",
            "category": categories["laptops"],
            "description": "Intel Evo Core Ultra 7 processor with AI studio effects, 2.8K 120Hz touch OLED, gem-cut styling, and rechargeable MPP 2.0 tilt pen included.",
            "price": Decimal("164990.00"),
            "discount_price": Decimal("149990.00"),
            "stock": 14,
            "rating": Decimal("4.7"),
            "review_count": 28,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 9,
            "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Lenovo Legion Pro 7i Gen 8 (RTX 4080, i9-13900HX)",
            "slug": "lenovo-legion-pro-7i-gen-8",
            "brand": "Lenovo",
            "category": categories["laptops"],
            "description": "AI-tuned esports battle station with Legion Coldfront 5.0 vapor chamber cooling, 240Hz 16-inch WQXGA gaming panel, and per-key RGB keyboard.",
            "price": Decimal("245000.00"),
            "discount_price": Decimal("224990.00"),
            "stock": 9,
            "rating": Decimal("4.9"),
            "review_count": 41,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 8,
            "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Razer Blade 16 (Dual-Mode Mini-LED, RTX 4090)",
            "slug": "razer-blade-16-dual-mode-mini-led",
            "brand": "Razer",
            "category": categories["laptops"],
            "description": "World's first dual-mode Mini-LED display toggling between UHD+ 120Hz and FHD+ 240Hz, paired with Nvidia RTX 4090 in an anodized unibody frame.",
            "price": Decimal("419999.00"),
            "discount_price": Decimal("389999.00"),
            "stock": 5,
            "rating": Decimal("4.9"),
            "review_count": 19,
            "featured": False,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Lenovo ThinkPad X1 Carbon Gen 12",
            "slug": "lenovo-thinkpad-x1-carbon-gen-12",
            "brand": "Lenovo",
            "category": categories["laptops"],
            "description": "Legendary ultralight business machine weighing just 1.09kg, MIL-STD 810H durability, Communications Bar with 8MP webcam, and tactile trackpoint.",
            "price": Decimal("189990.00"),
            "discount_price": Decimal("174990.00"),
            "stock": 16,
            "rating": Decimal("4.8"),
            "review_count": 37,
            "featured": False,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Dell Alienware m18 R2 Gaming Laptop",
            "slug": "dell-alienware-m18-r2-gaming",
            "brand": "Dell",
            "category": categories["laptops"],
            "description": "Monumental 18-inch desktop replacement with Cryo-tech cooling, Element 31 thermal interface, mechanical CherryMX ultra-low profile switches.",
            "price": Decimal("329990.00"),
            "discount_price": Decimal("309990.00"),
            "stock": 7,
            "rating": Decimal("4.8"),
            "review_count": 15,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 6,
            "image_url": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "ASUS ROG Strix SCAR 16 (RTX 4080, i9-14900HX)",
            "slug": "asus-rog-strix-scar-16",
            "brand": "ASUS",
            "category": categories["laptops"],
            "description": "ROG Nebula HDR Mini-LED 240Hz display with Conductonaut Extreme liquid metal cooling, 32GB DDR5 RAM, and customizable Aura Sync RGB.",
            "price": Decimal("279990.00"),
            "discount_price": Decimal("259990.00"),
            "stock": 10,
            "rating": Decimal("4.9"),
            "review_count": 28,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 7,
            "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=600&auto=format&fit=crop&q=80"
        },

        # Audio (8)
        {
            "name": "Sony WH-1000XM5 Wireless Noise-Cancelling Headphones",
            "slug": "sony-wh-1000xm5-headphones",
            "brand": "Sony",
            "category": categories["audio"],
            "description": "Industry-leading noise cancellation powered by dual processors and 8 microphones, LDAC Hi-Res Audio wireless, and crystal-clear hands-free calls.",
            "price": Decimal("34990.00"),
            "discount_price": Decimal("28990.00"),
            "stock": 35,
            "rating": Decimal("4.9"),
            "review_count": 178,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 17,
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Bose QuietComfort Ultra Headphones",
            "slug": "bose-quietcomfort-ultra-headphones",
            "brand": "Bose",
            "category": categories["audio"],
            "description": "Breakthrough spatialized audio with Bose Immersive Audio, world-class active noise cancellation, CustomTune technology, and luxe protein leather cushions.",
            "price": Decimal("35900.00"),
            "discount_price": Decimal("31900.00"),
            "stock": 25,
            "rating": Decimal("4.8"),
            "review_count": 89,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 11,
            "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Apple AirPods Pro (2nd Generation, USB-C)",
            "slug": "apple-airpods-pro-2-usb-c",
            "brand": "Apple",
            "category": categories["audio"],
            "description": "Up to 2x more Active Noise Cancellation, Adaptive Audio, Transparency mode, Personalized Spatial Audio with dynamic head tracking, and MagSafe case.",
            "price": Decimal("24900.00"),
            "discount_price": Decimal("21990.00"),
            "stock": 40,
            "rating": Decimal("4.9"),
            "review_count": 210,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 12,
            "image_url": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Sony WF-1000XM5 True Wireless Earbuds",
            "slug": "sony-wf-1000xm5-earbuds",
            "brand": "Sony",
            "category": categories["audio"],
            "description": "The best truly wireless noise canceling earbuds with Integrated Processor V2, Dynamic Driver X for wide frequency reproduction, and bone conduction sensors.",
            "price": Decimal("26990.00"),
            "discount_price": Decimal("22990.00"),
            "stock": 28,
            "rating": Decimal("4.7"),
            "review_count": 72,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 15,
            "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "JBL Boombox 3 Portable Bluetooth Speaker",
            "slug": "jbl-boombox-3-bluetooth-speaker",
            "brand": "JBL",
            "category": categories["audio"],
            "description": "Massive sound with monstrous bass from a 3-way acoustic speaker system, IP67 waterproof and dustproof design, and 24 hours of unstoppable playtime.",
            "price": Decimal("39999.00"),
            "discount_price": Decimal("34999.00"),
            "stock": 16,
            "rating": Decimal("4.8"),
            "review_count": 56,
            "featured": False,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Bose SoundLink Max Bluetooth Speaker",
            "slug": "bose-soundlink-max-speaker",
            "brand": "Bose",
            "category": categories["audio"],
            "description": "Deep, rumbling stereo bass in a rugged grab-and-go form factor with soft rope handle, IP67 water/dust resistance, and built-in USB-C phone charger.",
            "price": Decimal("37900.00"),
            "discount_price": Decimal("33900.00"),
            "stock": 14,
            "rating": Decimal("4.8"),
            "review_count": 31,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 10,
            "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Apple AirPods Max (Space Grey)",
            "slug": "apple-airpods-max-space-grey",
            "brand": "Apple",
            "category": categories["audio"],
            "description": "Apple-designed dynamic driver provides high-fidelity audio with computational acoustics from dual H1 chips and breathable knit-mesh canopy headband.",
            "price": Decimal("59900.00"),
            "discount_price": Decimal("54900.00"),
            "stock": 15,
            "rating": Decimal("4.8"),
            "review_count": 94,
            "featured": True,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "JBL Flip 6 Waterproof Bluetooth Speaker",
            "slug": "jbl-flip-6-bluetooth-speaker",
            "brand": "JBL",
            "category": categories["audio"],
            "description": "2-way speaker system delivering loud, crystal clear, powerful JBL Original Pro Sound with IP67 waterproof and dustproof design.",
            "price": Decimal("13999.00"),
            "discount_price": Decimal("10999.00"),
            "stock": 35,
            "rating": Decimal("4.8"),
            "review_count": 92,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 21,
            "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Garmin Forerunner 965 AMOLED GPS Running Watch",
            "slug": "garmin-forerunner-965-gps-watch",
            "brand": "Garmin",
            "category": categories["smartwatches"],
            "description": "Brilliant 1.4-inch AMOLED touchscreen with lightweight titanium bezel, built-in full-color mapping, and advanced training metrics.",
            "price": Decimal("67490.00"),
            "discount_price": Decimal("61990.00"),
            "stock": 14,
            "rating": Decimal("4.9"),
            "review_count": 38,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 8,
            "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Canon EOS R50 Mirrorless Camera (Creator Kit)",
            "slug": "canon-eos-r50-creator-kit",
            "brand": "Canon",
            "category": categories["cameras"],
            "description": "Compact and lightweight 24.2MP APS-C sensor camera with 4K uncropped 30p video, Dual Pixel CMOS AF II, and Vari-angle touchscreen.",
            "price": Decimal("75995.00"),
            "discount_price": Decimal("68990.00"),
            "stock": 16,
            "rating": Decimal("4.8"),
            "review_count": 45,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 9,
            "image_url": "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Xbox Wireless Controller (Robot White)",
            "slug": "xbox-wireless-controller-robot-white",
            "brand": "Microsoft",
            "category": categories["gaming"],
            "description": "Modernized ergonomic design with sculpted surfaces, refined geometry, hybrid D-pad, and textured grip for enhanced comfort during gameplay.",
            "price": Decimal("5990.00"),
            "discount_price": Decimal("5390.00"),
            "stock": 40,
            "rating": Decimal("4.8"),
            "review_count": 115,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 10,
            "image_url": "https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?w=600&auto=format&fit=crop&q=80"
        },

        # Smartwatches (6)
        {
            "name": "Apple Watch Ultra 2 (Titanium GPS + Cellular)",
            "slug": "apple-watch-ultra-2-titanium",
            "brand": "Apple",
            "category": categories["smartwatches"],
            "description": "Rugged 49mm titanium case, 3000-nit edge-to-edge display, dual-frequency precision GPS, 100m water resistance, and innovative Double Tap gesture control.",
            "price": Decimal("89900.00"),
            "discount_price": Decimal("84990.00"),
            "stock": 20,
            "rating": Decimal("4.9"),
            "review_count": 86,
            "featured": True,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Samsung Galaxy Watch 6 Classic 47mm LTE",
            "slug": "samsung-galaxy-watch-6-classic-47mm",
            "brand": "Samsung",
            "category": categories["smartwatches"],
            "description": "Iconic rotating physical bezel, Sapphire Crystal Super AMOLED display, BioActive Sensor with ECG and BIA body composition analysis.",
            "price": Decimal("43999.00"),
            "discount_price": Decimal("36999.00"),
            "stock": 22,
            "rating": Decimal("4.7"),
            "review_count": 64,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 16,
            "image_url": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Apple Watch Series 9 GPS 45mm (Midnight)",
            "slug": "apple-watch-series-9-gps-45mm",
            "brand": "Apple",
            "category": categories["smartwatches"],
            "description": "Powerful S9 SiP processor, ultra-bright 2000 nits Always-On Retina display, on-device Siri with health queries, and ECG heart rate notifications.",
            "price": Decimal("44900.00"),
            "discount_price": Decimal("39990.00"),
            "stock": 35,
            "rating": Decimal("4.8"),
            "review_count": 112,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 11,
            "image_url": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Google Pixel Watch 2 (Matte Black)",
            "slug": "google-pixel-watch-2",
            "brand": "Google",
            "category": categories["smartwatches"],
            "description": "Fitbit's most accurate heart rate tracking with multi-path sensor, body-response skin temperature sensor, Google Assistant, and 24-hour battery with fast charging.",
            "price": Decimal("39990.00"),
            "discount_price": Decimal("34990.00"),
            "stock": 18,
            "rating": Decimal("4.6"),
            "review_count": 38,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 13,
            "image_url": "https://images.unsplash.com/photo-1510017803434-a899398421b3?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Sony SmartBand Talk SWR30 E-Ink Watch",
            "slug": "sony-smartband-talk-swr30",
            "brand": "Sony",
            "category": categories["smartwatches"],
            "description": "Curved always-on E-Ink display readable in bright sunlight, voice interaction calling, waterproof IP68 certification, and week-long battery life.",
            "price": Decimal("12999.00"),
            "discount_price": Decimal("9999.00"),
            "stock": 15,
            "rating": Decimal("4.4"),
            "review_count": 18,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 23,
            "image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "OnePlus Watch 2 (Emerald Green)",
            "slug": "oneplus-watch-2-emerald",
            "brand": "OnePlus",
            "category": categories["smartwatches"],
            "description": "Dual-Engine Architecture with Snapdragon W5 + BES2700 chips, Wear OS 4, military-grade steel case with sapphire crystal, and up to 100 hours battery.",
            "price": Decimal("24999.00"),
            "discount_price": Decimal("21999.00"),
            "stock": 25,
            "rating": Decimal("4.7"),
            "review_count": 47,
            "featured": False,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=600&auto=format&fit=crop&q=80"
        },

        # Cameras & Drones (6)
        {
            "name": "Sony Alpha 7 IV Full-Frame Mirrorless Camera (Body)",
            "slug": "sony-alpha-7-iv-mirrorless-camera",
            "brand": "Sony",
            "category": categories["cameras"],
            "description": "33MP full-frame Exmor R back-illuminated CMOS sensor, BIONZ XR processing engine, 4K 60p 10-bit 4:2:2 recording, and AI Real-time Eye AF.",
            "price": Decimal("224990.00"),
            "discount_price": Decimal("209990.00"),
            "stock": 10,
            "rating": Decimal("4.9"),
            "review_count": 52,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 7,
            "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Canon EOS R6 Mark II Mirrorless Camera with 24-105mm Lens",
            "slug": "canon-eos-r6-mark-ii-kit",
            "brand": "Canon",
            "category": categories["cameras"],
            "description": "24.2MP CMOS sensor with continuous shooting up to 40 fps electronic shutter, 6K oversampled 4K 60p video, and 8 stops In-Body Image Stabilization.",
            "price": Decimal("269995.00"),
            "discount_price": Decimal("249990.00"),
            "stock": 8,
            "rating": Decimal("4.9"),
            "review_count": 39,
            "featured": True,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Nikon Z8 Full-Frame Hybrid Camera",
            "slug": "nikon-z8-full-frame-camera",
            "brand": "Nikon",
            "category": categories["cameras"],
            "description": "Flagship 45.7MP stacked CMOS sensor with blackout-free Real-Live Viewfinder, internal 8.3K 60p N-RAW recording, and deep learning subject detection.",
            "price": Decimal("343990.00"),
            "discount_price": Decimal("319990.00"),
            "stock": 6,
            "rating": Decimal("5.0"),
            "review_count": 27,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 7,
            "image_url": "https://images.unsplash.com/photo-1512790182412-b19e6d62bc39?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "DJI Mini 4 Pro Drone with Fly More Combo",
            "slug": "dji-mini-4-pro-fly-more-combo",
            "brand": "DJI",
            "category": categories["cameras"],
            "description": "Ultralight under 249g folding drone with omnidirectional obstacle sensing, 4K/60fps HDR true vertical shooting, 20km FHD video transmission, and 34-min flight time.",
            "price": Decimal("112900.00"),
            "discount_price": Decimal("99990.00"),
            "stock": 14,
            "rating": Decimal("4.9"),
            "review_count": 68,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 11,
            "image_url": "https://images.unsplash.com/photo-1527977966376-1c8408f9f108?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "DJI Osmo Pocket 3 Creator Combo 4K Camera",
            "slug": "dji-osmo-pocket-3-creator-combo",
            "brand": "DJI",
            "category": categories["cameras"],
            "description": "1-inch CMOS sensor with 4K/120fps capture, 3-axis mechanical stabilization, 2-inch rotatable OLED touchscreen, and wireless microphone transmitter.",
            "price": Decimal("64990.00"),
            "discount_price": Decimal("58990.00"),
            "stock": 18,
            "rating": Decimal("4.8"),
            "review_count": 49,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 9,
            "image_url": "https://images.unsplash.com/photo-1508873696983-2df5293cb32f?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Sony ZV-E1 Full-Frame Vlog Camera",
            "slug": "sony-zv-e1-vlog-camera",
            "brand": "Sony",
            "category": categories["cameras"],
            "description": "World's most compact interchangeable-lens full-frame vlog camera with AI-based auto framing, cinematic Vlog setting, and multiple directional microphones.",
            "price": Decimal("214990.00"),
            "discount_price": Decimal("194990.00"),
            "stock": 7,
            "rating": Decimal("4.7"),
            "review_count": 21,
            "featured": False,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=600&auto=format&fit=crop&q=80"
        },

        # Gaming & VR (6)
        {
            "name": "Sony PlayStation 5 Slim Console (Disc Edition)",
            "slug": "sony-playstation-5-slim-disc",
            "brand": "Sony",
            "category": categories["gaming"],
            "description": "Slimmer unibody design with 1TB ultra-high speed NVMe SSD, Ray Tracing hardware acceleration, 4K 120fps HDR gaming, and 3D Tempest AudioTech.",
            "price": Decimal("54990.00"),
            "discount_price": Decimal("49990.00"),
            "stock": 25,
            "rating": Decimal("4.9"),
            "review_count": 185,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 9,
            "image_url": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "PlayStation 5 DualSense Wireless Controller (Midnight Black)",
            "slug": "ps5-dualsense-wireless-controller",
            "brand": "Sony",
            "category": categories["gaming"],
            "description": "Immersive haptic feedback, dynamic adaptive triggers, built-in microphone and headset jack with integrated motion sensor and create button.",
            "price": Decimal("5990.00"),
            "discount_price": Decimal("5490.00"),
            "stock": 45,
            "rating": Decimal("4.8"),
            "review_count": 140,
            "featured": False,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Razer BlackWidow V4 Pro RGB Mechanical Gaming Keyboard",
            "slug": "razer-blackwidow-v4-pro-keyboard",
            "brand": "Razer",
            "category": categories["gaming"],
            "description": "Tactile Green mechanical switches with dedicated command dial, 8 dedicated macro keys, magnetic plush leatherette underglow wrist rest, and Chroma RGB.",
            "price": Decimal("24999.00"),
            "discount_price": Decimal("21999.00"),
            "stock": 18,
            "rating": Decimal("4.8"),
            "review_count": 62,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 12,
            "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Logitech G502 X PLUS Wireless RGB Gaming Mouse",
            "slug": "logitech-g502-x-plus-mouse",
            "brand": "Logitech",
            "category": categories["gaming"],
            "description": "LIGHTFORCE hybrid optical-mechanical switches, HERO 25K gaming sensor with sub-micron precision, LIGHTSPEED wireless, and customizable LIGHTSYNC RGB.",
            "price": Decimal("15495.00"),
            "discount_price": Decimal("13495.00"),
            "stock": 32,
            "rating": Decimal("4.9"),
            "review_count": 95,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 13,
            "image_url": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Razer Kraken V3 Pro Wireless Haptic Gaming Headset",
            "slug": "razer-kraken-v3-pro-headset",
            "brand": "Razer",
            "category": categories["gaming"],
            "description": "Razer HyperSense haptic technology converting audio signals into real-time tactile vibrations with TriForce Titanium 50mm drivers and THX Spatial Audio.",
            "price": Decimal("19999.00"),
            "discount_price": Decimal("16999.00"),
            "stock": 20,
            "rating": Decimal("4.7"),
            "review_count": 39,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 15,
            "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Logitech G Cloud Gaming Handheld",
            "slug": "logitech-g-cloud-gaming-handheld",
            "brand": "Logitech",
            "category": categories["gaming"],
            "description": "Cloud gaming portal with 7-inch Full HD 1080p 60Hz touchscreen, precision console-grade controls, lightweight ergonomic design, and 12+ hour battery life.",
            "price": Decimal("32990.00"),
            "discount_price": Decimal("28990.00"),
            "stock": 14,
            "rating": Decimal("4.6"),
            "review_count": 25,
            "featured": False,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=600&auto=format&fit=crop&q=80"
        },

        # Tablets (5)
        {
            "name": "Apple iPad Pro 13-inch M4 Ultra Retina XDR (256GB WiFi)",
            "slug": "apple-ipad-pro-13-m4",
            "brand": "Apple",
            "category": categories["tablets"],
            "description": "The world's thinnest Apple product with revolutionary Tandem OLED display, groundbreaking M4 chip with next-gen Neural Engine, and Apple Pencil Pro support.",
            "price": Decimal("129900.00"),
            "discount_price": Decimal("122900.00"),
            "stock": 16,
            "rating": Decimal("5.0"),
            "review_count": 58,
            "featured": True,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Samsung Galaxy Tab S9 Ultra (14.6-inch Dynamic AMOLED 2X)",
            "slug": "samsung-galaxy-tab-s9-ultra",
            "brand": "Samsung",
            "category": categories["tablets"],
            "description": "Massive 14.6-inch 120Hz AMOLED canvas with Snapdragon 8 Gen 2 for Galaxy, IP68 water & dust resistance, bidirectional S Pen charging included.",
            "price": Decimal("108999.00"),
            "discount_price": Decimal("99999.00"),
            "stock": 12,
            "rating": Decimal("4.8"),
            "review_count": 42,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 8,
            "image_url": "https://images.unsplash.com/photo-1561154464-82e9adf32764?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Apple iPad Air 11-inch M2 (128GB WiFi Space Grey)",
            "slug": "apple-ipad-air-11-m2",
            "brand": "Apple",
            "category": categories["tablets"],
            "description": "Supercharged by the Apple M2 chip with Liquid Retina display, landscape 12MP front camera with Center Stage, and superfast Wi-Fi 6E connectivity.",
            "price": Decimal("59900.00"),
            "discount_price": Decimal("54900.00"),
            "stock": 25,
            "rating": Decimal("4.8"),
            "review_count": 76,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 8,
            "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Lenovo Tab P12 Pro with Precision Pen 3",
            "slug": "lenovo-tab-p12-pro",
            "brand": "Lenovo",
            "category": categories["tablets"],
            "description": "12.6-inch 2K 120Hz AMOLED Dolby Vision display with quad JBL speakers tuned by Dolby Atmos, Qualcomm Snapdragon 870, and all-day 10,200mAh battery.",
            "price": Decimal("64999.00"),
            "discount_price": Decimal("54999.00"),
            "stock": 15,
            "rating": Decimal("4.6"),
            "review_count": 28,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 15,
            "image_url": "https://images.unsplash.com/photo-1589739900243-4b52cd9b104e?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Apple iPad 10th Gen 64GB (Blue)",
            "slug": "apple-ipad-10th-gen-blue",
            "brand": "Apple",
            "category": categories["tablets"],
            "description": "All-screen design with 10.9-inch Liquid Retina display, A14 Bionic chip, 12MP Ultra Wide front camera with Center Stage, and USB-C port.",
            "price": Decimal("39900.00"),
            "discount_price": Decimal("34900.00"),
            "stock": 35,
            "rating": Decimal("4.7"),
            "review_count": 92,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 13,
            "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&auto=format&fit=crop&q=80"
        },

        # Accessories & Power (5)
        {
            "name": "Anker 737 Power Bank (PowerCore 24K 140W)",
            "slug": "anker-737-power-bank-24k",
            "brand": "Anker",
            "category": categories["accessories"],
            "description": "Equipped with Power Delivery 3.1 and bi-directional technology to quickly recharge the portable charger or get a 140W ultra-powerful charge with smart digital display.",
            "price": Decimal("14999.00"),
            "discount_price": Decimal("12499.00"),
            "stock": 40,
            "rating": Decimal("4.9"),
            "review_count": 135,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 17,
            "image_url": "https://images.unsplash.com/photo-1609592426505-59b0d1e57c66?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Apple MagSafe Duo Charger",
            "slug": "apple-magsafe-duo-charger",
            "brand": "Apple",
            "category": categories["accessories"],
            "description": "Conveniently charges your compatible iPhone, Apple Watch, Wireless Charging Case for AirPods, and other Qi-certified devices in a folding compact travel form.",
            "price": Decimal("13900.00"),
            "discount_price": Decimal("12490.00"),
            "stock": 25,
            "rating": Decimal("4.6"),
            "review_count": 68,
            "featured": False,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1622445262464-84b1456045b6?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Logitech MX Master 3S Wireless Performance Mouse",
            "slug": "logitech-mx-master-3s-mouse",
            "brand": "Logitech",
            "category": categories["accessories"],
            "description": "Iconic ergonomic shape with Quiet Clicks, 8,000 DPI track-on-glass sensor, MagSpeed Electromagnetic scrolling, and multi-computer Flow control.",
            "price": Decimal("10995.00"),
            "discount_price": Decimal("9495.00"),
            "stock": 35,
            "rating": Decimal("5.0"),
            "review_count": 194,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 14,
            "image_url": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Logitech MX Keys S Wireless Illuminated Keyboard",
            "slug": "logitech-mx-keys-s-keyboard",
            "brand": "Logitech",
            "category": categories["accessories"],
            "description": "Low-profile spherically-dished keys matching your fingertips, smart ambient backlighting that turns on as hands approach, and custom Smart Actions shortcuts.",
            "price": Decimal("12995.00"),
            "discount_price": Decimal("11495.00"),
            "stock": 28,
            "rating": Decimal("4.9"),
            "review_count": 87,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 12,
            "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Anker Prime 240W 4-Port GaN Desktop Charger",
            "slug": "anker-prime-240w-gan-charger",
            "brand": "Anker",
            "category": categories["accessories"],
            "description": "Ultra-fast charging hub with 3 USB-C and 1 USB-A port delivering up to 140W from a single port, GaNPrime technology, and ActiveShield 2.0 temperature monitoring.",
            "price": Decimal("16999.00"),
            "discount_price": Decimal("14499.00"),
            "stock": 20,
            "rating": Decimal("4.8"),
            "review_count": 45,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 15,
            "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&auto=format&fit=crop&q=80"
        },
        # Smart Home (4)
        {
            "name": "Amazon Echo Show 10 (3rd Gen) with Motion",
            "slug": "amazon-echo-show-10",
            "brand": "Amazon",
            "category": categories["smart-home"],
            "description": "10.1-inch HD smart display designed to move with you during video calls, premium directional sound, built-in Zigbee smart home hub, and 13MP auto-framing camera.",
            "price": Decimal("24999.00"),
            "discount_price": Decimal("21999.00"),
            "stock": 18,
            "rating": Decimal("4.7"),
            "review_count": 78,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 12,
            "image_url": "https://images.unsplash.com/photo-1543512214-318c7553f230?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Apple HomePod (2nd Gen) Midnight",
            "slug": "apple-homepod-2nd-gen",
            "brand": "Apple",
            "category": categories["smart-home"],
            "description": "High-fidelity computational audio with room sensing, Spatial Audio with Dolby Atmos, Siri intelligence, Matter smart home connectivity, and built-in temperature sensor.",
            "price": Decimal("32900.00"),
            "discount_price": Decimal("29990.00"),
            "stock": 15,
            "rating": Decimal("4.8"),
            "review_count": 56,
            "featured": False,
            "is_deal": False,
            "deal_discount_percent": 0,
            "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Google Nest Cam Outdoor/Indoor (Battery)",
            "slug": "google-nest-cam-battery",
            "brand": "Google",
            "category": categories["smart-home"],
            "description": "Wire-free HDR smart security camera with intelligent vehicle, person, and animal alerts, 3 hours of free event video history, and weather-resistant magnetic mount.",
            "price": Decimal("17999.00"),
            "discount_price": Decimal("15499.00"),
            "stock": 22,
            "rating": Decimal("4.6"),
            "review_count": 42,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 14,
            "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Philips Hue White & Color Ambiance Starter Kit",
            "slug": "philips-hue-starter-kit",
            "brand": "Philips",
            "category": categories["smart-home"],
            "description": "Includes 3 E27 smart LED bulbs with 16 million colors, Hue Bridge controller, and smart dimmer switch with seamless Alexa, Apple HomeKit and Google Assistant integration.",
            "price": Decimal("14999.00"),
            "discount_price": Decimal("12999.00"),
            "stock": 30,
            "rating": Decimal("4.9"),
            "review_count": 110,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 13,
            "image_url": "https://images.unsplash.com/photo-1550985543-f47f38aeee65?w=600&auto=format&fit=crop&q=80"
        },
        # Monitors & Displays (3)
        {
            "name": "LG UltraGear 34-inch Curved OLED 240Hz Monitor",
            "slug": "lg-ultragear-34-curved-oled",
            "brand": "LG",
            "category": categories["monitors"],
            "description": "WQHD (3440 x 1440) 800R curved OLED gaming monitor featuring 0.03ms response time, 240Hz refresh rate, 98.5% DCI-P3 color gamut, and NVIDIA G-SYNC compatibility.",
            "price": Decimal("129999.00"),
            "discount_price": Decimal("114999.00"),
            "stock": 10,
            "rating": Decimal("4.9"),
            "review_count": 64,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 11,
            "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Dell UltraSharp 32-inch 4K USB-C Hub Monitor (U3223QE)",
            "slug": "dell-ultrasharp-32-4k-u3223qe",
            "brand": "Dell",
            "category": categories["monitors"],
            "description": "IPS Black technology with 2000:1 contrast ratio, 4K UHD 3840x2160 clarity, 90W USB-C power delivery, integrated RJ45 ethernet, and built-in KVM switch.",
            "price": Decimal("84999.00"),
            "discount_price": Decimal("74999.00"),
            "stock": 14,
            "rating": Decimal("4.8"),
            "review_count": 52,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 12,
            "image_url": "https://images.unsplash.com/photo-1585792180666-f7347c490ee2?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Samsung Odyssey OLED G8 34-inch Curved Gaming Monitor",
            "slug": "samsung-odyssey-oled-g8-34",
            "brand": "Samsung",
            "category": categories["monitors"],
            "description": "Neo Quantum Processor with vibrant OLED color, 175Hz refresh rate, 0.03ms response time, CoreSync ambient lighting, and Gaming Hub cloud gaming built-in.",
            "price": Decimal("119999.00"),
            "discount_price": Decimal("104999.00"),
            "stock": 8,
            "rating": Decimal("4.8"),
            "review_count": 39,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 13,
            "image_url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600&auto=format&fit=crop&q=80"
        },
        # Storage & Networking (3)
        {
            "name": "Samsung 990 PRO 2TB PCIe 4.0 NVMe SSD with Heatsink",
            "slug": "samsung-990-pro-2tb-heatsink",
            "brand": "Samsung",
            "category": categories["storage"],
            "description": "Blazing read/write speeds up to 7,450/6,900 MB/s, built-in futuristic heatsink optimized for PlayStation 5 and high-end desktop gaming rigs.",
            "price": Decimal("22999.00"),
            "discount_price": Decimal("18999.00"),
            "stock": 40,
            "rating": Decimal("5.0"),
            "review_count": 130,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 17,
            "image_url": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "SanDisk Extreme PRO 2TB Portable NVMe External SSD",
            "slug": "sandisk-extreme-pro-2tb-ssd",
            "brand": "SanDisk",
            "category": categories["storage"],
            "description": "Rugged IP65 water and dust resistant forged aluminum chassis delivering up to 2000MB/s NVMe transfer speeds for 8K video editors and outdoor photographers.",
            "price": Decimal("24999.00"),
            "discount_price": Decimal("21499.00"),
            "stock": 35,
            "rating": Decimal("4.9"),
            "review_count": 92,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 14,
            "image_url": "https://images.unsplash.com/photo-1531492746076-161ca9bcad58?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Netgear Nighthawk AXE7800 Tri-Band WiFi 6E Router",
            "slug": "netgear-nighthawk-axe7800-router",
            "brand": "Netgear",
            "category": categories["storage"],
            "description": "Next-gen 6GHz band delivering combined WiFi speeds up to 7.8Gbps across 8 simultaneous streams, 2.5G Multi-Gig ethernet port, and NETGEAR Armor cybersecurity.",
            "price": Decimal("38999.00"),
            "discount_price": Decimal("32999.00"),
            "stock": 12,
            "rating": Decimal("4.7"),
            "review_count": 34,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 15,
            "image_url": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&auto=format&fit=crop&q=80"
        },
        # Audio & Creator Peripherals (4)
        {
            "name": "Sennheiser Momentum 4 Wireless ANC Headphones",
            "slug": "sennheiser-momentum-4-wireless",
            "brand": "Sennheiser",
            "category": categories["audio"],
            "description": "Audiophile-inspired 42mm transducer system, adaptive noise cancellation, crystal-clear voice pick-up, and an astounding 60-hour battery life with fast charging.",
            "price": Decimal("34990.00"),
            "discount_price": Decimal("28990.00"),
            "stock": 20,
            "rating": Decimal("4.8"),
            "review_count": 68,
            "featured": True,
            "is_deal": True,
            "deal_discount_percent": 17,
            "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Nothing Ear (2) True Wireless Hi-Res Earbuds",
            "slug": "nothing-ear-2-wireless-earbuds",
            "brand": "Nothing",
            "category": categories["audio"],
            "description": "Iconic transparent dual-chamber design with LHDC 5.0 Hi-Res Audio certification, personalized active noise cancellation, and dual connection device pairing.",
            "price": Decimal("9999.00"),
            "discount_price": Decimal("8499.00"),
            "stock": 30,
            "rating": Decimal("4.7"),
            "review_count": 115,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 15,
            "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "SteelSeries Apex Pro TKL Mechanical Gaming Keyboard",
            "slug": "steelseries-apex-pro-tkl-keyboard",
            "brand": "SteelSeries",
            "category": categories["gaming"],
            "description": "World's fastest OmniPoint 2.0 adjustable hypermagnetic switches with 0.2mm to 3.8mm actuation, OLED Smart Display command center, and aircraft-grade aluminum frame.",
            "price": Decimal("23999.00"),
            "discount_price": Decimal("19999.00"),
            "stock": 16,
            "rating": Decimal("4.9"),
            "review_count": 48,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 17,
            "image_url": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=600&auto=format&fit=crop&q=80"
        },
        {
            "name": "Belkin BoostCharge Pro 3-in-1 MagSafe Wireless Stand",
            "slug": "belkin-boostcharge-pro-3in1-stand",
            "brand": "Belkin",
            "category": categories["accessories"],
            "description": "Official 15W MagSafe fast charging stand engineered for iPhone, Apple Watch Ultra fast charging, and dedicated wireless tray for AirPods Pro.",
            "price": Decimal("13999.00"),
            "discount_price": Decimal("11999.00"),
            "stock": 25,
            "rating": Decimal("4.8"),
            "review_count": 62,
            "featured": False,
            "is_deal": True,
            "deal_discount_percent": 14,
            "image_url": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600&auto=format&fit=crop&q=80"
        }
    ]

    for p in raw_products:
        prod, created = Product.objects.update_or_create(
            slug=p["slug"],
            defaults=p
        )
        if created:
            print(f"Created product: {prod.name}")
        else:
            print(f"Updated product: {prod.name}")

    print(f"[PASS] Total Products in Database: {Product.objects.count()}")

    # 4. Setup 5 Verified Customer Testimonials
    testimonials_data = [
        {
            "name": "Vikramaditya Singhania",
            "role_or_title": "Verified Buyer • Founder at DevMatrix",
            "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
            "rating": 5,
            "content": "Nexus Electronics is hands down the most seamless tech shopping experience in India. Ordered the MacBook Pro M3 Max and it arrived within 24 hours in Bangalore in flawless condition. The 3D product view gave me exact spatial clarity before buying!"
        },
        {
            "name": "Priyanka Nair",
            "role_or_title": "Verified Buyer • Lead Sound Designer",
            "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
            "rating": 5,
            "content": "Purchased the Sony WH-1000XM5 headphones during their flash deals. Authentic brand warranty, immediate shipment updates via WhatsApp, and zero pricing hidden fees. Absolutely world-class customer service."
        },
        {
            "name": "Rohan Mehta",
            "role_or_title": "Verified Buyer • Commercial Drone Filmmaker",
            "avatar_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
            "rating": 5,
            "content": "Getting authentic DJI gear in Mumbai has never been this stress-free. The transparent INR checkout and instantaneous receipt generation makes claiming GST input credits an absolute breeze."
        },
        {
            "name": "Ananya Sen",
            "role_or_title": "Verified Buyer • Creative Director",
            "avatar_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80",
            "rating": 5,
            "content": "The iPad Pro M4 Tandem OLED is a masterpiece. Nexus Electronics provided free expedited shipping above ₹5,000, and their packaging was extraordinarily protective. Highly recommended!"
        },
        {
            "name": "Karthik Rajagopalan",
            "role_or_title": "Verified Buyer • Esports Athlete",
            "avatar_url": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150&auto=format&fit=crop&q=80",
            "rating": 5,
            "content": "Ordered the Razer BlackWidow V4 Pro and Logitech G502 X PLUS. The tactile switches feel incredible and the live shipment tracking was pinpoint accurate. Nexus is my go-to tech store."
        }
    ]

    for t in testimonials_data:
        Testimonial.objects.update_or_create(
            name=t["name"],
            defaults=t
        )

    print("[PASS] Testimonials seeded successfully.")

    # 5. Setup Sample Customer Orders
    if Order.objects.count() < 3:
        p1 = Product.objects.get(slug="apple-iphone-15-pro-max-256gb")
        p2 = Product.objects.get(slug="sony-wh-1000xm5-headphones")
        
        ord1 = Order.objects.create(
            user=demo_user,
            order_number="NEX-2026-08912",
            first_name="Rahul",
            last_name="Sharma",
            email="rahul.sharma@example.com",
            phone="+91 91234 56789",
            address="104 Tech Park, Koramangala 5th Block",
            city="Bengaluru",
            state="Karnataka",
            postal_code="560095",
            country="India",
            subtotal=p1.current_price + p2.current_price,
            shipping_fee=Decimal("0.00"),
            total_amount=p1.current_price + p2.current_price,
            payment_method="Test Payment",
            payment_status="Paid",
            order_status="Delivered"
        )
        OrderItem.objects.create(order=ord1, product=p1, product_name=p1.name, price=p1.current_price, quantity=1, subtotal=p1.current_price)
        OrderItem.objects.create(order=ord1, product=p2, product_name=p2.name, price=p2.current_price, quantity=1, subtotal=p2.current_price)
        print("[PASS] Sample delivered order created.")

    print("\nDATABASE SEEDING COMPLETED SUCCESSFULLY! [PASS]\n")

if __name__ == '__main__':
    run_seed()
