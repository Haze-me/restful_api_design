
from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer
from utils.responses import success_response, error_response
from utils.permissions import IsOwnerOrReadOnly
from django.utils import timezone
from django.http import Http404
from django.db.models import Q

class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'due_date']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(user=user)
        
        # Filter by status if provided
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
            
        # Filter by due date range if provided
        due_date_from = self.request.query_params.get('due_date_from', None)
        due_date_to = self.request.query_params.get('due_date_to', None)
        
        if due_date_from:
            queryset = queryset.filter(due_date__gte=due_date_from)
        if due_date_to:
            queryset = queryset.filter(due_date__lte=due_date_to)
            
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return success_response(
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return error_response(
            message="Validation error",
            data=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
   
     )

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        if not obj.user == self.request.user:
            raise Http404("Task not found")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return success_response(data=serializer.data)
        except Http404:
            return error_response(
                message="Task not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return success_response(data=serializer.data)
            return error_response(
                message="Validation error",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Http404:
            return error_response(
                message="Task not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return success_response(data=serializer.data)
            return error_response(
                message="Validation error during patch",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Http404:
            return error_response(
                message="Task not found in the database",
                status_code=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return success_response(message="Tasked deleted successfully")
        except Http404:
            return error_response(
                message="Task not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
