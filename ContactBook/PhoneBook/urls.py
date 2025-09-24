from django.urls import path

from . import views


urlpatterns = [
    path("", views.get_contacts, name="get_contacts"),
    path("add_contact/", views.add_contact, name="add_contact")
]