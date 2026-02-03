from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('decrease/<int:pk>/', views.decrease_item, name='decrease_item'),
    path('checkout/', views.checkout, name='checkout'),

    path('login/', auth_views.LoginView.as_view(
        template_name='shop/login.html',
        redirect_authenticated_user=True
    ), name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('register/', views.register, name='register'),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('help/', views.help_page, name='help_page'),
]
