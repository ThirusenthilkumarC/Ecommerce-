from django.urls import path
from . import views

urlpatterns = [
    # Storefront & Catalog
    path("", views.home, name="home"),
    path("products/", views.products_list, name="products"),
    path("products/<int:id>/", views.product_detail, name="product_detail_by_id"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("deals/", views.deals_view, name="deals"),
    path("new-arrivals/", views.new_arrivals_view, name="new_arrivals"),
    path("brands/", views.brands_view, name="brands"),

    # Cart & Wishlist
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/", views.update_cart_item, name="update_cart_item"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/clear/", views.clear_cart, name="clear_cart"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("wishlist/toggle/<int:product_id>/", views.toggle_wishlist, name="toggle_wishlist"),

    # Checkout & Orders
    path("checkout/", views.checkout_view, name="checkout"),
    path("place-order/", views.place_order, name="place_order"),
    path("order-success/<str:order_number>/", views.order_success, name="order_success"),
    path("orders/", views.my_orders, name="my_orders"),
    path("orders/<str:order_number>/", views.order_detail_view, name="order_detail"),
    path("track-order/", views.track_order_lookup, name="track_order"),

    # Authentication & Profile
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),

    # Information, Currency & Language
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
    path("newsletter/subscribe/", views.newsletter_subscribe, name="newsletter_subscribe"),
    path("set-currency/", views.set_currency, name="set_currency"),
    path("set-language/", views.set_language, name="set_language"),

    # Custom Admin Management Dashboard
    path("dashboard/", views.admin_dashboard, name="dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/products/", views.admin_products_list, name="admin_products"),
    path("admin-dashboard/products/add/", views.admin_product_add, name="admin_product_add"),
    path("admin-dashboard/products/edit/<int:product_id>/", views.admin_product_edit, name="admin_product_edit"),
    path("admin-dashboard/products/delete/<int:product_id>/", views.admin_product_delete, name="admin_product_delete"),
    path("admin-dashboard/categories/", views.admin_categories_list, name="admin_categories"),
    path("admin-dashboard/categories/add/", views.admin_category_add, name="admin_category_add"),
    path("admin-dashboard/categories/edit/<int:category_id>/", views.admin_category_edit, name="admin_category_edit"),
    path("admin-dashboard/categories/delete/<int:category_id>/", views.admin_category_delete, name="admin_category_delete"),
    path("admin-dashboard/orders/", views.admin_orders_list, name="admin_orders"),
    path("admin-dashboard/orders/update/<str:order_number>/", views.admin_order_update, name="admin_order_update"),
    path("admin-dashboard/customers/", views.admin_customers_list, name="admin_customers"),
    path("admin-dashboard/messages/", views.admin_messages_list, name="admin_messages"),
    path("admin-dashboard/messages/read/<int:message_id>/", views.admin_message_mark_read, name="admin_message_mark_read"),
    
    # Compatibility route
    path("add-product/", views.admin_product_add, name="add_product"),
]