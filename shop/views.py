from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Profile
from .forms import CustomUserCreationForm
from .telegram_bot import send_order_notification
from asgiref.sync import async_to_sync
from django.core.paginator import Paginator


def index(request):
    category = request.GET.get('category')
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    products = Product.objects.all().order_by("-created_at")
    if category:
        products = products.filter(category=category)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    recent_products = []
    recent_ids = request.session.get('recent_products', [])
    if not isinstance(recent_ids, list):
        recent_ids = []

    for rid in recent_ids:
        try:
            p = Product.objects.get(id=rid)
            recent_products.append(p)
        except Product.DoesNotExist:
            continue

    return render(request, 'shop/index.html', {
        'products': products,
        'selected_category': category,
        'recent_products': recent_products,
        'min_price': min_price,
        'max_price': max_price,
    })



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    recent = request.session.get('recent_products', [])
    if not isinstance(recent, list):
        recent = []

    if product.id in recent:
        recent.remove(product.id)
    recent.insert(0, product.id)
    recent = recent[:3]
    request.session['recent_products'] = recent
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
    item.save()
    return redirect('cart')

@login_required
def decrease_item(request, pk):
    item = get_object_or_404(
        CartItem,
        pk=pk,
        cart__user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(
        CartItem,
        pk=pk,
        cart__user=request.user
    )
    item.delete()
    return redirect('cart')


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = 0
    for item in items:
        item.total_price = item.product.price * item.quantity
        total += item.total_price

    return render(request, 'shop/cart.html', {
        'items': items,
        'total': total
    })


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        order_items = "\n".join([f"{item.product.name} x {item.quantity}" for item in cart.items.all()])
        message = f"Новый заказ от {request.user.username}:\n{order_items}"

        async_to_sync(send_order_notification)(message)

        cart.items.all().delete()

        return render(request, 'shop/checkout_success.html', {
            'message': "Ваш заказ в обработке. С вами свяжется наш менеджер"
        })
    return redirect('cart')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get("phone")
            Profile.objects.create(user=user, phone=phone)
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "shop/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('index')

def help_page(request):
    if request.method == "POST":
        username = request.POST.get("username", "Аноним")
        phone = request.POST.get("phone", "Не указан")
        message = f"💬 Заявка на помощь!\nПользователь: {username}\nТелефон: {phone}"
        async_to_sync(send_order_notification)(message)
        return render(request, "shop/help_sent.html", {"username": username})
    return render(request, "shop/help.html")


