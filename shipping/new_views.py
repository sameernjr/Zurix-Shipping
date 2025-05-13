from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
                
                # Debug print to console for troubleshooting
                print(f"Proceeding to order preview. Base Price: ${order.base_price}, Total: ${order.total_price}")
                
                # Directly render the order preview template with the order object
                return render(request, 'shipping/order_preview.html', {'order': order})
            else:
                print(f"Form validation failed: {form.errors}")
                messages.error(request, "Please correct the errors in the form.")
                
        elif 'confirm_order' in request.POST:
            # Final submission - save to database
            form = ShippingForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                order.status = 'pending'  # Set initial status
                
                # Calculate prices
                order.calculate_pricing()
                
                order.save()
                messages.success(request, "Your order has been placed successfully!")
                return redirect('order_success', order_id=order.id)
            else:
                print(f"Form errors during confirmation: {form.errors}")
                messages.error(request, "There was an error processing your order.")
                
    else:
        form = ShippingForm()
    
    return render(request, 'shipping/shipping_form.html', {
        'form': form
    })

@login_required
def order_success(request, order_id):
    try:
        order = ShippingOrder.objects.get(id=order_id, user=request.user)
        return render(request, 'shipping/success.html', {
            'order': order,
            'status_display': order.get_status_display()
        })
    except ShippingOrder.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('order_history')

@login_required
def order_history(request):
    orders = ShippingOrder.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shipping/order_history.html', {
        'orders': orders
    })
