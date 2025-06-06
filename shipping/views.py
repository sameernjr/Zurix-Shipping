from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import ShippingForm
from .models import Shipping, ShippingPreview

@login_required
def create_shipping(request):
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            request.session['shipping_preview'] = form.cleaned_data
            return redirect('shipping:preview')
    else:
        form = ShippingForm()
    return render(request, 'shipping/create_shipping.html', {'form': form})

@login_required
def shipping_preview(request):
    preview_data = request.session.get('shipping_preview')
    if not preview_data:
        return redirect('shipping:create_shipping')
    
    preview_data['weight'] = float(preview_data['weight'])

    preview = ShippingPreview(preview_data)
    shipping_cost = preview.calculate_shipping_cost()

    context = {
        'preview': preview,
        'shipping_cost': shipping_cost,
        'shipping_location_display': preview.get_shipping_location_display(),
        'shipping_type_display': preview.get_shipping_type_display(),
    }

    return render(request, 'shipping/shipping_preview.html', context)

@login_required
@require_http_methods(["POST"])
def confirm_shipping(request):
    preview_data = request.session.get('shipping_preview')
    if not preview_data:
        return redirect('shipping:create_shipping')
    
    shipping = Shipping(
        user = request.user,
        weight = preview_data['weight'],
        shipping_location = preview_data['shipping_location'],
        pickup_location = preview_data['pickup_location'],
        pickup_contact = preview_data['pickup_contact'],
        destination_location = preview_data['destination_location'],
        destination_contact = preview_data['destination_contact'],
        shipping_type = preview_data['shipping_type'],
        status = Shipping.StatusChoices.PENDING,  # Set initial status
    )

    shipping.save()

    if 'shipping_preview' in request.session:
        del request.session['shipping_preview']
    return redirect('shipping:shipping_detail', order_id=shipping.order_id)  # Fixed namespace

@login_required
def shipping_detail(request, order_id):
    try:
        shipping = Shipping.objects.get(order_id=order_id)
        return render(request, 'shipping/shipping_detail.html', {'shipping': shipping})
    except Shipping.DoesNotExist:
        return redirect('shipping:create_shipping')