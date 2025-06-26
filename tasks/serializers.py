from rest_framework import serializers
from .models import Task
from users.models import User
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    status = serializers.ChoiceField(choices=Task.Status.choices)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 'user', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_due_date(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value