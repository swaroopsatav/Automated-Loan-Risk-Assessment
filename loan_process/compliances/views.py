from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404

from .models import ComplianceCheck, ComplianceAuditTrail
from .serializers import (
    ComplianceCheckSerializer,
    ComplianceCheckUpdateSerializer,
    ComplianceAuditTrailSerializer
)


class ComplianceCheckListView(generics.ListAPIView):
    serializer_class = ComplianceCheckSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter compliance checks by the loan ID provided in the URL.
        Returns 404 if loan ID doesn't exist.
        """
        loan_id = self.kwargs.get('loan_id')
        if not loan_id:
            raise ValidationError("Loan ID is required")

        queryset = ComplianceCheck.objects.filter(loan_application_id=loan_id)
        if not queryset.exists():
            raise ValidationError("No compliance checks found for this loan")

        return queryset


class ComplianceCheckUpdateView(generics.UpdateAPIView):
    """
    View to allow admins or staff to update a compliance check record.
    Only accessible by admin users.
    """
    serializer_class = ComplianceCheckUpdateSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return ComplianceCheck.objects.all()

    def perform_update(self, serializer):
        compliance_check = serializer.save()

        # Create audit trail entry
        ComplianceAuditTrail.objects.create(
            actor=self.request.user,
            loan_application=compliance_check.loan_application,
            action='modified',
            notes=f"Compliance check {compliance_check.id} updated by {self.request.user}"
        )


class ComplianceAuditTrailListView(generics.ListAPIView):
    """
    View to list all compliance audit trails.
    Only accessible by admin users.
    """
    serializer_class = ComplianceAuditTrailSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = ComplianceAuditTrail.objects.all().order_by('-timestamp')

        # Optional filtering by loan ID
        loan_id = self.request.query_params.get('loan_id')
        if loan_id:
            queryset = queryset.filter(loan_application_id=loan_id)

        return queryset
