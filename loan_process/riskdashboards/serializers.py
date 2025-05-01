from rest_framework import serializers
from .models import RiskSnapshot, RiskTrend, ModelPerformanceLog


class RiskSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskSnapshot
        fields = [
            'id', 'snapshot_date', 'total_applications', 'avg_risk_score',
            'high_risk_count', 'low_risk_count', 'approved_count',
            'rejected_count', 'under_review_count', 'model_version',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'avg_risk_score': {'max_value': 100, 'min_value': 0}
        }

    def validate_avg_risk_score(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Average risk score must be between 0 and 100.")
        return value


class RiskTrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskTrend
        fields = [
            'id', 'date', 'avg_score', 'approval_rate', 'rejection_rate',
            'model_version',
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'avg_score': {'max_value': 100, 'min_value': 0},
            'approval_rate': {'max_value': 100, 'min_value': 0},
            'rejection_rate': {'max_value': 100, 'min_value': 0}
        }

    def validate(self, data):
        for field in ['avg_score', 'approval_rate', 'rejection_rate']:
            if data.get(field) and (data[field] < 0 or data[field] > 100):
                raise serializers.ValidationError(f"{field} must be between 0 and 100.")
        return data


class ModelPerformanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelPerformanceLog
        fields = [
            'id', 'model_version', 'timestamp', 'accuracy', 'precision',
            'recall', 'auc_score', 'f1_score', 'notes',
        ]
        read_only_fields = ['id', 'timestamp']
        extra_kwargs = {
            'accuracy': {'max_value': 1.0, 'min_value': 0.0},
            'precision': {'max_value': 1.0, 'min_value': 0.0},
            'recall': {'max_value': 1.0, 'min_value': 0.0},
            'auc_score': {'max_value': 1.0, 'min_value': 0.0},
            'f1_score': {'max_value': 1.0, 'min_value': 0.0}
        }

    def validate(self, data):
        metrics = ['accuracy', 'precision', 'recall', 'auc_score', 'f1_score']
        for metric in metrics:
            if data.get(metric) and (data[metric] < 0 or data[metric] > 1):
                raise serializers.ValidationError(f"{metric} must be between 0 and 1.")
            if data.get(metric):
                data[metric] = round(data[metric], 4)
        return data
