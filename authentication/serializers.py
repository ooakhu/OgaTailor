from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Customer
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=7,
                                     write_only=True)  # you initialize this here because the user model and others do not have a password field

    class Meta:
        model = get_user_model()
        fields = ['password', 'email', 'username', 'phone_number']

    def validate(self, attrs):
        '''Validates the data coming through the request'''
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('Username must be Alpha Numeric')
        return attrs

    def create(self, validated_data):
        '''Create the user using the validated data'''
        return User.objects.create_user(**validated_data)


class CustomerSerializer(serializers.ModelSerializer):  # serialize customer detail
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerSerializerDetail(
    serializers.ModelSerializer):  # serializes customers detail and give access to user data using depth
    class Meta:
        model = Customer
        fields = '__all__'
        depth = 1


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=700)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=65, min_length=7,
                                     write_only=True)  # write only so we dont send it back to the user
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=608, min_length=7, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email,
                                 password=password)  # authenticates the user with the email and password passed
        if not user:
            raise AuthenticationFailed('Could not find username or password.')
        if not user.is_active:
            raise AuthenticationFailed('Your account has been deactivated. Please contact an admin.')
        if not user.is_verified:
            raise AuthenticationFailed('Please verify your email first.')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }


class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=5)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
