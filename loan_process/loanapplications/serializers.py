from rest_framework import serializers
from .models import LoanApplication, LoanDocument
from users.models import CustomUser


# --- Document Serializer ---
class LoanDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanDocument
        fields = ['id', 'loan', 'document_type', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=LoanDocument.objects.all(),
                fields=['loan', 'document_type'],
                message="This document type has already been uploaded for this loan."
            )
        ]


# --- User-facing Loan Create Serializer ---
class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = [
            'id', 'amount_requested', 'purpose', 'term_months',
            'monthly_income', 'existing_loans',
        ]
        read_only_fields = ['id']

    def validate_amount_requested(self, value):
        if value <= 0:
            raise serializers.ValidationError("The loan amount must be a positive number.")
        return value

    def validate_term_months(self, value):
        if value < 1 or value > 360:
            raise serializers.ValidationError("The loan term must be between 1 and 360 months.")
        return value

    def validate_monthly_income(self, value):
        if value <= 0:
            raise serializers.ValidationError("Monthly income must be a positive number.")
        return value


# --- Detail Serializer for User Viewing Their Loan ---
class LoanApplicationDetailSerializer(serializers.ModelSerializer):
    documents = LoanDocumentSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()
    status = serializers.CharField(source='get_status_display')
    ai_decision = serializers.CharField(source='get_ai_decision_display')

    class Meta:
        model = LoanApplication
        fields = [
            'id', 'user', 'amount_requested', 'purpose', 'term_months',
            'monthly_income', 'existing_loans', 'credit_score_records',
            'risk_score', 'ai_decision', 'status',
            'submitted_at', 'reviewed_at', 'notes',
            'ml_scoring_output', 'documents'
        ]
        read_only_fields = [
            'id', 'user', 'risk_score', 'ai_decision', 'status',
            'submitted_at', 'reviewed_at', 'notes',
            'ml_scoring_output', 'documents', 'credit_score_records'
        ]


# --- Admin: Full Loan Serializer ---
class AdminLoanApplicationSerializer(serializers.ModelSerializer):
    documents = LoanDocumentSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=True)
    amount_requested = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    status = serializers.CharField(source='get_status_display', read_only=True)
    ai_decision = serializers.CharField(source='get_ai_decision_display', read_only=True)

    class Meta:
        model = LoanApplication
        fields = '__all__'

    def validate_amount_requested(self, value):
        if value <= 0:
            raise serializers.ValidationError("The loan amount must be a positive number.")
        return value

    def validate(self, data):
        risk_score = data.get('risk_score', 0)
        credit_score = data.get('credit_score_records', 0)
        income = data.get('monthly_income', 0)
        loan_amount = data.get('amount_requested', 0)
        has_existing_loans = data.get('existing_loans', False)

        errors = {}

        if has_existing_loans and risk_score > 80:
            errors['amount_requested'] = "High-risk applicants with existing loans cannot apply for new loans."

        if credit_score < 500:
            errors['amount_requested'] = "Application cannot be processed due to low credit score."

        if income < (loan_amount / 12):
            errors['amount_requested'] = "Monthly income is insufficient for the requested loan amount."

        if errors:
            raise serializers.ValidationError(errors)

        return data
