from rest_framework import serializers
from account.models import User

class UserRegistrationSerilizer(serializers.ModelSerializer):
    # We are writing this because we need confirm password field in our registration request
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validating password and confirm password while registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and confirm doesn't match")
        return attrs
    
    # Create user so that create method 
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class UserLoginSerilizer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']