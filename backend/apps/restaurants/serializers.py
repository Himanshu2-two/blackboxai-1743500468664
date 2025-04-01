from rest_framework import serializers
from .models import Restaurant, MenuItem, Order, OrderItem

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'image_url', 'description']
        read_only_fields = ['id']

class MenuItemSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'description', 'restaurant', 'restaurant_name', 'image_url']
        read_only_fields = ['id', 'restaurant_name']

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_price = serializers.DecimalField(source='menu_item.price', read_only=True, max_digits=10, decimal_places=2)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'menu_item_price', 'quantity', 'price']
        read_only_fields = ['id', 'menu_item_name', 'menu_item_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total', 'created_at', 'items']
        read_only_fields = ['id', 'user', 'total', 'created_at', 'items']