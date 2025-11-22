from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page, never_cache
from django.db.models import Q
from django.conf import settings

from .models import Contact, Product, Basket, FeaturedProduct, TopProduct
from .forms import ContactForm, ProductForm

# Create your views here.

@login_required(login_url="/sign_in")
def add_contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            cache.delete(f'user_contacts_{request.user.id}')
            messages.add_message(request=request, level=messages.SUCCESS, message="Контакт додан")
            return redirect("get_contacts")
    
    return render(request=request, template_name="add_contact.html", context=dict(form=form))

@login_required(login_url="/sign_in")
def get_contacts(request):
    """Отримання контактів користувача з кешуванням"""
    cache_key = f'user_contacts_{request.user.id}'
    contacts = cache.get(cache_key)
    
    if contacts is None:
        contacts = list(Contact.objects.filter(user=request.user).all())
        cache.set(cache_key, contacts, getattr(settings, 'CACHE_TIMEOUT_MEDIUM', 300))
    
    return render(request=request, template_name="contacts.html", context=dict(contacts=contacts))


@login_required
def delete_contact(request, id):
    contact = Contact.objects.filter(pk=id, user=request.user).first()
    contact_name = str(contact)
    contact.delete()
    # Очищення кешу контактів користувача
    cache.delete(f'user_contacts_{request.user.id}')
    messages.add_message(request=request, message=f"Контакт '{contact_name}' видалено", level=messages.SUCCESS)
    return redirect("get_contacts")


@login_required
def edit_contact(request, id):
    contact = Contact.objects.filter(pk=id, user=request.user).first()
    form = ContactForm(data=request.POST or None, files=request.FILES or None, instance=contact)
    if request.POST and form.changed_data:
        form.save()
        # Очищення кешу контактів користувача
        cache.delete(f'user_contacts_{request.user.id}')
        messages.add_message(request=request, message="Дані оновлені", level=messages.SUCCESS)
        return redirect("get_contacts")
    
    return render(request=request, template_name="edit.html", context=dict(form=form))


@login_required
def filter_contacts(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    phone_number = request.POST.get("phone_number")
    email = request.POST.get("email")
    address = request.POST.get("address")
    
    contacts = (Contact.objects
                .filter(first_name__icontains=first_name)
                .filter(last_name__icontains=last_name)
                .filter(phone_number__icontains=phone_number)
                .filter(email__icontains=email)
                .filter(address__icontains=address)
                .filter(user=request.user)
                .all()
    )
    return render(request=request, template_name="contacts.html", context=dict(contacts=contacts))


# ========== STORE VIEWS ==========

def is_admin(user):
    """Перевірка чи користувач адміністратор"""
    return user.is_authenticated and user.is_staff


def store_home(request):
    """Головна сторінка магазину з популярними та головними товарами"""
    cache_key = 'store_home_products'
    products_data = cache.get(cache_key)
    
    if not products_data:
        featured_products = list(Product.objects.filter(
            id__in=FeaturedProduct.objects.values_list('product_id', flat=True)
        ).order_by('featuredproduct__order')[:10])
        
        top_products = list(Product.objects.filter(
            id__in=TopProduct.objects.values_list('product_id', flat=True)
        ).order_by('topproduct__order')[:10])
        
        products_data = {
            'featured_products': featured_products,
            'top_products': top_products,
        }
        cache.set(cache_key, products_data, getattr(settings, 'CACHE_TIMEOUT_LONG', 900))  # Кешування на 15 хвилин
    else:
        featured_products = products_data['featured_products']
        top_products = products_data['top_products']
    
    # Встановлення cookie для відстеження відвідувань
    visit_count = request.COOKIES.get('visit_count', '0')
    try:
        visit_count = int(visit_count) + 1
    except ValueError:
        visit_count = 1
    
    response = render(request, 'store/home.html', {
        'featured_products': featured_products,
        'top_products': top_products,
        'visit_count': visit_count,
    })
    response.set_cookie('visit_count', str(visit_count), max_age=60*60*24*365)  # 1 рік
    return response


@user_passes_test(is_admin, login_url='/users/sign_in/')
def add_product(request):
    """Додавання нового товару (тільки для адмінів)"""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Очищення кешу
            cache.delete('store_home_products')
            cache.delete('all_products_admin')
            messages.success(request, "Товар успішно додано!")
            return redirect("store_home")
    else:
        form = ProductForm()
    
    return render(request, 'store/add_product.html', {'form': form})


@user_passes_test(is_admin, login_url='/users/sign_in/')
def manage_products(request):
    """Управління товарами (тільки для адмінів)"""
    cache_key = 'all_products_admin'
    products = cache.get(cache_key)
    
    if products is None:
        products = list(Product.objects.all().order_by('-created_at'))
        cache.set(cache_key, products, getattr(settings, 'CACHE_TIMEOUT_SHORT', 60))  # Коротке кешування для адмін-панелі
    
    return render(request, 'store/manage_products.html', {'products': products})


@user_passes_test(is_admin, login_url='/users/sign_in/')
def delete_product(request, product_id):
    """Видалення товару (тільки для адмінів)"""
    if not request.user.is_staff:
        messages.error(request, "Доступ заборонено!")
        return redirect("store_home")
    
    product = get_object_or_404(Product, id=product_id)
    product_name = product.name
    
    # Видалення товару (сигнал автоматично видалить з кошиків)
    product.delete()
    
    # Очищення кешу
    cache.delete('store_home_products')
    cache.delete('all_products_admin')
    
    messages.success(request, f"Товар '{product_name}' успішно видалено!")
    return redirect("manage_products")


@user_passes_test(is_admin, login_url='/users/sign_in/')
def manage_featured_top(request):
    """Управління головними та топ товарами (тільки для адмінів)"""
    cache_key = 'featured_top_products_admin'
    products_data = cache.get(cache_key)
    
    if products_data is None:
        featured_products = list(FeaturedProduct.objects.select_related('product').all())
        top_products = list(TopProduct.objects.select_related('product').all())
        products_data = {
            'featured_products': featured_products,
            'top_products': top_products,
        }
        cache.set(cache_key, products_data, getattr(settings, 'CACHE_TIMEOUT_SHORT', 60))
    else:
        featured_products = products_data['featured_products']
        top_products = products_data['top_products']
    
    return render(request, 'store/manage_featured_top.html', {
        'featured_products': featured_products,
        'top_products': top_products,
    })


@login_required
def add_to_basket(request, product_id):
    """Додавання товару до кошика"""
    product = get_object_or_404(Product, id=product_id)
    
    # Перевірка наявності товару на складі
    if product.count <= 0:
        messages.error(request, "Товар відсутній на складі!")
        return redirect("store_home")
    
    # Перевірка чи товар вже є в кошику
    basket_item, created = Basket.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        # Якщо товар вже є, збільшуємо кількість
        if basket_item.quantity < product.count:
            basket_item.quantity += 1
            basket_item.save()
            messages.success(request, f"Кількість товару '{product.name}' збільшено!")
        else:
            messages.warning(request, f"Максимальна кількість товару '{product.name}' на складі!")
    else:
        messages.success(request, f"Товар '{product.name}' додано до кошика!")
    
    # Збереження в сесії
    if 'basket_items' not in request.session:
        request.session['basket_items'] = []
    request.session['basket_items'].append(product_id)
    request.session.modified = True
    
    # Очищення кешу кошика
    cache.delete(f'basket_{request.user.id}')
    
    return redirect("store_home")


@login_required
def basket_view(request):
    """Перегляд кошика користувача з кешуванням"""
    cache_key = f'basket_{request.user.id}'
    basket_data = cache.get(cache_key)
    
    if basket_data is None:
        basket_items = Basket.objects.filter(user=request.user).select_related('product')
        # Обчислюємо суму для кожного товару та загальну суму
        items_with_total = []
        total_price = 0
        for item in basket_items:
            item_total = float(item.product.price) * item.quantity
            items_with_total.append({
                'item': item,
                'item_total': item_total,
            })
            total_price += item_total
        
        basket_data = {
            'basket_items': items_with_total,
            'total_price': total_price,
        }
        cache.set(cache_key, basket_data, getattr(settings, 'CACHE_TIMEOUT_SHORT', 60))  # Коротке кешування для кошика
    else:
        items_with_total = basket_data['basket_items']
        total_price = basket_data['total_price']
    
    return render(request, 'store/basket.html', {
        'basket_items': items_with_total,
        'total_price': total_price,
    })


@login_required
def remove_from_basket(request, basket_id):
    """Видалення товару з кошика"""
    basket_item = get_object_or_404(Basket, id=basket_id, user=request.user)
    basket_item.delete()
    # Очищення кешу кошика
    cache.delete(f'basket_{request.user.id}')
    messages.success(request, "Товар видалено з кошика!")
    return redirect("basket_view")