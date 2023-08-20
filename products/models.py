from django.db import models

from users.models import User


# models = table
class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products_images")
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ["id"]

    def __str__(self):
        return f"Продукт: {self.name} | Категория: {self.category}"


class BasketQuerySet(models.QuerySet):
    """
    This class extends .objects manager. total_sum() and total_quantity() methods are
    available in templates using point attribute:
    # {{ baskets.total_sum }}
    # {{ baskets.total_quantity }}
    """

    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateField(auto_now_add=True)

    objects = (
        BasketQuerySet.as_manager()
    )  # updates objects manager by adding some new methods from class

    def __str__(self):
        return f"Корзина для {self.user.username} | Продукт: {self.product.name}"

    def sum(self):
        return self.product.price * self.quantity
