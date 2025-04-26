from django import forms
from .models import CreditScoreRecord


class CreditScoreReviewForm(forms.ModelForm):
    """Optional: Let underwriters review/override AI decisions."""

    class Meta:
        model = CreditScoreRecord
        fields = ['decision']
        widgets = {
            'decision': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_decision(self):
        decision = self.cleaned_data.get('decision')
        if not decision:
            raise forms.ValidationError("Decision is required.")

        decision = decision.lower()
        valid_choices = [choice[0] for choice in CreditScoreRecord._meta.get_field('decision').choices]

        if decision not in valid_choices:
            raise forms.ValidationError(f"Invalid decision. Expected one of {valid_choices}.")

        return decision


class CreditScoreReadOnlyForm(forms.ModelForm):
    """Display scoring data (inputs/outputs) without allowing edits."""

    class Meta:
        model = CreditScoreRecord
        fields = '__all__'
        labels = {
            'risk_score': 'Risk Score',
            'credit_utilization_pct': 'Credit Utilization %',
            'dpd_max': 'Maximum Days Past Due',
            'emi_to_income_ratio': 'EMI to Income Ratio'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].disabled = True
            self.fields[field].widget.attrs.update({
                'readonly': True,
                'class': 'form-control-plaintext'
            })
