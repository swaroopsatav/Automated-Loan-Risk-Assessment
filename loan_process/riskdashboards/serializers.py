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
            'recall', 'auc_score', 'notes',
        ]
        read_only_fields = ['id', 'timestamp']

    def validate(self, data):
        metrics = ['accuracy', 'precision', 'recall', 'auc_score']
        for metric in metrics:
            if data.get(metric) and (data[metric] < 0 or data[metric] > 1):
                raise serializers.ValidationError(f"{metric} must be between 0 and 1.")
            if data.get(metric):
                data[metric] = round(data[metric], 4)
        return data
