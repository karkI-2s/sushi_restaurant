from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from .models import SushiItem, Category, Hotel, Order
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# ----------------------------
# HOME
# ----------------------------
def index(request):
    latest_items = SushiItem.objects.filter(available=True)[:6]
    return render(request, 'shop/index.html', {
        'latest_items': latest_items,
    })


# ----------------------------
# HOTEL
# ----------------------------
def hotel_view(request):
    hotels = Hotel.objects.all().order_by('-created_at')
    hotel = hotels.first()

    return render(request, 'shop/hotel.html', {
        'hotel': hotel,
        'hotels': hotels,
        'hotel_count': hotels.count(),
    })


# ----------------------------
# ABOUT
# ----------------------------
def about(request):
    return render(request, 'shop/about.html')


# ----------------------------
# CONTACT
# ----------------------------
def contact(request):
    return render(request, 'shop/contact.html')


# ----------------------------
# MENU
# ----------------------------
def menu_view(request):
    categories = Category.objects.all()
    products = SushiItem.objects.filter(available=True)

    return render(request, 'shop/menu.html', {
        'products': products,
        'categories': categories
    })


# ----------------------------
# CATEGORY ITEMS
# ----------------------------
def category_items(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    items = SushiItem.objects.filter(category=category, available=True)

    return render(request, 'shop/category_items.html', {
        'category': category,
        'items': items
    })


# ----------------------------
# SIDE DISHES
# ----------------------------
def side_dishes(request):
    category = get_object_or_404(Category, name="Side Dishes")
    items = SushiItem.objects.filter(category=category, available=True)
    return render(request, 'shop/side_dishes.html', {
        'items': items
    })


# ----------------------------
# ADD TO CART
# ----------------------------
def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart_view')


# ----------------------------
# REMOVE FROM CART
# ----------------------------
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        del cart[str(item_id)]
    request.session['cart'] = cart
    return redirect('cart_view')


# ----------------------------
# UPDATE CART
# ----------------------------
def update_cart(request, item_id, action):
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        if action == 'increase':
            cart[str(item_id)] += 1
        elif action == 'decrease':
            cart[str(item_id)] -= 1
            if cart[str(item_id)] <= 0:
                del cart[str(item_id)]

    request.session['cart'] = cart
    return redirect('cart_view')


# ----------------------------
# CART VIEW
# ----------------------------
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for item_id, quantity in cart.items():
        item = get_object_or_404(SushiItem, id=item_id)
        subtotal = item.price * quantity
        total += subtotal

        cart_items.append({
            'item': item,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# ----------------------------
# CHECKOUT
# ----------------------------
def checkout_view(request):

    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_view')

    total_amount = 0
    for item_id, quantity in cart.items():
        item = get_object_or_404(SushiItem, id=item_id)
        total_amount += item.price * quantity

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        delivery_area = request.POST.get("delivery_area")
        payment_method = request.POST.get("payment_method")

        # DELIVERY FEE
        delivery_fee = 0
        if delivery_area == "tokyo":
            delivery_fee = 500
        elif delivery_area == "chiba":
            delivery_fee = 800
        elif delivery_area == "kanagawa":
            delivery_fee = 1000

        final_total = total_amount + delivery_fee

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            phone=phone,
            address=address,
            delivery_area=delivery_area,
            payment_method=payment_method,
            total_amount=int(final_total)
        )

        # STRIPE CARD
        if payment_method == "card":
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'jpy',
                        'product_data': {
                            'name': f'UB Sushi Order #{order.id}'
                        },
                        'unit_amount': int(final_total),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/checkout/'),
            )
            return redirect(session.url)

        elif payment_method == "paypay":
            request.session.pop('cart', None)
            return redirect('payment_success')

        elif payment_method == "cod":
            request.session.pop('cart', None)
            return redirect('payment_success')

    return render(request, 'shop/checkout.html', {
        'total_amount': total_amount
    })


# ----------------------------
# PAYMENT SUCCESS
# ----------------------------
def payment_success(request):
    request.session.pop('cart', None)
    return render(request, 'shop/success.html')


# ----------------------------
# REGISTER
# ----------------------------
def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Register successful!")
            return redirect('index')

    return render(request, 'shop/register.html', {'form': form})


# ----------------------------
# NEWS DATA
# ----------------------------
news_data = {
    1: {
        "title": "Grand Opening Celebration",
        "content": "Join us for the grand opening of UB Sushi Restaurant!"
    },
    2: {
        "title": "New Seasonal Sushi Menu",
        "content": "Enjoy our fresh seasonal sushi crafted by expert chefs."
    },
    3: {
        "title": "Private Room Reservations",
        "content": "Private rooms now available for family gatherings."
    }
}


# ----------------------------
# NEWS DETAIL
# ----------------------------
def news_detail(request, id):
    news = news_data.get(id)
    return render(request, 'shop/news_detail.html', {
        'news': news
    })


# ======================================================
# HOTEL AMENITIES PAGES
# ======================================================

def wifi_info(request):
    return render(request, 'amenities/wifi_info.html')

def breakfast(request):
    return render(request, 'amenities/breakfast.html')

def swimming_pool(request):
    return render(request, 'amenities/swimming_pool.html')

def parking(request):
    return render(request, 'amenities/parking.html')

def air_conditioning(request):
    return render(request, 'amenities/air_conditioning.html')

def fitness_center(request):
    return render(request, 'amenities/fitness_center.html')

def reception(request):
    return render(request, 'amenities/reception.html')

def airport_shuttle(request):
    return render(request, 'amenities/airport_shuttle.html')

def bar(request):
    return render(request, 'amenities/bar.html')

def spa(request):
    return render(request, 'amenities/spa.html')

def home(request):
    return render(request, 'index.html')

def opening_event(request):
    return render(request, 'opening_event.html')


def seasonal_menu(request):
    return render(request, 'seasonal_menu.html')


def private_room(request):
    return render(request, 'private_room.html')

def date_page(request):
    return render(request, 'shop/date.html')

def casual_page(request):
    return render(request, 'shop/casual.html')

def business_page(request):
    return render(request, 'shop/business.html')

def group_page(request):
    return render(request, 'shop/group.html')