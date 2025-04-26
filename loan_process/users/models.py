from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.utils.timezone import now
from django.conf import settings
import os

# Validator for phone number
phone_regex = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits."
)


# Function to define upload path for user documents
def user_document_upload_path(instance, filename):
    # Get file extension while handling case sensitivity
    ext = os.path.splitext(filename)[1].lower()
    # Generate unique filename using timestamp
    new_filename = f"{now().strftime('%Y%m%d_%H%M%S')}{ext}"
    return os.path.join('kyc_documents', f'user_{instance.id}', new_filename)


class CustomUser(AbstractUser):
    # --- Basic Profile Info ---
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[phone_regex],
        help_text="Enter 10 digit phone number without any spaces or special characters"
    )
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # --- Financial Profile ---
    annual_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Annual income in local currency"
    )
    employment_status = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=[
            ('employed', 'Employed'),
            ('self_employed', 'Self Employed'),
            ('unemployed', 'Unemployed'),
            ('retired', 'Retired')
        ]
    )
    credit_score = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinLengthValidator(300), MaxLengthValidator(900)]
    )
    credit_history_fetched = models.BooleanField(default=False)

    # --- KYC Verification ---
    is_kyc_verified = models.BooleanField(default=False)
    kyc_verified_on = models.DateTimeField(blank=True, null=True)
    govt_id_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=[
            ('passport', 'Passport'),
            ('driving_license', 'Driving License'),
            ('national_id', 'National ID')
        ]
    )
    govt_id_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(6, "Government ID number must be at least 6 characters."),
            MaxLengthValidator(100, "Government ID number cannot exceed 100 characters.")
        ]
    )

    # --- Document Uploads ---
    id_proof = models.FileField(
        upload_to=user_document_upload_path,
        blank=True,
        null=True,
        help_text="Upload government issued photo ID"
    )
    address_proof = models.FileField(
        upload_to=user_document_upload_path,
        blank=True,
        null=True,
        help_text="Upload proof of current residential address"
    )
    income_proof = models.FileField(
        upload_to=user_document_upload_path,
        blank=True,
        null=True,
        help_text="Upload latest salary slip or tax returns"
    )

    # --- Experian API Linkage ---
    experian_customer_ref = models.CharField(max_length=100, blank=True, null=True)
    last_experian_sync = models.DateTimeField(blank=True, null=True)
    experian_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('success', 'Success'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.email})"

    def save(self, *args, **kwargs):
        if self.is_kyc_verified and not self.kyc_verified_on:
            self.kyc_verified_on = now()
        super().save(*args, **kwargs)
