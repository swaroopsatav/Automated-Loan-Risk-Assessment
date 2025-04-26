from rest_framework import serializers
from .models import CreditScoreRecord


# --- Serializer for regular users to view their loan score ---
class CreditScoreDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for regular users to view their credit score details.
    Only includes the fields relevant to the user.
    """
    loan_id = serializers.IntegerField(source='loan_application.id', read_only=True)
    risk_score = serializers.FloatField(min_value=0.0, max_value=1.0)
    decision = serializers.ChoiceField(choices=['approve', 'reject', 'manual_review'], read_only=True)
    scoring_inputs = serializers.JSONField(read_only=True)
    scoring_output = serializers.JSONField(read_only=True)

    class Meta:
        model = CreditScoreRecord
        fields = [
            'id', 'loan_id', 'risk_score', 'decision',
            'model_name', 'scoring_inputs', 'scoring_output', 'created_at'
        ]
        read_only_fields = fields


# --- Serializer for admin users to view full credit score details ---  
class AdminCreditScoreSerializer(serializers.ModelSerializer):
    """
    Serializer for admin users to view detailed credit score records.
    Includes user details and all fields from the CreditScoreRecord.
    """
    user = serializers.StringRelatedField()
    loan_id = serializers.IntegerField(source='loan_application.id', read_only=True)
    risk_score = serializers.FloatField(min_value=0.0, max_value=1.0)
    decision = serializers.ChoiceField(choices=['approve', 'reject', 'manual_review'], read_only=True)
    scoring_inputs = serializers.JSONField(read_only=True)
    scoring_output = serializers.JSONField(read_only=True)
    credit_utilization_pct = serializers.FloatField(min_value=0.0, max_value=100.0, read_only=True)
    dpd_max = serializers.IntegerField(min_value=0, read_only=True)
    emi_to_income_ratio = serializers.FloatField(min_value=0.0, max_value=1.0, read_only=True)

    class Meta:
        model = CreditScoreRecord
        fields = [
            'id', 'user', 'loan_id',
            'model_name', 'risk_score', 'decision',
            'scoring_inputs', 'scoring_output', 'created_at',
            'credit_utilization_pct', 'dpd_max', 'emi_to_income_ratio'
        ]
        read_only_fields = fields
