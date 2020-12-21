from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSerializer


class GoogleAuthView(GenericAPIView):
    serializer_class = GoogleSerializer

    def post(self, request):
        """post with auth_token
        Send an idtoken from googlr to get user information"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data['auth_token'])
        return Response(data, status=status.HTTP_200_OK)
