from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('industrial', 'Промышленный робот'),
        ('home', 'Домашний робот'),
        ('security', 'Охранный робот'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name='Категория'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.CharField("Страна производителя",
                               max_length=50, blank=True, null=True)
    lifespan = models.CharField("Срок экспуатации",
                                max_length=10, blank=True, null=True)
    warranty = models.CharField("Срок гарантии",
                                max_length=10, blank=True, null=True)
    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField("Номер телефона", max_length=13, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"