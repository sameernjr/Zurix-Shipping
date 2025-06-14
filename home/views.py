from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index_view(request):
    return render(request, 'home/index.html')
@login_required
def about_view(request):
    return render(request, 'home/about.html')
@login_required
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message. We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'home/contact.html', {'form': form})