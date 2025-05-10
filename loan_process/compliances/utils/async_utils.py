"""
Utility functions for asynchronous operations in the compliances module.
"""
from django.db import transaction
from asgiref.sync import sync_to_async, async_to_sync
from ..models import ComplianceCheck, ComplianceAuditTrail
from loanapplications.models import LoanApplication
from users.models import CustomUser

async def get_compliance_checks_async(loan_id):
    """
    Asynchronously retrieve compliance checks for a loan.
    
    Args:
        loan_id: The ID of the loan application
        
    Returns:
        QuerySet of ComplianceCheck objects
    """
    return await sync_to_async(list)(ComplianceCheck.objects.filter(loan_application_id=loan_id))

async def get_compliance_check_async(check_id):
    """
    Asynchronously retrieve a specific compliance check.
    
    Args:
        check_id: The ID of the compliance check
        
    Returns:
        ComplianceCheck object or None if not found
    """
    try:
        return await sync_to_async(ComplianceCheck.objects.get)(id=check_id)
    except ComplianceCheck.DoesNotExist:
        return None

async def update_compliance_check_async(check_id, data, user):
    """
    Asynchronously update a compliance check and create an audit trail.
    
    Args:
        check_id: The ID of the compliance check to update
        data: Dictionary containing the fields to update
        user: The user performing the update
        
    Returns:
        Updated ComplianceCheck object or None if not found
    """
    try:
        # Use transaction to ensure both operations succeed or fail together
        @sync_to_async
        @transaction.atomic
        def update_with_audit():
            check = ComplianceCheck.objects.get(id=check_id)
            
            # Update fields
            for key, value in data.items():
                if hasattr(check, key):
                    setattr(check, key, value)
            
            check.save()
            
            # Create audit trail
            ComplianceAuditTrail.objects.create(
                actor=user,
                loan_application=check.loan_application,
                action='modified',
                notes=f"Compliance check {check.id} updated by {user}"
            )
            
            return check
            
        return await update_with_audit()
    except ComplianceCheck.DoesNotExist:
        return None

async def get_audit_trail_async(loan_id=None):
    """
    Asynchronously retrieve compliance audit trail entries.
    
    Args:
        loan_id: Optional loan ID to filter by
        
    Returns:
        QuerySet of ComplianceAuditTrail objects
    """
    queryset = ComplianceAuditTrail.objects.all().order_by('-timestamp')
    
    if loan_id:
        queryset = queryset.filter(loan_application_id=loan_id)
    
    return await sync_to_async(list)(queryset)