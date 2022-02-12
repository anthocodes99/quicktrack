from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from rest_framework import serializers

from .validators import validate_username

class LoginSerializer(serializers.Serializer):
    # email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect username or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            # 'last_login',
            # 'email',
            'username',
            # 'is_active',
            # 'joined_at',
            'password'
        )
        read_only_fields = ('last_login', 'is_active', 'joined_at')
        extra_kwargs = {
            'password': {'required': True, 'write_only': True},
            'username': {'required': True}
        }

    @staticmethod
    def validate_email(value):
        return validate_username(value)

    def create(self, validated_data):
        return settings.AUTH_USER_MODEL.objects.create_user(
                    validated_data.pop('email'),
                    validated_data.pop('password'),
                    **validated_data
                )
