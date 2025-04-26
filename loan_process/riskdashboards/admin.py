from django.contrib import admin
from .models import RiskSnapshot, RiskTrend, ModelPerformanceLog


@admin.register(RiskSnapshot)
class RiskSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        'snapshot_date', 'total_applications', 'avg_risk_score',
        'high_risk_count', 'low_risk_count',
        'approved_count', 'rejected_count',
        'under_review_count', 'model_version',
    )
    list_filter = ('snapshot_date', 'model_version')
    search_fields = ('snapshot_date', 'model_version')
    readonly_fields = ('created_at',)
    list_per_page = 50
    date_hierarchy = 'snapshot_date'


@admin.register(RiskTrend)
class RiskTrendAdmin(admin.ModelAdmin):
    list_display = ('date', 'avg_score', 'approval_rate', 'rejection_rate', 'model_version')
    list_filter = ('date', 'model_version')
    search_fields = ('date', 'model_version')
    ordering = ('-date',)
    readonly_fields = ('date', 'model_version')
    list_per_page = 50
    date_hierarchy = 'date'


@admin.register(ModelPerformanceLog)
class ModelPerformanceLogAdmin(admin.ModelAdmin):
    list_display = ('model_version', 'timestamp', 'accuracy', 'precision', 'recall', 'auc_score')
    list_filter = ('model_version', 'timestamp')
    search_fields = ('model_version', 'notes')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
    list_per_page = 50
    date_hierarchy = 'timestamp'
