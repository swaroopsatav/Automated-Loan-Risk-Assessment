from django.db import models
from django.core.exceptions import ValidationError
from users.models import CustomUser
from loanapplications.models import LoanApplication
from django.core.validators import MinValueValidator, MaxValueValidator


class CreditScoreRecord(models.Model):
    """
    Stores the credit scoring results for a loan application.
    This includes the risk score, decision, and additional details such as model inputs and outputs.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='credit_scores',
        help_text="The user associated with this credit score record."
    )
    loan_application = models.OneToOneField(
        LoanApplication,
        on_delete=models.CASCADE,
        related_name='credit_scoring_record',
        help_text="The loan application associated with this credit score record."
    )

    # ML model information
    model_name = models.CharField(
        max_length=100,
        default='xgboost_v1',
        help_text="The name or version of the ML model used for scoring."
    )
    risk_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="The calculated risk score for this loan application (between 0 and 1)."
    )
    decision = models.CharField(
        max_length=20,
        choices=[
            ('approve', 'Approve'),
            ('reject', 'Reject'),
            ('manual_review', 'Manual Review')
        ],
        default='manual_review',
        help_text="The decision made by the model for this loan application."
    )
    scoring_inputs = models.JSONField(
        help_text="Input features used by the model for scoring.",
        default=dict,
        null=True,
        blank=True
    )
    scoring_output = models.JSONField(
        blank=True,
        null=True,
        help_text="Optional: Model outputs like SHAP values or feature importance."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The timestamp when the credit score record was created."
    )
    credit_utilization_pct = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="The credit utilization percentage of the user at the time of scoring (0-100%)."
    )
    dpd_max = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="The maximum number of days past due for the user in their credit history."
    )
    emi_to_income_ratio = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="The ratio of the user's equated monthly installment (EMI) to their monthly income (between 0 and 1)."
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['loan_application']),
        ]

    def __str__(self):
        return f"Credit Score for Loan #{self.loan_application.id} ({self.user.username})"

    def clean(self):
        if self.risk_score < 0 or self.risk_score > 1:
            raise ValidationError({'risk_score': 'Risk score must be between 0 and 1'})
        if self.credit_utilization_pct and (self.credit_utilization_pct < 0 or self.credit_utilization_pct > 100):
            raise ValidationError({'credit_utilization_pct': 'Credit utilization must be between 0 and 100'})
        if self.dpd_max and self.dpd_max < 0:
            raise ValidationError({'dpd_max': 'Days past due cannot be negative'})
        if self.emi_to_income_ratio and (self.emi_to_income_ratio < 0 or self.emi_to_income_ratio > 1):
            raise ValidationError({'emi_to_income_ratio': 'EMI to income ratio must be between 0 and 1'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
