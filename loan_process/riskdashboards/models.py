from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import date


class RiskSnapshot(models.Model):
    """Periodic snapshot of system-wide credit risk scoring metrics."""
    snapshot_date = models.DateField(default=date.today, unique=True, db_index=True)

    total_applications = models.PositiveIntegerField(default=0)
    avg_risk_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        default=0.0
    )
    high_risk_count = models.PositiveIntegerField(default=0)
    low_risk_count = models.PositiveIntegerField(default=0)
    approved_count = models.PositiveIntegerField(default=0)
    rejected_count = models.PositiveIntegerField(default=0)
    under_review_count = models.PositiveIntegerField(default=0)

    model_version = models.CharField(max_length=50, default='xgboost_v1', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-snapshot_date']
        indexes = [
            models.Index(fields=['snapshot_date', 'model_version']),
        ]

    def __str__(self):
        return f"Risk Snapshot - {self.snapshot_date}"

    def clean(self):
        super().clean()
        if self.total_applications != (self.approved_count + self.rejected_count + self.under_review_count):
            raise ValidationError("Total applications must equal sum of approved, rejected and under review")
        if self.high_risk_count + self.low_risk_count > self.total_applications:
            raise ValidationError("Sum of risk counts cannot exceed total applications")


class RiskTrend(models.Model):
    """Trends over time (e.g., rolling weekly/monthly risk metrics)."""
    date = models.DateField(db_index=True)
    avg_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        default=0.0
    )
    approval_rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        default=0.0
    )
    rejection_rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        default=0.0
    )
    model_version = models.CharField(max_length=50, default='xgboost_v1', db_index=True)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date', 'model_version']),
        ]

    def __str__(self):
        return f"Trend on {self.date}"

    def clean(self):
        super().clean()
        if round(self.approval_rate + self.rejection_rate, 2) > 100.0:
            raise ValidationError("Sum of approval and rejection rates cannot exceed 100%")


class ModelPerformanceLog(models.Model):
    """Log of model evaluation metrics over time (accuracy, precision, etc.)."""
    model_version = models.CharField(max_length=50, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    accuracy = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.0
    )
    precision = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.0
    )
    recall = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.0
    )
    auc_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.0
    )

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp', 'model_version']),
        ]

    def __str__(self):
        return f"Model {self.model_version} - {self.timestamp.date()}"
