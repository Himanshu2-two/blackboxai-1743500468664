from django.urls import path
from .views import manage_orders

urlpatterns = [
    path('manage/', manage_orders, name='manage-orders'),
]