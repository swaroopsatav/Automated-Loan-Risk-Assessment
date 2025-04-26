from django.urls import path
from .views import (
    ComplianceCheckListView,
    ComplianceCheckUpdateView,
    ComplianceAuditTrailListView,
)

app_name = 'compliances'

urlpatterns = [
    # Retrieve all compliance checks for a specific loan
    path(
        'loan/<int:loan_id>/checks/',
        ComplianceCheckListView.as_view(),
        name='loan-compliance-checks'
    ),

    # Update a specific compliance check
    path(
        'checks/<int:pk>/',
        ComplianceCheckUpdateView.as_view(),
        name='update-compliance-check'
    ),

    # Retrieve the compliance audit trail
    path(
        'audit-trail/',
        ComplianceAuditTrailListView.as_view(),
        name='compliance-audit-trail'
    ),
]
