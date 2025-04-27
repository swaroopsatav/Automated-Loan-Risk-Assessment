from django.contrib import admin
from .models import ComplianceCheck, ComplianceAuditTrail


@admin.register(ComplianceCheck)
class ComplianceCheckAdmin(admin.ModelAdmin):
    """
    Admin interface for managing ComplianceCheck records.
    """
    list_display = (
        'loan_application', 'check_type', 'is_compliant',
        'user', 'created_at',
    )
    list_filter = ('check_type', 'is_compliant', 'user', 'created_at')
    search_fields = ('loan_application__id', 'user__username', 'check_notes')
    ordering = ('-created_at',)
    fieldsets = (
        ("Check Info", {
            'fields': ('loan_application', 'check_type', 'is_compliant', 'notes'),
        }),
        ("Review Details", {
            'fields': ('user', 'check_notes'),
            'classes': ('collapse',),
        }),
        ("Metadata", {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at',)
    autocomplete_fields = ('loan_application', 'user')
    date_hierarchy = 'created_at'

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(ComplianceAuditTrail)
class ComplianceAuditTrailAdmin(admin.ModelAdmin):
    """
    Admin interface for managing ComplianceAuditTrail records.
    """
    list_display = ('actor', 'loan_application', 'action', 'timestamp')
    list_filter = ('actor', 'action', 'timestamp')
    search_fields = ('loan_application__id', 'actor__username', 'action', 'notes')
    ordering = ('-timestamp',)
    readonly_fields = [field.name for field in ComplianceAuditTrail._meta.fields]
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
