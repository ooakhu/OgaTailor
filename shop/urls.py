from django.urls import path

from .views import OrdersView, OrderDetail

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='orders'),
    path('orders/<int:pk>', OrderDetail.as_view(), name='orders'),
]