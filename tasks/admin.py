from django.contrib import admin
from .models import Task
from django.utils.translation import gettext_lazy as _

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'due_date', 'created_at', 'updated_at')
    list_filter = ('status', 'user', 'created_at', 'due_date')
    search_fields = ('title', 'description', 'user__username', 'user__email')
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {'fields': ('user', 'title', 'description')}),
        (_('Status'), {'fields': ('status',)}),
        (_('Dates'), {'fields': ('due_date', 'created_at', 'updated_at')}),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

admin.site.register(Task, TaskAdmin)