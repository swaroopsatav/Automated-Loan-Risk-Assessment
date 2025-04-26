from django import forms
from .models import ComplianceCheck, ComplianceAuditTrail


class ComplianceCheckForm(forms.ModelForm):
    """
    Form for managing `ComplianceCheck` instances.
    Provides validation to ensure user is set when the status is not 'pending'.
    """

    class Meta:
        model = ComplianceCheck
        fields = ['check_type', 'is_compliant', 'user', 'checked_on', 'check_notes']
        widgets = {
            'checked_on': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'check_notes': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        """
        Custom validation to ensure that a user is assigned
        when the compliance status is not 'pending'.
        """
        cleaned_data = super().clean()
        is_compliant = cleaned_data.get("is_compliant")
        user = cleaned_data.get("user")

        if is_compliant != 'pending' and not user:
            raise forms.ValidationError("A user must be assigned when marking compliance status.")
        return cleaned_data


class ComplianceAuditTrailForm(forms.ModelForm):
    """
    Read-only form for `ComplianceAuditTrail` instances.
    All fields are disabled to prevent editing.
    """

    class Meta:
        model = ComplianceAuditTrail
        fields = ['actor', 'loan_application', 'action', 'timestamp', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'readonly': 'readonly'}),
            'timestamp': forms.DateTimeInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and explicitly disable all fields to make them read-only.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
