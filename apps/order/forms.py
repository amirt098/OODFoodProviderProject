# serializers.py
from rest_framework import serializers
from apps.order.models import Order, OrderItem, Review
from apps.order.data_classes import OrderInfo, OrderItemInfo

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'price', 'quantity']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'rating', 'message', 'driver_rating']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['uid', 'user', 'provider', 'created', 'state', 'footnote', 'order_items', 'reviews']
