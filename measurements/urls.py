from django.urls import path, include
from .views import MeasurementApiView, MeasurementDetailApiView

urlpatterns = [
    path('', MeasurementApiView.as_view(), name='measurements'),
    path('<int:id>', MeasurementDetailApiView.as_view(), name='measurement'),
]