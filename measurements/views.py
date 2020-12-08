from rest_framework import generics
from .serializers import MeasurementDetailSerializer
from .models import Measurements
from .permissions import IsOwner
from rest_framework import permissions
# Create your views here.

class MeasurementApiView(generics.ListCreateAPIView):
    serializer_class = MeasurementDetailSerializer
    queryset = Measurements.objects.all() #gets the objects of the instance
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        '''overides the method that creates an instance of measurement and points it at the creator and thats the current login user'''
        return serializer.save(owner=self.request.user.customer) #saves with the owner

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user.customer) #this ensuures the user gets only the measurement they created

class MeasurementDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MeasurementDetailSerializer
    queryset = Measurements.objects.all() #gets the objects of the instance
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = 'id'

    def perform_create(self, serializer):
        '''overides the method that creates an instance of measurement and points it at the creator and thats the current login user'''
        return serializer.save(owner=self.request.user.customer) #saves with the owner

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user.customer) #this ensuures the user get