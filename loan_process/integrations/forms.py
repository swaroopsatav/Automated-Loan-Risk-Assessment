from django import forms
from .models import MockKYCRecord, MockExperianReport
import json
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.utils import timezone


class MockKYCRecordForm(forms.ModelForm):
    class Meta:
        model = MockKYCRecord
        fields = '__all__'
        widgets = {
            'mock_response': forms.Textarea(attrs={'rows': 6, 'class': 'monospace'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form, pre-filling the JSON fields with formatted JSON if the instance exists.
        """
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.mock_response:
            self.fields['mock_response'].initial = json.dumps(self.instance.mock_response, indent=2)

    def clean_mock_response(self):
        """
        Validates and parses the mock_response field as JSON.
        """
        raw = self.cleaned_data.get('mock_response')
        if not raw:
            return None
        if isinstance(raw, dict):
            return raw
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON format in mock_response.")

    def clean_dob(self):
        """
        Validates that DOB is not in the future
        """
        dob = self.cleaned_data.get('dob')
        if dob and dob > timezone.now().date():
            raise ValidationError("Date of birth cannot be in the future")
        return dob


class MockExperianReportForm(forms.ModelForm):
    class Meta:
        model = MockExperianReport
        fields = '__all__'
        widgets = {
            'mock_raw_report': forms.Textarea(attrs={'rows': 6, 'class': 'monospace'}),
            'tradelines': forms.Textarea(attrs={'rows': 4, 'class': 'monospace'}),
            'enquiries': forms.Textarea(attrs={'rows': 4, 'class': 'monospace'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form, pre-filling the JSON fields with formatted JSON if the instance exists.
        """
        super().__init__(*args, **kwargs)
        json_fields = ['mock_raw_report', 'tradelines', 'enquiries']
        for field in json_fields:
            value = getattr(self.instance, field, None)
            if value:
                self.fields[field].initial = json.dumps(value, indent=2)

    def _parse_json_field(self, field_value, field_name):
        """
        Helper method to validate and parse a JSON field.
        """
        if not field_value:
            return None
        if isinstance(field_value, (dict, list)):
            return field_value
        try:
            return json.loads(field_value)
        except json.JSONDecodeError:
            raise ValidationError(f"Invalid JSON in {field_name}")

    def clean_mock_raw_report(self):
        """
        Validates and parses the mock_raw_report field as JSON.
        """
        raw = self.cleaned_data.get('mock_raw_report')
        if not raw:
            return {}
        return self._parse_json_field(raw, 'mock_raw_report')

    def clean_tradelines(self):
        """
        Validates and parses the tradelines field as JSON.
        """
        data = self.cleaned_data.get('tradelines')
        if not data:
            return []
        return self._parse_json_field(data, 'tradelines')

    def clean_enquiries(self):
        """
        Validates and parses the enquiries field as JSON.
        """
        data = self.cleaned_data.get('enquiries')
        if not data:
            return []
        return self._parse_json_field(data, 'enquiries')
