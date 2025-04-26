from django.db import models
from django.db.models import JSONField
from users.models import CustomUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


def loan_doc_upload_path(instance, filename):
    return f'loan_documents/loan_{instance.loan.id}/{instance.document_type}/{filename}'


class LoanApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    AI_DECISION_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('manual_review', 'Manual Review'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='loan_applications',default=1)

    amount_requested = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        default=0.01
    )
    purpose = models.CharField(max_length=255)
    term_months = models.PositiveIntegerField(validators=[MinValueValidator(1)],default=12)

    monthly_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        default=0.01
    )
    existing_loans = models.BooleanField(default=False)

    # AI & Risk Analysis
    risk_score = models.FloatField(null=True, blank=True)
    ai_decision = models.CharField(
        max_length=20,
        choices=AI_DECISION_CHOICES,
        null=True,
        blank=True
    )
    ml_scoring_output = JSONField(null=True, blank=True)

    # Status & workflow  
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    notes = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    credit_score_records = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(300)]
    )

    def clean(self):
        if self.amount_requested and self.amount_requested <= 0:
            raise ValidationError("Amount requested must be greater than zero")
        if self.monthly_income and self.monthly_income <= 0:
            raise ValidationError("Monthly income must be greater than zero")
        if self.credit_score_records and (self.credit_score_records < 300 or self.credit_score_records > 850):
            raise ValidationError("Credit score must be between 300 and 850")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class LoanDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('bank_statement', 'Bank Statement'),
        ('salary_slip', 'Salary Slip'),
        ('id_proof', 'ID Proof'),
        ('address_proof', 'Address Proof'),
    ]

    loan = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(
        max_length=100,
        choices=DOCUMENT_TYPE_CHOICES
    )
    file = models.FileField(upload_to=loan_doc_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('loan', 'document_type')

    def __str__(self):
        return f"{self.get_document_type_display()} for Loan #{self.loan.id}"
