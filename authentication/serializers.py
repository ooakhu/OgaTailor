from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Customer
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=7, write_only=True) #you initialize this here because the user model and others do not have a password field
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

class CustomerSerializer(serializers.ModelSerializer): #serialize customer detail
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerSerializerDetail(serializers.ModelSerializer): #serializes customers detail and give access to user data using depth
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
    password = serializers.CharField(max_length=65, min_length=7, write_only=True) #write only so we dont send it back to the user
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=608, min_length=7, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password) #authenticates the user with the email and password passed
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

class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'new_password2']

        def validate (self, attrs):
            if attrs['new_password'] != attrs['new_password2']:
                raise serializers.ValidationError({"new_password": "Passwords don't match"})
            print(attrs['new_password'],"new password",
            '---------------------------------------------------------')

            return attrs

        def validate_old_password(self, value):
g

            if not user.check_password(value):
                raise serializers.ValidationError({"old_password": "Old Password is not correct"})
            print(user.id,"new user",
            '---------------------------------------------------------')
            return value

        def update(self, instance, validated_data):
            instance.set_password(validated_data['new_password'])
            instance.save()
            print(validated_data,"validated data", instance,
            '---------------------------------------------------------')

            return instance

class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

