from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Revision, Visit

# Make both models read-only. Also set it to make relations visible

class ReadOnlyModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False

class VisitInline(admin.TabularInline):
    model = Visit.revisions.through
    extra = 0

class ReadOnlyRevisionAdmin(admin.ModelAdmin):
    inlines = [VisitInline]

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False

# Register models
admin.site.register(Revision, ReadOnlyRevisionAdmin)
admin.site.register(Visit, ReadOnlyModelAdmin)
