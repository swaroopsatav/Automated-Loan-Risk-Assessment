from django import forms
from .models import RiskSnapshot, RiskTrend, ModelPerformanceLog


class RiskSnapshotForm(forms.ModelForm):
    class Meta:
        model = RiskSnapshot
        fields = '__all__'
        widgets = {
            field.name: forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
            for field in RiskSnapshot._meta.fields
            if field.name != 'id'  # Exclude id field
        }


class RiskTrendForm(forms.ModelForm):
    class Meta:
        model = RiskTrend
        fields = '__all__'
        widgets = {
            field.name: forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
            for field in RiskTrend._meta.fields
            if field.name != 'id'  # Exclude id field
        }


class ModelPerformanceLogForm(forms.ModelForm):
    class Meta:
        model = ModelPerformanceLog
        fields = '__all__'
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
        }

    def clean_metric(self, metric_name):
        value = self.cleaned_data.get(metric_name)
        if value is None:
            raise forms.ValidationError(f"{metric_name} is required")
        if not 0 <= value <= 1:
            raise forms.ValidationError(f"{metric_name} must be between 0 and 1")
        return round(value, 4)

    def clean_accuracy(self):
        return self.clean_metric('accuracy')

    def clean_precision(self):
        return self.clean_metric('precision')

    def clean_recall(self):
        return self.clean_metric('recall')

    def clean_auc_score(self):
        return self.clean_metric('auc_score')

    def clean_f1_score(self):
        return self.clean_metric('f1_score')
