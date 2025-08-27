from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from userauth.models import CustomUser
from store.models import Product


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # We accept either email or contact_no as "username"
    username_field = "username"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['contact_no'] = user.contact_no
        token['is_staff'] = user.is_staff
        token['full_name'] = user.full_name
        return token

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        # Try email first
        try:
            user_obj = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            # Then try contact_no
            try:
                user_obj = CustomUser.objects.get(contact_no=username)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid login credentials")

        # Authenticate user with password check
        user = authenticate(username=user_obj.email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid login credentials")

        # Generate token
        data = super().validate({"username": user.email, "password": password})
        data['email'] = user.email
        data['contact_no'] = user.contact_no
        data['is_staff'] = user.is_staff
        data['full_name'] = user.full_name
        return data


# ✅ Product serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


# ✅ Registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'contact_no', 'password', 'full_name', 'is_staff')
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data.get('email'),
            contact_no=validated_data.get('contact_no'),
            password=validated_data['password'],
            full_name=validated_data['full_name']
        )
        return user


# ✅ Serializer for user details
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'contact_no', 'full_name', 'is_staff', 'date_joined']
