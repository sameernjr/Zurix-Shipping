from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ShippingOrder
from .forms import ShippingForm
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.conf import pdfkit


# Create your views here.
@login_required
def shipping_form(request):
    form = ShippingForm(request.POST)
    if form.is_valid():
        order = form.save(commit=False)
        order.user = request.user
        order.cost = calculate_shipping_cost(order.weight)
        order.save()
        return redirect('generate_receipt', order_id=order.id)
    else:
        form = ShippingForm()
    return render(request, 'shipping/order_form.html', {'form': form})

@login_required
def generate_receipt(request, order_id):
    order = ShippingOrder.objects.get(id=order_id)
    html = render_to_string('shipping/receipt.html', {'order': order})
    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type = 'application/pdf')
    response['Content-Disposition'] = f'attachment; filename=receipt_{order.id}.pdf'
    return response

@login_required
def user_history(request):
    orders = ShippingOrder.objects.filter(user=request.user)
    return render(request, 'shipping/user_history.html', {'orders': orders})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home') #Redirect non-admin users
    orders = ShippingOrder.objects.all()
    return render(request, 'shipping/admin_dashboard.html', {'orders': orders})

def calculate_shipping_cost(weight):
    #Example: $5 per Kg
    return weight * 5