from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Restaurant, MenuItem, Order, OrderItem
from .serializers import RestaurantSerializer, MenuItemSerializer, OrderSerializer
from django.contrib.auth.models import User

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def menu_items(self, request, pk=None):
        restaurant = self.get_object()
        items = MenuItem.objects.filter(restaurant=restaurant)
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        order = self.get_object()
        menu_item = get_object_or_404(MenuItem, id=request.data.get('menu_item_id'))
        quantity = int(request.data.get('quantity', 1))
        
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            menu_item=menu_item,
            defaults={'quantity': quantity, 'price': menu_item.price}
        )
        
        if not created:
            order_item.quantity += quantity
            order_item.save()
        
        order.total = sum(item.price * item.quantity for item in order.items.all())
        order.save()
        
        return Response({'status': 'item added'}, status=status.HTTP_200_OK)