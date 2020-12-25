from django.urls import path, include
from .views import (RegisterView, VerifyEmailView, LoginView,
                    LogoutView, ChangePasswordView)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/<int:pk>/', ChangePasswordView.as_view(), name='change-password')
]