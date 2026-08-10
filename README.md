# 🛍️ Nexus Electronics — Django E-Commerce Platform

<p align="center">
  <strong>A modern, colorful, responsive and fully database-connected Django E-Commerce platform.</strong>
</p>

<p align="center">
  Built with Django • SQLite • HTML • CSS • JavaScript
</p>

---

## 📌 Overview

**Nexus Electronics** is a complete full-stack Django E-Commerce application designed with a premium electronics-shopping experience.

The UI is inspired by modern high-end e-commerce layouts, featuring a dark obsidian and neon-violet hero, colorful product cards, promotional sections, flash deals, new arrivals, best sellers, customer services, testimonials, newsletter subscription and a professional footer.

The project is not just a static frontend. Core functionality is connected to the Django backend and database, including products, categories, authentication, cart, wishlist, checkout, orders, stock management, contact messages and an administrative dashboard.

---

## ✨ Features

### 🏠 Home Page

- Premium hero section with interactive carousel
- Neon-violet visual theme
- Dynamic product categories
- Category product counts
- Promotional Bento grid
- Featured collections
- Flash Deals
- Live countdown timer
- New Arrivals
- Best Sellers
- Trust & Service section
- App promotion
- Customer testimonials
- Newsletter subscription
- Premium footer

### 🛒 Product System

- Product catalog
- Product details
- Product images
- Categories
- Brands
- Discount prices
- Stock management
- Featured products
- Deal products
- Ratings and review counts
- Search
- Category filtering
- Brand filtering
- Deal filtering
- Sorting
- Pagination
- Related products

### 👤 Authentication

- User registration
- User login
- User logout
- Password hashing through Django authentication
- Automatic customer profile creation
- Customer profile information

### 🛍️ Shopping Cart

- Add products to cart
- AJAX Add to Cart
- Increase quantity
- Decrease quantity
- Remove items
- Stock limit validation
- Dynamic cart count
- Subtotal calculation
- Shipping fee calculation
- Free shipping threshold

### ❤️ Wishlist

- Add/remove wishlist items
- Guest session wishlist support
- Logged-in customer wishlist
- Dynamic wishlist counter

### 💳 Checkout & Orders

- Checkout form
- Shipping information
- Cash on Delivery
- Test Payment
- Order creation
- Unique order number
- Order item snapshots
- Automatic stock deduction
- Cart clearing after successful order
- Order confirmation
- My Orders page
- Order status tracking

### 📊 Admin Dashboard

- Total Products
- Total Customers
- Total Orders
- Total Revenue
- Pending Orders
- Delivered Orders
- Out of Stock products
- Product CRUD
- Category CRUD
- Order status management
- Customer directory
- Customer order/spending metrics
- Contact message management

### 📩 Customer Communication

- Contact form
- Database-backed contact messages
- Mark-as-read support messages
- Newsletter subscription
- Testimonials

---

## 🎨 UI / UX

The application uses a modern visual system with:

- Dark obsidian backgrounds
- Neon violet/purple gradients
- Clean white layouts
- Rounded cards
- Soft shadows
- Product hover effects
- Responsive layouts
- Smooth transitions
- Modern icons
- Sticky navigation
- Mobile navigation drawer
- Toast notifications
- Empty states
- Responsive product grids

The design is optimized for:

- 📱 Mobile
- 📱 Tablet
- 💻 Laptop
- 🖥️ Desktop

---

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| SQLite | Development database |
| HTML5 | Page structure |
| CSS3 | Styling and responsive UI |
| JavaScript | Interactions and dynamic UI |
| Django ORM | Database operations |
| AJAX / Fetch | Cart and wishlist interactions |

---

## 📁 Project Structure

```text
Ecommerce/
│
├── Ecommerce/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── Customers/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── context_processors.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── products/
│   ├── accounts/
│   ├── cart/
│   ├── orders/
│   └── admin/
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── responsive.css
│   │
│   └── js/
│       ├── main.js
│       ├── cart.js
│       ├── countdown.js
│       └── slider.js
│
├── db.sqlite3
├── manage.py
├── seed_database.py
└── README.md
```

---

## 🗄️ Database Models

The application includes the following major models:

### Category

Stores product categories.

### Product

Stores:

- Product name
- Description
- Price
- Discount price
- Category
- Brand
- Stock
- Image
- Featured status
- Deal status
- Rating
- Review count
- Slug
- Product status

### CustomerProfile

Stores additional customer information such as:

- Phone
- Address
- City
- State
- Postal code
- Country
- Profile picture

### Cart & CartItem

Handles customer shopping carts and item quantities.

### Wishlist

Stores wishlist products for customers and guest sessions.

### Order & OrderItem

Stores completed orders and individual order items.

### ContactMessage

Stores customer support/contact requests.

### NewsletterSubscriber

Stores newsletter subscribers.

### Testimonial

Stores customer reviews/testimonials.

---

## 🔄 Customer Shopping Flow

```text
Home
  ↓
Shop
  ↓
Search / Filter
  ↓
Product Details
  ↓
Add to Cart
  ↓
Cart
  ↓
Checkout
  ↓
Place Order
  ↓
Stock Deduction
  ↓
Order Confirmation
  ↓
My Orders
```

---

## 🔐 Admin Flow

```text
Admin Login
    ↓
Dashboard
    ↓
Products
    ├── Add Product
    ├── Edit Product
    └── Delete Product
    ↓
Categories
    ├── Add
    ├── Edit
    └── Delete
    ↓
Customers
    ↓
Orders
    ↓
Update Order Status
    ↓
Contact Messages
```

---

## 🧪 Testing

The project includes an automated integration test suite in:

```text
Customers/tests.py
```

### Test Result

```text
Found 9 test(s).

System check identified no issues (0 silenced).

.........
----------------------------------------------------------------------
Ran 9 tests in 20.185s

OK
```

### Verified Features

1. Home page loading
2. Product catalog and filters
3. Product details
4. User registration and login
5. Cart lifecycle and stock limits
6. Checkout and order placement
7. Wishlist toggle
8. Contact and newsletter submissions
9. Admin dashboard and CRUD operations

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd Ecommerce
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Django

```bash
pip install django
```

If the project contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Seed demo data

Optional:

```bash
python seed_database.py
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 👨‍💼 Demo Admin Account

For local development/testing:

```text
Username: admin
Password: admin123
```

Admin dashboard:

```text
http://127.0.0.1:8000/dashboard/
```

or:

```text
http://127.0.0.1:8000/admin-dashboard/
```

> ⚠️ Change demo credentials before using the application in a real production environment.

---

## 👤 Demo Customer Account

```text
Username: johndoe
Password: password123
```

> ⚠️ These credentials are intended for local development/testing only.

---

## 🧪 Run Tests

Run the complete test suite with:

```bash
python manage.py test Customers
```

Or:

```bash
python manage.py test
```

---

## ⚙️ Useful Django Commands

Check the project:

```bash
python manage.py check
```

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Run the server:

```bash
python manage.py runserver
```

---

## 📱 Responsive Design

The interface is designed to adapt to:

- Mobile phones
- Tablets
- Laptops
- Desktop monitors
- Large screens

Responsive behavior includes:

- Mobile navigation drawer
- Responsive product grids
- Horizontal category scrolling
- Adaptive hero section
- Responsive promotional cards
- Mobile-friendly checkout
- Responsive dashboard tables

---

## 🔒 Security

The project uses Django security features including:

- CSRF protection
- Django authentication
- Password hashing
- Login-required pages
- Staff-only dashboard access
- Form validation
- Database-backed operations

Never use the demo credentials in production.

---

## 📈 Future Improvements

Possible future enhancements:

- Real payment gateway integration
- Product reviews and ratings submission
- Advanced product image gallery
- Coupon and promo-code system
- PDF invoice generation
- Email order notifications
- Advanced sales analytics
- Redis caching
- REST API
- React frontend
- Production deployment
- Cloud image storage
- PostgreSQL production database

---

## 🌟 Project Highlights

- ✅ Full-stack Django application
- ✅ Database-connected Ecommerce system
- ✅ Premium responsive UI
- ✅ Product management
- ✅ Category management
- ✅ Authentication
- ✅ Cart
- ✅ Wishlist
- ✅ Checkout
- ✅ Orders
- ✅ Stock management
- ✅ Admin dashboard
- ✅ Contact management
- ✅ Newsletter
- ✅ Automated tests

---

## 📄 License

This project is intended for educational and development purposes.

---

## 👨‍💻 Author

**Nexus Electronics**

Built as a full-stack Django E-Commerce project with a focus on modern UI/UX, functionality and responsive design.
