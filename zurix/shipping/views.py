from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ShippingForm
from .models import ShippingOrder

@login_required
def shipping_request(request):
    if request.method == 'POST':
        if 'proceed_to_order' in request.POST:
            # First submission - show order preview
            form = ShippingForm(request.POST)
            if form.is_valid():
                # Create unsaved order instance to calculate price
                order = form.save(commit=False)
                order.user = request.user
                order.calculate_pricing()
                return render(request, 'shipping/order_preview.html', {'order': order})
        elif 'confirm_order' in request.POST:
            # Final submission - save to database
            form = ShippingForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                return redirect('order_success', order_id=order.id)
    else:
        form = ShippingForm()
    
    return render(request, 'shipping/shipping_form.html', {'form': form})

@login_required
def order_success(request, order_id):
    try:
        order = ShippingOrder.objects.get(id=order_id, user=request.user)
        return render(request, 'shipping/success.html', {'order': order})
    except ShippingOrder.DoesNotExist:
        return redirect('order_history')

@login_required
def order_history(request):
    orders = ShippingOrder.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shipping/order_history.html', {'orders': orders})
