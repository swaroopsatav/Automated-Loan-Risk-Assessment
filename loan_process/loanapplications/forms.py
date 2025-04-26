from django import forms
from .models import LoanApplication, LoanDocument


class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = [
            'amount_requested', 'purpose', 'term_months',
            'monthly_income', 'existing_loans'
        ]
        widgets = {
            'purpose': forms.TextInput(attrs={'placeholder': 'E.g. Home renovation, Business expansion'}),
            'term_months': forms.NumberInput(attrs={'min': 1, 'max': 360}),
            'amount_requested': forms.NumberInput(attrs={'min': 0.01}),
            'monthly_income': forms.NumberInput(attrs={'min': 0.01}),
        }

    def clean_amount_requested(self):
        amount = self.cleaned_data.get('amount_requested')
        if not amount:
            raise forms.ValidationError("Loan amount is required.")
        if amount <= 0:
            raise forms.ValidationError("Loan amount must be positive.")
        return amount

    def clean_term_months(self):
        term = self.cleaned_data.get('term_months')
        if not term:
            raise forms.ValidationError("Loan term is required.")
        if term < 1 or term > 360:
            raise forms.ValidationError("Term must be between 1 and 360 months.")
        return term

    def clean_monthly_income(self):
        income = self.cleaned_data.get('monthly_income')
        if not income:
            raise forms.ValidationError("Monthly income is required.")
        if income <= 0:
            raise forms.ValidationError("Monthly income must be positive.")
        return income


class LoanReviewForm(forms.ModelForm):
    """For manual review by underwriters."""

    class Meta:
        model = LoanApplication
        fields = ['status', 'notes', 'ai_decision']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        notes = cleaned_data.get('notes')
        ai_decision = cleaned_data.get('ai_decision')

        if status in ['rejected', 'under_review'] and not notes:
            raise forms.ValidationError({
                'notes': "Notes are required for rejected or under review applications."
            })

        if status == 'approved' and ai_decision == 'reject':
            raise forms.ValidationError("Cannot approve a loan that AI recommended to reject.")

        return cleaned_data


class LoanDocumentForm(forms.ModelForm):
    class Meta:
        model = LoanDocument
        fields = ['document_type', 'file']
        widgets = {
            'document_type': forms.Select(choices=[
                ('id_proof', 'ID Proof'),
                ('bank_statement', 'Bank Statement'),
                ('salary_slip', 'Salary Slip'),
                ('other', 'Other')
            ])
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise forms.ValidationError("Document file is required.")
        return file
