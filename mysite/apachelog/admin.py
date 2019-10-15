from django.contrib import admin

from apachelog.models import ApacheLog


@admin.register(ApacheLog)
class ApacheLogAdmin(admin.ModelAdmin):
    list_display = ('host', 'time', 'method', 'url', 'status', 'size')
    search_fields = ('host', 'time', 'method', 'url', 'status', 'size')
    ordering = ('time',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
