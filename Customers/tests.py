import os
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Customers.models import (
    Category, Product, CustomerProfile, Cart, CartItem,
    Wishlist, Order, OrderItem, ContactMessage, NewsletterSubscriber, Testimonial
)

class EcommerceEndToEndTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create Category
        self.category = Category.objects.create(
            name="Audio & Sound",
            slug="audio-sound",
            icon="fa-headphones",
            description="High fidelity audio gear"
        )

        # Create Products
        self.product1 = Product.objects.create(
            name="Sony WH-1000XM5",
            slug="sony-wh-1000xm5",
            category=self.category,
            brand="Sony",
            price=Decimal("399.00"),
            discount_price=Decimal("299.00"),
            stock=10,
            featured=True,
            is_deal=True,
            rating=Decimal("4.9"),
            review_count=150,
            status="Available",
            is_active=True
        )

        self.product2 = Product.objects.create(
            name="AirPods Pro USB-C",
            slug="airpods-pro-usb-c",
            category=self.category,
            brand="Apple",
            price=Decimal("249.00"),
            discount_price=None,
            stock=5,
            featured=False,
            is_deal=False,
            rating=Decimal("4.8"),
            review_count=80,
            status="Available",
            is_active=True
        )

        # Create Normal User
        self.user = User.objects.create_user(
            username="testcustomer",
            email="customer@example.com",
            password="testpassword123",
            first_name="Alice",
            last_name="Smith"
        )
        CustomerProfile.objects.create(
            user=self.user,
            phone="+1 555-0192",
            address="123 Silicon Ave",
            city="Tech City",
            state="CA",
            postal_code="94016",
            country="USA"
        )

        # Create Staff / Admin User
        self.admin_user = User.objects.create_superuser(
            username="testadmin",
            email="admin@example.com",
            password="adminpassword123"
        )

    def test_01_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Future Technology")
        self.assertContains(response, "Audio")
        self.assertContains(response, "Sony WH-1000XM5")

    def test_02_product_catalog_and_filters(self):
        # 1. All products
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sony WH-1000XM5")
        self.assertContains(response, "AirPods Pro USB-C")

        # 2. Search query
        response = self.client.get(reverse('products') + '?q=Sony')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sony WH-1000XM5")
        self.assertNotContains(response, "AirPods Pro USB-C")

        # 3. Category filter
        response = self.client.get(reverse('products') + '?category=audio-sound')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sony WH-1000XM5")

        # 4. Deals filter
        response = self.client.get(reverse('products') + '?deals=1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sony WH-1000XM5")
        self.assertNotContains(response, "AirPods Pro USB-C")

    def test_03_product_detail_page(self):
        response = self.client.get(reverse('product_detail', kwargs={'slug': self.product1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sony WH-1000XM5")
        self.assertContains(response, "$299.00")
        self.assertContains(response, "In Stock")

    def test_04_user_registration_and_login(self):
        # Register new user
        reg_response = self.client.post(reverse('register'), {
            'first_name': 'Bob',
            'last_name': 'Jones',
            'username': 'bobjones',
            'email': 'bob@example.com',
            'password': 'secretpassword123',
            'confirm_password': 'secretpassword123'
        })
        self.assertEqual(reg_response.status_code, 302)
        self.assertTrue(User.objects.filter(username='bobjones').exists())
        new_user = User.objects.get(username='bobjones')
        self.assertTrue(hasattr(new_user, 'profile'))

        # Logout & Login
        self.client.get(reverse('logout'))
        login_response = self.client.post(reverse('login'), {
            'username': 'bobjones',
            'password': 'secretpassword123'
        })
        self.assertEqual(login_response.status_code, 302)

    def test_05_cart_lifecycle_and_stock_limits(self):
        self.client.login(username="testcustomer", password="testpassword123")

        # 1. Add to cart
        add_response = self.client.post(
            reverse('add_to_cart', kwargs={'product_id': self.product1.id}),
            {'quantity': 2}
        )
        self.assertEqual(add_response.status_code, 302)

        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.get_total_items(), 2)
        self.assertEqual(cart.get_subtotal(), Decimal("598.00")) # 2 * 299.00

        # 2. Update quantity
        item = cart.items.first()
        update_response = self.client.post(
            reverse('update_cart_item', kwargs={'item_id': item.id}),
            {'action': 'increase'}
        )
        self.assertEqual(update_response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 3)

        # 3. View cart page
        cart_page = self.client.get(reverse('cart'))
        self.assertEqual(cart_page.status_code, 200)
        self.assertContains(cart_page, "Sony WH-1000XM5")

    def test_06_checkout_and_order_placement_with_stock_deduction(self):
        self.client.login(username="testcustomer", password="testpassword123")

        # Add 3 units of product2 (Initial stock: 5)
        self.client.post(
            reverse('add_to_cart', kwargs={'product_id': self.product2.id}),
            {'quantity': 3}
        )

        initial_stock = self.product2.stock

        # Place Order
        order_response = self.client.post(reverse('place_order'), {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'customer@example.com',
            'phone': '+1 555-0192',
            'address': '123 Silicon Ave',
            'city': 'Tech City',
            'state': 'CA',
            'postal_code': '94016',
            'country': 'USA',
            'payment_method': 'Test Payment',
            'order_notes': 'Please deliver before 5 PM'
        })
        self.assertEqual(order_response.status_code, 302)

        # Verify Order was created
        order = Order.objects.filter(user=self.user).latest('created_at')
        self.assertTrue(order.order_number.startswith("NEX-"))
        self.assertEqual(order.payment_status, "Paid")
        self.assertEqual(order.items.count(), 1)

        # Verify stock was reduced in database
        self.product2.refresh_from_db()
        self.assertEqual(self.product2.stock, initial_stock - 3)

        # Verify cart was cleared
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)

        # Verify order success receipt page
        success_page = self.client.get(reverse('order_success', kwargs={'order_number': order.order_number}))
        self.assertEqual(success_page.status_code, 200)
        self.assertContains(success_page, order.order_number)

        # Verify My Orders page
        my_orders_page = self.client.get(reverse('my_orders'))
        self.assertEqual(my_orders_page.status_code, 200)
        self.assertContains(my_orders_page, order.order_number)

    def test_07_wishlist_toggle(self):
        self.client.login(username="testcustomer", password="testpassword123")

        # Toggle Wishlist ON
        toggle_res = self.client.post(reverse('toggle_wishlist', kwargs={'product_id': self.product1.id}))
        self.assertEqual(toggle_res.status_code, 302)
        self.assertTrue(Wishlist.objects.filter(user=self.user, product=self.product1).exists())

        # Toggle Wishlist OFF
        toggle_res2 = self.client.post(reverse('toggle_wishlist', kwargs={'product_id': self.product1.id}))
        self.assertEqual(toggle_res2.status_code, 302)
        self.assertFalse(Wishlist.objects.filter(user=self.user, product=self.product1).exists())

    def test_08_contact_and_newsletter_submissions(self):
        # Contact message submission
        contact_res = self.client.post(reverse('contact'), {
            'name': 'Charlie Puth',
            'email': 'charlie@music.com',
            'subject': 'Headphone recommendation',
            'message': 'Which headphones are best for studio monitoring?'
        })
        self.assertEqual(contact_res.status_code, 302)
        self.assertTrue(ContactMessage.objects.filter(email='charlie@music.com').exists())

        # Newsletter subscriber submission
        news_res = self.client.post(reverse('newsletter_subscribe'), {
            'email': 'techgeek@future.io'
        })
        self.assertEqual(news_res.status_code, 302)
        self.assertTrue(NewsletterSubscriber.objects.filter(email='techgeek@future.io').exists())

    def test_09_admin_dashboard_and_crud_operations(self):
        # Unauthorized access denied for regular user
        self.client.login(username="testcustomer", password="testpassword123")
        res_unauth = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(res_unauth.status_code, 302) # Redirects to login

        # Admin login
        self.client.login(username="testadmin", password="adminpassword123")

        # 1. Admin Dashboard Loads with Real Metrics
        dash_res = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(dash_res.status_code, 200)
        self.assertContains(dash_res, "Store Analytics & Operations")

        # 2. Admin Add Product
        add_p_res = self.client.post(reverse('admin_product_add'), {
            'name': 'Razer Viper V3 Pro',
            'brand': 'Razer',
            'price': '159.99',
            'stock': 18,
            'description': 'Ultra-lightweight wireless esports gaming mouse.',
            'status': 'Available',
            'is_active': True
        })
        self.assertEqual(add_p_res.status_code, 302)
        self.assertTrue(Product.objects.filter(name='Razer Viper V3 Pro').exists())
        new_prod = Product.objects.get(name='Razer Viper V3 Pro')

        # 3. Admin Edit Product
        edit_p_res = self.client.post(reverse('admin_product_edit', kwargs={'product_id': new_prod.id}), {
            'name': 'Razer Viper V3 Pro (White Edition)',
            'brand': 'Razer',
            'price': '169.99',
            'stock': 20,
            'description': 'Updated description.',
            'status': 'Available',
            'is_active': True
        })
        self.assertEqual(edit_p_res.status_code, 302)
        new_prod.refresh_from_db()
        self.assertEqual(new_prod.name, 'Razer Viper V3 Pro (White Edition)')

        # 4. Admin Delete Product
        del_p_res = self.client.post(reverse('admin_product_delete', kwargs={'product_id': new_prod.id}))
        self.assertEqual(del_p_res.status_code, 302)
        self.assertFalse(Product.objects.filter(id=new_prod.id).exists())

        # 5. Admin Category Management
        add_cat_res = self.client.post(reverse('admin_category_add'), {
            'name': 'Drones & Robotics',
            'icon': 'fa-drone',
            'description': 'Autonomous aerial cameras',
            'is_active': True
        })
        self.assertEqual(add_cat_res.status_code, 302)
        self.assertTrue(Category.objects.filter(name='Drones & Robotics').exists())

        # 6. Admin Customer List
        cust_res = self.client.get(reverse('admin_customers'))
        self.assertEqual(cust_res.status_code, 200)
        self.assertContains(cust_res, "testcustomer")
