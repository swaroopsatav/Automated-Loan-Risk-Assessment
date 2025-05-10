from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async, async_to_sync

from .models import ComplianceCheck, ComplianceAuditTrail
from .serializers import (
    ComplianceCheckSerializer,
    ComplianceCheckUpdateSerializer,
    ComplianceAuditTrailSerializer
)
from .utils.async_utils import (
    get_compliance_checks_async,
    get_compliance_check_async,
    update_compliance_check_async,
    get_audit_trail_async
)


class ComplianceCheckListView(generics.ListAPIView):
    serializer_class = ComplianceCheckSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    async def get_queryset(self):
        """
        Filter compliance checks by the loan ID provided in the URL.
        Returns 404 if loan ID doesn't exist.
        Uses async function to sync with other modules.
        """
        loan_id = self.kwargs.get('loan_id')
        if not loan_id:
            raise ValidationError("Loan ID is required")

        checks = await get_compliance_checks_async(loan_id)
        if not checks:
            raise ValidationError("No compliance checks found for this loan")

        return checks


class ComplianceCheckUpdateView(generics.UpdateAPIView):
    """
    View to allow admins or staff to update a compliance check record.
    Only accessible by admin users.
    Uses async functions to sync with other modules.
    """
    serializer_class = ComplianceCheckUpdateSerializer
    permission_classes = [IsAdminUser]

    async def get_queryset(self):
        return ComplianceCheck.objects.all()

    async def perform_update(self, serializer):
        # Get the check ID from the URL
        check_id = self.kwargs.get('pk')

        # Use the async utility function to update the check and create audit trail
        await update_compliance_check_async(
            check_id=check_id,
            data=serializer.validated_data,
            user=self.request.user
        )


class ComplianceAuditTrailListView(generics.ListAPIView):
    """
    View to list all compliance audit trails.
    Only accessible by admin users.
    Uses async functions to sync with other modules.
    """
    serializer_class = ComplianceAuditTrailSerializer
    permission_classes = [IsAdminUser]

    async def get_queryset(self):
        # Optional filtering by loan ID
        loan_id = self.request.query_params.get('loan_id')

        # Use the async utility function to get audit trail entries
        return await get_audit_trail_async(loan_id=loan_id)
