from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # ----------------------------
    # Main Pages
    # ----------------------------
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu_view, name='menu_view'),
    path('contact/', views.contact, name='contact'),

    # ----------------------------
    # Category Filter
    # ----------------------------
    path('category/<int:category_id>/', views.category_items, name='category_items'),

    # ----------------------------
    # Cart System
    # ----------------------------
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/<str:action>/', views.update_cart, name='update_cart'),

    # ----------------------------
    # Checkout & Payment
    # ----------------------------
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/', views.payment_success, name='payment_success'),
    # ----------------------------
    # Authentication
    # ----------------------------
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    # ----------------------------
    # Side Dishes
    # ----------------------------
    path('side-dishes/', views.side_dishes, name='side_dishes'),
    path('register/', views.register, name='register'),
    path('news/<int:id>/', views.news_detail, name='news_detail'),
    path('hotel/', views.hotel_view, name='hotel'),
        # ===== AMENITIES =====
    path('wifi-info/', views.wifi_info, name='wifi_info'),
    path('breakfast/', views.breakfast, name='breakfast'),
    path('swimming-pool/', views.swimming_pool, name='swimming_pool'),
    path('parking/', views.parking, name='parking'),
    path('air-conditioning/', views.air_conditioning, name='air_conditioning'),
    path('fitness-center/', views.fitness_center, name='fitness_center'),
    path('reception/', views.reception, name='reception'),
    path('airport-shuttle/', views.airport_shuttle, name='airport_shuttle'),
    path('bar/', views.bar, name='bar'),
    path('spa/', views.spa, name='spa'),
    
    path('grand-opening/', views.opening_event, name='opening_event'),
    path('seasonal-menu/', views.seasonal_menu, name='seasonal_menu'),
    path('private-room/', views.private_room, name='private_room'),
    path('date/', views.date_page, name='date'),
    path('casual/', views.casual_page, name='casual'),
    path('business/', views.business_page, name='business'),
    path('group/', views.group_page, name='group'),
]

