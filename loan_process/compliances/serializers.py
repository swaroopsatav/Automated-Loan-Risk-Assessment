from rest_framework import serializers
from .models import ComplianceCheck, ComplianceAuditTrail


class ComplianceCheckSerializer(serializers.ModelSerializer):
    """
    Serializer for read-only representation of ComplianceCheck data.
    Includes loan ID and reviewer details in a user-friendly format.
    """
    loan_id = serializers.IntegerField(source='loan_application.id', read_only=True)
    reviewer = serializers.StringRelatedField(read_only=True)
    check_type_display = serializers.CharField(source='get_check_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ComplianceCheck
        fields = [
            'id',
            'loan_id',
            'check_type',
            'check_type_display',
            'status',
            'status_display',
            'reviewer',
            'review_notes',
            'created_at',
            'reviewed_at'
        ]
        read_only_fields = fields


class ComplianceCheckUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating ComplianceCheck data.
    Allows updating of status, reviewer, review timestamp, and notes.
    """

    class Meta:
        model = ComplianceCheck
        fields = ['status', 'reviewer', 'review_notes', 'reviewed_at']

    def validate_status(self, value):
        if value not in dict(ComplianceCheck.STATUS_CHOICES):
            raise serializers.ValidationError("Invalid status value")
        return value


class ComplianceAuditTrailSerializer(serializers.ModelSerializer):
    """
    Serializer for read-only representation of ComplianceAuditTrail data.
    Includes actor and loan ID in a user-friendly format.
    """
    actor = serializers.StringRelatedField()
    loan_id = serializers.IntegerField(source='loan_application.id')
    action_display = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = ComplianceAuditTrail
        fields = ['id', 'actor', 'loan_id', 'action', 'action_display', 'timestamp', 'notes']
        read_only_fields = fields
