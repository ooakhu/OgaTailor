from django.contrib.auth.models import (AbstractUser, BaseUserManager)
from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import uuid
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class UserManager(BaseUserManager):
    '''A custom manager for managing the custom user model'''

    def create_user(self, username, email, password=None, **extra_field):
        '''Creates a user. Everybody who signs up is a user'''

        if username is None:
            raise ValueError('Please provide a username')
        if email is None:
            raise ValueError('Please Provide an Email')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_field)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, username, **extra_fields):
        '''Create a superuser'''

        extra_fields.setdefault("is_admin", False)
        extra_fields.setdefault("is_superadmin", True)
        extra_fields.setdefault("email_verified", True)
        if password is None:
            raise ValueError('Please Provide a password')
        if extra_fields.get("is_superadmin") is not True:
            raise ValueError('Superadmin must have is_superadmin=True.')

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractUser):
    '''The user from which other profiles inherit'''
    id              = models.AutoField(primary_key=True)
    email           = models.EmailField(max_length=255, unique=True)
    username        = models.CharField(max_length=255)
    phone_number    = PhoneNumberField()
    is_verified     = models.BooleanField(default=False)
    email_verified  = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now=False, default=timezone.now)
    updated_at      = models.DateTimeField(auto_now=True)
    objects         = UserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    def tokens(self):

        refresh_token = RefreshToken.for_user(self) #retrives both the refresh and access token of the user
        return {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)
        }

    def __str__(self):
        return self.email

class Customer(models.Model):
    '''Customer profile'''
    id              = models.AutoField(primary_key=True)
    user_id         = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    full_name       = models.CharField(max_length=30, null=True)
    created_at      = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.full_name


class Admin(models.Model):
    '''Admin profile'''
    id              = models.AutoField(primary_key=True)
    user_id         = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    full_name       = models.CharField(max_length=255)


    def __str__(self):
        return self.full_name
