from django.db import models

# Create your models here.

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=40, null=True, default=None)
    address = models.TextField(null=True, default=None)
    profile_picture = models.ImageField(null=True, blank=True, upload_to=".")
    user = models.ForeignKey("UserManager.MySuperUser", on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва товару")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(upload_to="products/", null=True, blank=True, verbose_name="Зображення")
    is_new = models.BooleanField(default=False, verbose_name="Новий товар")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")
    count = models.IntegerField(default=0, verbose_name="Кількість на складі")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class FeaturedProduct(models.Model):
    """Модель для головних товарів"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    order = models.IntegerField(default=0, verbose_name="Порядок відображення")
    
    class Meta:
        verbose_name = "Головний товар"
        verbose_name_plural = "Головні товари"
        ordering = ['order']
    
    def __str__(self):
        return f"Головний: {self.product.name}"


class TopProduct(models.Model):
    """Модель для товарів у топі"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    order = models.IntegerField(default=0, verbose_name="Порядок відображення")
    
    class Meta:
        verbose_name = "Товар у топі"
        verbose_name_plural = "Товари у топі"
        ordering = ['order']
    
    def __str__(self):
        return f"Топ: {self.product.name}"


class Basket(models.Model):
    """Кошик користувача"""
    user = models.ForeignKey("UserManager.MySuperUser", on_delete=models.CASCADE, verbose_name="Користувач")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.IntegerField(default=1, verbose_name="Кількість")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Кошик"
        verbose_name_plural = "Кошики"
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} x{self.quantity}"