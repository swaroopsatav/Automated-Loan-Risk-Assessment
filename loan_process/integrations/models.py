from django.db import models
from users.models import CustomUser
from loanapplications.models import LoanApplication
from django.core.validators import MinValueValidator, MaxValueValidator


class MockKYCRecord(models.Model):
    """
    Simulated response from a real-world KYC API (PAN + Aadhaar verification).
    Stores mock KYC data for a user.
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='mock_kyc',
        help_text="The user associated with this mock KYC record."
    )

    pan_number = models.CharField(
        max_length=20,
        help_text="The PAN number of the user.",
        validators=[MinValueValidator(10)]
    )
    pan_holder_name = models.CharField(
        max_length=255,
        help_text="The name on the PAN card."
    )
    pan_verified = models.BooleanField(
        default=False,
        help_text="Indicates whether the PAN is verified."
    )

    aadhaar_last_4 = models.CharField(
        max_length=4,
        help_text="The last 4 digits of the Aadhaar number.",
        validators=[MinValueValidator(4), MaxValueValidator(4)]
    )
    aadhaar_verified = models.BooleanField(
        default=False,
        help_text="Indicates whether the Aadhaar is verified."
    )

    dob = models.DateField(
        help_text="The date of birth of the user."
    )

    KYC_TYPE_CHOICES = [
        ('full', 'Full KYC'),
        ('simplified', 'Simplified KYC')
    ]
    kyc_type = models.CharField(
        max_length=50,
        choices=KYC_TYPE_CHOICES,
        default="simplified",
        help_text="The type of KYC (full or simplified)."
    )

    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('failed', 'Failed')
    ]
    verification_status = models.CharField(
        max_length=50,
        choices=VERIFICATION_STATUS_CHOICES,
        default="pending",
        help_text="The status of the KYC verification."
    )

    VERIFICATION_SOURCE_CHOICES = [
        ('mock_provider', 'Mock Provider'),
        ('real_provider', 'Real Provider')
    ]
    verification_source = models.CharField(
        max_length=100,
        choices=VERIFICATION_SOURCE_CHOICES,
        default="mock_provider",
        help_text="The source of the KYC verification."
    )

    mock_response = models.JSONField(
        blank=True,
        null=True,
        help_text="The raw mock response from the KYC API."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The timestamp when this record was created."
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Mock KYC Record'
        verbose_name_plural = 'Mock KYC Records'

    def __str__(self):
        return f"Mock KYC for {self.user.username}"

    def clean(self):
        super().clean()
        if len(self.aadhaar_last_4) != 4:
            raise models.ValidationError('Aadhaar last 4 digits must be exactly 4 characters')
        if len(self.pan_number) < 10:
            raise models.ValidationError('PAN number must be at least 10 characters')


class MockExperianReport(models.Model):
    """
    Simulated Experian-style credit report based on a real schema.
    Stores mock credit report data for a loan application.
    """
    loan_application = models.ForeignKey(
        LoanApplication,
        on_delete=models.CASCADE,
        related_name='mock_experian',
        help_text="The loan application associated with this mock Experian report."
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='experian_reports',
        help_text="The user associated with this mock Experian report."
    )

    bureau_score = models.IntegerField(
        help_text="The credit score of the user.",
        validators=[MinValueValidator(300), MaxValueValidator(900)]
    )

    SCORE_BAND_CHOICES = [
        ('poor', 'Poor (300-579)'),
        ('fair', 'Fair (580-669)'),
        ('good', 'Good (670-739)'),
        ('very_good', 'Very Good (740-799)'),
        ('excellent', 'Excellent (800-850)')
    ]
    score_band = models.CharField(
        max_length=100,
        choices=SCORE_BAND_CHOICES,
        help_text="The band of the credit score."
    )

    REPORT_STATUS_CHOICES = [
        ('mocked', 'Mocked'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]
    report_status = models.CharField(
        max_length=50,
        choices=REPORT_STATUS_CHOICES,
        default="processing",
        help_text="The status of the report."
    )

    total_accounts = models.PositiveIntegerField(
        help_text="The total number of credit accounts."
    )
    active_accounts = models.PositiveIntegerField(
        help_text="The number of active credit accounts."
    )
    overdue_accounts = models.PositiveIntegerField(
        help_text="The number of overdue credit accounts."
    )
    dpd_max = models.PositiveIntegerField(
        help_text="The maximum number of Days Past Due (DPD) for credit accounts."
    )
    credit_utilization_pct = models.FloatField(
        help_text="The percentage of credit utilization.",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    emi_to_income_ratio = models.FloatField(
        help_text="The ratio of EMI to income.",
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )

    tradelines = models.JSONField(
        blank=True,
        null=True,
        help_text="The tradelines in the credit report."
    )
    enquiries = models.JSONField(
        blank=True,
        null=True,
        help_text="The enquiries in the credit report."
    )

    mock_raw_report = models.JSONField(
        help_text="The raw mock API response for the credit report."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The timestamp when this report was created."
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Mock Experian Report'
        verbose_name_plural = 'Mock Experian Reports'

    def __str__(self):
        return f"Mock Experian Report for Loan #{self.loan_application.id}"

    def clean(self):
        super().clean()
        if self.active_accounts > self.total_accounts:
            raise models.ValidationError('Active accounts cannot exceed total accounts')
        if self.overdue_accounts > self.active_accounts:
            raise models.ValidationError('Overdue accounts cannot exceed active accounts')
