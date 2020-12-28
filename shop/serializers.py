from shop.models import Products, Order, Cart
from rest_framework import serializers
from authentication.models import Customer


class ProductsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)

    class Meta:
        model = Products
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['product', 'quantity', 'delivery_method', 'payment_method']

    def create(self, validated_data):
        order= Order.objects.create(**validated_data)
        return order

    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.delivery_method = validated_data.get('delivery_method', instance.delivery_method)
        instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.save()
        return instance


class CartSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Cart
        fields = '__all__'
