from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from apps.restaurants.models import Restaurant
from apps.orders.models import Order

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    if request.method == 'POST':
        try:
            Restaurant.objects.create(
                name=request.POST.get('name'),
                address=request.POST.get('address'),
                description=request.POST.get('description'),
                image_url=request.POST.get('image_url') or 'https://images.pexels.com/photos/262978/pexels-photo-262978.jpeg'
            )
            messages.success(request, 'Restaurant added successfully!')
            return redirect('admin-dashboard')
        except Exception as e:
            messages.error(request, f'Error adding restaurant: {str(e)}')

    # Calculate statistics
    restaurants_count = Restaurant.objects.count()
    active_orders_count = Order.objects.exclude(
        status__in=['delivered', 'cancelled']
    ).count()
    
    # Calculate today's revenue
    today = timezone.now().date()
    todays_orders = Order.objects.filter(
        created_at__date=today,
        status='delivered'
    )
    todays_revenue = sum(order.total for order in todays_orders)
    
    # Get recent orders
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    return render(request, 'admin_dashboard.html', {
        'restaurants_count': restaurants_count,
        'active_orders_count': active_orders_count,
        'todays_revenue': todays_revenue,
        'recent_orders': recent_orders
    })
