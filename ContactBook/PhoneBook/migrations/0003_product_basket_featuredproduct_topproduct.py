# Generated manually

from django.conf import settings
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PhoneBook', '0002_contact_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Назва товару')),
                ('description', models.TextField(verbose_name='Опис')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ціна')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Зображення')),
                ('is_new', models.BooleanField(default=False, verbose_name='Новий товар')),
                ('rating', models.IntegerField(default=0, verbose_name='Рейтинг')),
                ('count', models.IntegerField(default=0, verbose_name='Кількість на складі')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товари',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FeaturedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0, verbose_name='Порядок відображення')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PhoneBook.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Головний товар',
                'verbose_name_plural': 'Головні товари',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TopProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0, verbose_name='Порядок відображення')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PhoneBook.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Товар у топі',
                'verbose_name_plural': 'Товари у топі',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='Кількість')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PhoneBook.product', verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Кошик',
                'verbose_name_plural': 'Кошики',
                'unique_together': {('user', 'product')},
            },
        ),
    ]


