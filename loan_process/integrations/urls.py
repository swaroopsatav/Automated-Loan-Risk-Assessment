from django.urls import path
from .views import (
    MyMockKYCView,
    MockExperianReportView,
    AllMockExperianReportsView,
)

app_name = 'integrations'

urlpatterns = [
    # Endpoint to fetch the current user's mock KYC record 
    path('mock/kyc/', MyMockKYCView.as_view(), name='my-mock-kyc'),

    # Endpoint to fetch a mock Experian report for a specific loan
    path('mock/experian/loan/<int:loan_id>/', MockExperianReportView.as_view(), name='mock-experian-report'),

    # Admin endpoint to fetch all mock Experian reports
    path('mock/experian/reports/', AllMockExperianReportsView.as_view(), name='all-mock-reports'),
]
