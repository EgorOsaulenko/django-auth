"""
Сигнали для додатку PhoneBook

Важливість сесій:
1. Збереження стану кошика між запитами
2. Відстеження активності користувача
3. Збереження тимчасових даних (наприклад, товари в кошику до авторизації)
4. Персоналізація досвіду користувача

Реальне використання сесій в цьому застосунку:
- Збереження товарів у кошику навіть якщо користувач не авторизований
- Відстеження переглянутих товарів для рекомендацій
- Збереження фільтрів пошуку між сторінками
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product, Basket, FeaturedProduct, TopProduct


@receiver(post_save, sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    """Очищення кешу при збереженні товару"""
    cache.delete('store_home_products')


@receiver(post_delete, sender=Product)
def clear_product_cache_on_delete(sender, instance, **kwargs):
    """Очищення кешу та видалення товару з кошиків при видаленні товару"""
    cache.delete('store_home_products')
    # Видаляємо товар з усіх кошиків
    Basket.objects.filter(product_id=instance.id).delete()


@receiver(post_save, sender=FeaturedProduct)
@receiver(post_delete, sender=FeaturedProduct)
def clear_cache_on_featured_change(sender, instance, **kwargs):
    """Очищення кешу при зміні головних товарів"""
    cache.delete('store_home_products')


@receiver(post_save, sender=TopProduct)
@receiver(post_delete, sender=TopProduct)
def clear_cache_on_top_change(sender, instance, **kwargs):
    """Очищення кешу при зміні топ товарів"""
    cache.delete('store_home_products')

