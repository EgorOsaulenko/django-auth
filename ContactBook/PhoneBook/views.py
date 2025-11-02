from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Contact
from .forms import ContactForm

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
            messages.add_message(request=request, level=messages.SUCCESS, message="Контакт додан")
            return redirect("get_contacts")
    
    return render(request=request, template_name="add_contact.html", context=dict(form=form))

@login_required(login_url="/sign_in")
def get_contacts(request):
    contacts = Contact.objects.filter(user=request.user).all()
    return render(request=request, template_name="contacts.html", context=dict(contacts=contacts))


@login_required
def delete_contact(request, id):
    contact = Contact.objects.filter(pk=id, user=request.user).first()
    contact.delete()
    messages.add_message(request=request, message=f"Контакт '{contact}' видалено", level=messages.SUCCESS)
    return redirect("get_contacts")


@login_required
def edit_contact(request, id):
    contact = Contact.objects.filter(pk=id, user=request.user).first()
    form = ContactForm(data=request.POST or None, files=request.FILES or None, instance=contact)
    if request.POST and form.changed_data:
        form.save()
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