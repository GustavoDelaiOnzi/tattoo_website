from rest_framework import serializers
from .models import AuthenticationUser

class AuthenticationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationUser
        fields = '__all__'


class TokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
