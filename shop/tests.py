from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem, Profile
from .forms import CustomUserCreationForm


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Тестовый робот",
            description="Описание робота",
            price=199.99
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Тестовый робот")

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = Profile.objects.create(user=self.user, phone="+375291234567")

    def test_profile_str(self):
        self.assertEqual(str(self.profile), "testuser Profile")

class CustomUserCreationFormTest(TestCase):
    def test_valid_phone(self):
        form_data = {
            "username": "newuser",
            "phone": "+375291234567",
            "password1": "StrongPass123",
            "password2": "StrongPass123"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_phone(self):
        form_data = {
            "username": "newuser",
            "phone": "abc123",
            "password1": "StrongPass123",
            "password2": "StrongPass123"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)


class ShopViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.product1 = Product.objects.create(name="Робот1", description="desc", price=100)
        self.product2 = Product.objects.create(name="Робот2", description="desc", price=200)

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

    def test_product_detail_view(self):
        response = self.client.get(reverse("product_detail", args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)

    def test_add_to_cart_authenticated(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("add_to_cart", args=[self.product1.id]))
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.cartitem_set.count(), 1)
        self.assertRedirects(response, reverse("cart"))

    def test_cart_view_authenticated(self):
        self.client.login(username="testuser", password="12345")
        Cart.objects.create(user=self.user)
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)

    def test_checkout_clears_cart(self):
        self.client.login(username="testuser", password="12345")
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product1, quantity=2)
        response = self.client.post(reverse("checkout"))
        self.assertEqual(cart.cartitem_set.count(), 0)
        self.assertContains(response, "Ваш заказ в обработке")

    def test_category_filter(self):
        response = self.client.get(reverse("index") + "?category=industrial")
        self.assertEqual(response.status_code, 200)

    def test_recent_products_in_session(self):
        session = self.client.session
        session['recent_product_id'] = [self.product1.id]
        session.save()
        response = self.client.get(reverse("index"))
        self.assertContains(response, self.product1.name)