from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import Contact

def contact(request):
    form = ContactForm()
    return render(request, 'contact/contact.html', {'form':form})

def send_contact_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                user = request.user
                title = form.cleaned_data['title']
                message = form.cleaned_data['message']
                new_contact = Contact(user=user, title=title, message=message)
                new_contact.save()

                message_content = mark_safe(f'Thank you for your feedback!')
                messages.success(request, message_content)
            else:
                message_content = mark_safe('Please log in to your account before sending a form')
                messages.warning(request, message_content)
                return redirect('login')
    else:
        form = ContactForm()
    
    return render(request, 'contact/contact.html', {'form': form})