from rest_framework import serializers
from . import google
from .register import register_social_user
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class GoogleSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)

        try:
            user_data['sub']
        except:
            raise serializers.ValidationError('This token is invalid, please login again')

        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('oops, who are you')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)
