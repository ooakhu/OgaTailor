from rest_framework import generics, status, views
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, CustomerSerializer, CustomerSerializerDetail
from rest_framework.response import Response
from .models import User, Customer, Admin
from django.db import transaction
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import email_template
from django.contrib.sites.shortcuts import get_current_site
import jwt
from django.conf import settings
from django.urls import reverse # takes url name and gives us the path
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class RegisterView(generics.GenericAPIView):
    """View for registering new users"""
    serializer_class = RegisterSerializer

    @transaction.atomic()
    def post(self, request):
        '''Sends a post request to create a new user'''
        user = request.data #gets details passed from the request and assigns it to user
        full_name = request.data.get('full_name')
        serializer = RegisterSerializer(data=user) # serializes and validates the data sent in request by passing it to register serializer
        serializer.is_valid(raise_exception=True) # confirms that the data in serializer is indeed valid
        serializer.save() #creates and saves this data which is user to db
        user_data = serializer.data # user data is the data that the serializer has saved

        user = User.objects.get(email=user_data['email']) #initializes a user by fetching it from the db using the users email
        token = RefreshToken.for_user(user).access_token # generates and ties a token to the users email passed to it


        customer = {"user_id":str(user.id), #creates customer object by accessing User id
                    "full_name": full_name}

        customer_serializer = CustomerSerializer(data=customer) #serializes customer data
        customer_serializer.is_valid(raise_exception=True)
        customer_serializer.save() #creates and save customer to db
        customer_instance = Customer.objects.get(full_name=customer_serializer.data["full_name"])
        customer_data = CustomerSerializerDetail(customer_instance) #uses the customer instance to access all the users attributes

        current_site = get_current_site(request).domain #you want the user to be directed back to your site(this site) when they click the registration link
        relativeLink = reverse('verify-email') #takes the url name passed and gives us the path
        absolute = 'http://' + current_site + relativeLink +"?token=" + str(token) #this is the link that will be sent to new user to click on

        email_subject = 'Welcome To OgaTailor'
        email_body = f'''
            Hello {user.username}, Welcome to OgaTailor, we are delighted to have you on board!
            <br><br><b>Note: <i>Please click the link below to verify your account.</i> </b>
            <br><br><b> <i>{absolute}</i> </b>
            <br><br><b>Note: <i>It expires in 10 minutes.</i> </b>'''

        email_template(email_subject, user.email, email_body)
        return Response(customer_data.data, status=status.HTTP_201_CREATED)

class VerifyEmailView(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token') #get the token from the user when they hit our view
        try:
            payload = jwt.decode(token, settings.SECRET_KEY) # here we are truing to access the informattion encoded in to the link. Functionality comes with jwt
            user = User.objects.get(id=payload['user_id']) # here we extract the user from the payload
            if not user.is_verified: #check that the user is not already verified so as to reduce the db queries
                user.is_verified = True
                user.email_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'This activation link has expired. Please request for a new one.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token, request a new one.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status.HTTP_200_OK)

# class LogoutView(generics.GenericAPIView):
#     def post(self, request):
#         logout(request)
#         data = {'Success': 'Logout Successful'}
#         return Response(data=data, status=status.HTTP_200_OK)
