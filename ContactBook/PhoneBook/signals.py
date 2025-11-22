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
from .models import Product, Basket, FeaturedProduct, TopProduct, Contact


@receiver(post_save, sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    """Очищення кешу при збереженні товару"""
    cache.delete('store_home_products')
    cache.delete('all_products_admin')
    cache.delete('featured_top_products_admin')


@receiver(post_delete, sender=Product)
def clear_product_cache_on_delete(sender, instance, **kwargs):
    """Очищення кешу та видалення товару з кошиків при видаленні товару"""
    cache.delete('store_home_products')
    cache.delete('all_products_admin')
    cache.delete('featured_top_products_admin')
    # Видаляємо товар з усіх кошиків та очищаємо кеші кошиків
    baskets = Basket.objects.filter(product_id=instance.id)
    user_ids = set(baskets.values_list('user_id', flat=True))
    baskets.delete()
    # Очищаємо кеші кошиків для всіх користувачів
    for user_id in user_ids:
        cache.delete(f'basket_{user_id}')


@receiver(post_save, sender=FeaturedProduct)
@receiver(post_delete, sender=FeaturedProduct)
def clear_cache_on_featured_change(sender, instance, **kwargs):
    """Очищення кешу при зміні головних товарів"""
    cache.delete('store_home_products')
    cache.delete('featured_top_products_admin')


@receiver(post_save, sender=TopProduct)
@receiver(post_delete, sender=TopProduct)
def clear_cache_on_top_change(sender, instance, **kwargs):
    """Очищення кешу при зміні топ товарів"""
    cache.delete('store_home_products')
    cache.delete('featured_top_products_admin')


@receiver(post_save, sender=Basket)
@receiver(post_delete, sender=Basket)
def clear_basket_cache(sender, instance, **kwargs):
    """Очищення кешу кошика при зміні"""
    if hasattr(instance, 'user_id'):
        cache.delete(f'basket_{instance.user_id}')


@receiver(post_save, sender=Contact)
@receiver(post_delete, sender=Contact)
def clear_contacts_cache(sender, instance, **kwargs):
    """Очищення кешу контактів при зміні"""
    if hasattr(instance, 'user_id'):
        cache.delete(f'user_contacts_{instance.user_id}')

