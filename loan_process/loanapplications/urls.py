from django.urls import path
from .views import (
    LoanApplicationCreateView,
    UserLoanListView,
    UserLoanDetailView,
    LoanDocumentUploadView,
    AdminLoanListView,
    AdminLoanDetailView,
)

app_name = 'loans'

urlpatterns = [
    # --- User-facing ---
    path('submission/', LoanApplicationCreateView.as_view(), name='loan-submit'),
    path('', UserLoanListView.as_view(), name='my-loans'),
    path('<int:pk>/', UserLoanDetailView.as_view(), name='my-loan-detail'),
    path('<int:loan_id>/documents/', LoanDocumentUploadView.as_view(), name='loan-documents'),

    # --- Admin-only ---
    path('admin/', AdminLoanListView.as_view(), name='admin-loan-list'),
    path('admin/<int:pk>/', AdminLoanDetailView.as_view(), name='admin-loan-detail'),
]
