# /home/siisi/praevia_gemini/praevia_api/auth_views.py

from rest_framework import viewsets, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate, login, logout
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


# --- User Serializers ---
class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'name', 'username', 'email', 'role',
            'password', 'confirm_password',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        raw_password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(raw_password)  # ✅ Proper Django password hashing
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop('confirm_password', None)
        if 'password' in validated_data:
            raw_password = validated_data.pop('password')
            instance.set_password(raw_password)  # ✅ Proper password update
        return super().update(instance, validated_data)

# --- User Views ---
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    #queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=user.id)


# --- Login Serializers ---
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# --- Login View ---
class LoginView(APIView):
    permission_classes = [AllowAny]
    renderer_classes   = [BrowsableAPIRenderer, JSONRenderer]
    serializer_class   = LoginSerializer

    def get(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            return Response({'serializer': self.serializer_class()})
        return Response({})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            print(f"DEBUG: Login serializer validation failed: {serializer.errors}")
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        print(f"DEBUG: Attempting login for email: {email}")
        print(f"DEBUG: Password received (first 5 chars): {password[:5]}...")

        # ✅ FIXED: Use 'email' instead of 'username'
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # 1) set the session cookie for browsable UI
            login(request, user)
            print(f"DEBUG: User '{user.email}' authenticated successfully.")
            # 2) return (or create) your token
            token, created = Token.objects.get_or_create(user=user)
            print(f"DEBUG: Token for '{user.email}': {token.key} (Created: {created})")

            return Response({
                'success': True,
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'username': user.username,
                'role': user.role,
            }, status=status.HTTP_200_OK)
        else:
            print(f"DEBUG: Authentication failed for email: {email}. Invalid credentials.")
            return Response({'errors': {'non_field_errors': ['Identifiants invalides']}}, status=status.HTTP_401_UNAUTHORIZED)


# --- Logout Serializers ---
class LogoutSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# --- Logout Views ---
class LogoutView(APIView):
    permission_classes = [AllowAny]
    renderer_classes   = [BrowsableAPIRenderer, JSONRenderer]
    serializer_class   = LogoutSerializer
    
    def post(self, request, format=None):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Authenticate user with credentials
        user = authenticate(request, email=email, password=password)

        if user is not None and request.user == user:
            logout(request)
            return Response({'message': 'You have been logged out.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
