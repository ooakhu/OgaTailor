from django.urls import path
from .views import (RegisterView, VerifyEmailView, LoginView,
                    LogoutView, PasswordTokenCheckView, RequestPasswordEmailView, SetNewPasswordAPIView, SendSmsView, VerifyOtpView)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('request-password-reset', RequestPasswordEmailView.as_view(), name='request-password-reset'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckView.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('send-sms/', SendSmsView.as_view(), name='send-sms'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp')
]