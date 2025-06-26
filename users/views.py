
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, RegisterSerializer
from utils.responses import success_response, error_response
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
import logging
from rest_framework import serializers

logger = logging.getLogger(__name__)

User = get_user_model()

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You don't have permission to view this profile")
        return obj

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        # Ensure required fields are included
        if 'username' not in data:
            data['username'] = instance.username
        if 'email' not in data:
            data['email'] = instance.email
            
        serializer = self.get_serializer(instance, data=data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data)
        return error_response(
            message="Validation error",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response(
            message="User deleted successfully",
            status_code=status.HTTP_200_OK
        )
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        logger.info(f"Login attempt for email: {request.data.get('email')}")
        
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            
            response_data = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Login successful',
                'data': serializer.validated_data
            }
            
            logger.info(f"Login successful for user: {serializer.user.email}")
            return Response(response_data, status=status.HTTP_200_OK)
            
        except serializers.ValidationError as e:
            logger.warning(f"Login failed - validation error: {str(e)}")
            response_data = {
                'success': False,
                'status_code': status.HTTP_401_UNAUTHORIZED,
                'message': 'Invalid credentials',
                'data': None,
                'errors': {'detail': 'Invalid credentials'}
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
            
        except Exception as e:
            logger.error(f"Login failed - unexpected error: {str(e)}", exc_info=True)
            response_data = {
                'success': False,
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'An error occurred during authentication',
                'data': None,
                'error': str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return success_response(
                data=UserSerializer(user).data,
                status_code=status.HTTP_201_CREATED
            )
        return error_response(
            message="Validation error",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )