from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, AddressSerializer
from .models import Address

User = get_user_model()


# ---------- Helper: Token generator ----------
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# ---------- Signup ----------
class SignupView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        tokens = get_tokens_for_user(user)
        user_data = UserSerializer(user).data

        return Response({
            **tokens,
            'user': user_data,
            'redirect_url': '/admin' if (user.is_staff or user.is_superuser) else '/'
        }, status=status.HTTP_201_CREATED)


# ---------- Login ----------
class LoginView(APIView):
    def post(self, request):
        identifier = request.data.get('identifier')  # email or phone
        password = request.data.get('password')

        if not identifier or not password:
            return Response({'error': 'Please provide both identifier and password'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            if '@' in identifier:
                user = authenticate(request, email=identifier, password=password)
            else:
                user_obj = User.objects.get(contact_no=identifier)
                user = authenticate(request, email=user_obj.email, password=password)
        except User.DoesNotExist:
            user = None

        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens_for_user(user)
        user_data = UserSerializer(user).data

        return Response({
            **tokens,
            'user': user_data,
            'redirect_url': '/admin' if (user.is_staff or user.is_superuser) else '/'
        }, status=status.HTTP_200_OK)


# ---------- Address Views ----------
class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if serializer.validated_data.get("is_default"):
            Address.objects.filter(user=self.request.user).update(is_default=False)
        serializer.save(user=self.request.user)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.validated_data.get("is_default"):
            Address.objects.filter(user=self.request.user).update(is_default=False)
        serializer.save(user=self.request.user)
