from django.urls import path
from .views import (
    CreditScoreByLoanView,
    AdminCreditScoreListView,
    AdminCreditScoreDetailView,
    RescoreLoanView
)

app_name = 'creditscorings'

urlpatterns = [
    # --- User-Facing Endpoints ---
    # Get credit score details for a specific loan (by loan ID)
    path('loans/<int:loan_id>/score/', CreditScoreByLoanView.as_view(), name='loan-score'),

    # --- Admin Endpoints --- 
    # List all credit scores for admin users
    path('admin/scores/', AdminCreditScoreListView.as_view(), name='admin-score-list'),
    # Retrieve detailed credit score record for a specific score (by ID)
    path('admin/scores/<int:pk>/', AdminCreditScoreDetailView.as_view(), name='admin-score-detail'),
    # Re-score a specific loan application (by loan ID)
    path('admin/loans/<int:loan_id>/rescore/', RescoreLoanView.as_view(), name='loan-rescore'),
]
