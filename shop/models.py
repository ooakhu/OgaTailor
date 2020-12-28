from django.db import models
from decimal import Decimal
from authentication.models import Customer
from django.utils import timezone


# Create your models here.


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    quantity = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    description = models.TextField(default='Product description.')

    def __str__(self):
        return self.name

    def get_cost(self):
        return self.price * self.quantity


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    product = models.CharField(max_length=30)
    # product = models.ForeignKey(Products, related_name='products', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    delivery_method = models.CharField(max_length=30, default='')
    payment_method = models.CharField(max_length=30, default='')
    owner = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=False, default=timezone.now)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.owner.email

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.product.all())


class Cart(models.Model):
    owner = models.OneToOneField(Customer, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.order.all())
