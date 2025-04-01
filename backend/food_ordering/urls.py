from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.accounts.views import admin_dashboard
from apps.orders.views import manage_orders

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/dashboard/', user_passes_test(lambda u: u.is_staff)(admin_dashboard), name='admin-dashboard'),
    path('admin/orders/', user_passes_test(lambda u: u.is_staff)(manage_orders), name='manage-orders'),
    path('api/', include('api.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('restaurants/', include('apps.restaurants.urls')),
    path('orders/', include('apps.orders.urls')),
]
