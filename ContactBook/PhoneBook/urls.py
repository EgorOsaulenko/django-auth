from django.urls import path
from . import views

urlpatterns = [
    # Contact URLs
    path('contacts/', views.get_contacts, name='get_contacts'),
    path('contacts/add/', views.add_contact, name='add_contact'),
    path('contacts/delete/<int:id>/', views.delete_contact, name='delete_contact'),
    path('contacts/edit/<int:id>/', views.edit_contact, name='edit_contact'),
    path('contacts/filter/', views.filter_contacts, name='filter_contacts'),
    
    # Store URLs
    path('', views.store_home, name='store_home'),
    path('store/add-product/', views.add_product, name='add_product'),
    path('store/manage-products/', views.manage_products, name='manage_products'),
    path('store/delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('store/manage-featured-top/', views.manage_featured_top, name='manage_featured_top'),
    path('store/basket/', views.basket_view, name='basket_view'),
    path('store/add-to-basket/<int:product_id>/', views.add_to_basket, name='add_to_basket'),
    path('store/remove-from-basket/<int:basket_id>/', views.remove_from_basket, name='remove_from_basket'),
]