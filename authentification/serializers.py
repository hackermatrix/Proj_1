from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Clients
from .models import Websites
# ...
class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = Clients
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = Clients
        fields = ('username',)

class WebsitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Websites
        fields = ('domain_name', 'subdomains', 'metadata')