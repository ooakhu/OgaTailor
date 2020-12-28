from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from authentication.models import Customer
from django.http import Http404
from .models import Products, Order, Cart
from .serializer import OrdersSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status


# Create your views here.

class OrdersView(APIView):
    serializer_class = OrdersSerializer

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrdersSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        order = request.data
        serializer = OrdersSerializer(data=order)
        if serializer.is_valid(raise_exception=True):
            order_saved = serializer.save()
            return Response({'message': 'Success, your order has been created'}, status=status.HTTP_201_CREATED)
        return Response({"message": "Order could not be created this time. Please contact us."},
                        status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    serializer_class = OrdersSerializer

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = OrdersSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = self.get_object(pk)
        serializer = OrdersSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = get_object_or_404(Order.objects.all(), pk=pk)
        order.delete()
        return Response({"message": "your order has been deleted"}, status=status.HTTP_204_NO_CONTENT)
