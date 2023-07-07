from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Revision, Visit

class ReadOnlyModelAdmin(admin.ModelAdmin):
    pass
    # Override has_delete_permission to disable deleting
    # def has_delete_permission(self, request, obj=None):
    #     return False
    
    # def has_change_permission(self, request, obj=None):
    #     return False
    
    # def has_add_permission(self, request, obj=None):
    #     return False

# class VisitInline(admin.TabularInline):
#     model = Visit

# class RevisionModelAdmin(admin.ModelAdmin):
#     inlines = [VisitInline]

# Register your models here.
# admin.site.register(Revision,RevisionModelAdmin)
admin.site.register(Revision,ReadOnlyModelAdmin)
admin.site.register(Visit,ReadOnlyModelAdmin)