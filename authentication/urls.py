from django.urls import path, include
from .views import RegisterView, VerifyEmailView, LoginView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    # path('logout/', LogoutView.as_view(), name='logout'),
]