
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserListView,
    UserDetailView,
    CustomTokenObtainPairView,
    RegisterView,
)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]