from rest_framework import serializers
from .models import MockKYCRecord, MockExperianReport


class MockKYCSerializer(serializers.ModelSerializer):
    """
    Serializer for the MockKYCRecord model. 
    All fields are read-only by default.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MockKYCRecord
        fields = [
            'id',
            'user',
            'pan_number',
            'pan_holder_name',
            'pan_verified',
            'aadhaar_last_4',
            'aadhaar_verified',
            'dob',
            'kyc_type',
            'verification_status',
            'verification_source',
            'mock_response',
            'created_at'
        ]
        read_only_fields = fields


class MockExperianReportSerializer(serializers.ModelSerializer):
    """
    Serializer for the MockExperianReport model.
    All fields are read-only by default.
    """
    loan_application = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    tradelines = serializers.JSONField(required=False)
    enquiries = serializers.JSONField(required=False)

    class Meta:
        model = MockExperianReport
        fields = [
            'id',
            'loan_application',
            'user',
            'bureau_score',
            'score_band',
            'report_status',
            'total_accounts',
            'active_accounts',
            'overdue_accounts',
            'dpd_max',
            'credit_utilization_pct',
            'emi_to_income_ratio',
            'tradelines',
            'enquiries',
            'mock_raw_report',
            'created_at'
        ]
        read_only_fields = fields
