from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from .models import MockKYCRecord, MockExperianReport, LoanApplication
from .serializers import MockKYCSerializer, MockExperianReportSerializer


# --- Get mock KYC for the authenticated user ---
class MyMockKYCView(generics.RetrieveAPIView):
    """
    API view to retrieve the mock KYC record for the authenticated user.
    """
    serializer_class = MockKYCSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Returns the MockKYCRecord for the authenticated user.
        Raises NotFound if no record exists.
        """
        try:
            return MockKYCRecord.objects.get(user=self.request.user)
        except MockKYCRecord.DoesNotExist:
            raise NotFound(detail="Mock KYC record not found for the user.")


# --- Get mock Experian report by loan ID ---
class MockExperianReportView(generics.RetrieveAPIView):
    """
    API view to retrieve the mock Experian report for a specific loan application.
    Only accessible by the user who owns the loan application.
    """
    serializer_class = MockExperianReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieves a specific MockExperianReport by loan ID.
        Raises NotFound if no report exists for the given loan ID.
        Raises PermissionDenied if user does not own the loan application.
        """
        loan_id = self.kwargs.get('loan_id')
        if not loan_id:
            raise NotFound(detail="Loan ID is required.")

        try:
            loan = LoanApplication.objects.get(id=loan_id)
            if loan.user != self.request.user:
                raise PermissionDenied(detail="You do not have permission to access this report.")

            return MockExperianReport.objects.get(
                loan_application=loan,
                user=self.request.user
            )
        except LoanApplication.DoesNotExist:
            raise NotFound(detail=f"Loan application with ID {loan_id} not found.")
        except MockExperianReport.DoesNotExist:
            raise NotFound(detail=f"No mock Experian report found for loan ID {loan_id}.")


# --- Admin-only: List all mock Experian reports --- 
class AllMockExperianReportsView(generics.ListAPIView):
    """
    API view to list all mock Experian reports.
    Accessible only by admin users.
    """
    serializer_class = MockExperianReportSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        """
        Returns queryset of all MockExperianReports ordered by creation date.
        Allows optional filtering by user_id query parameter.
        """
        queryset = MockExperianReport.objects.all().order_by('-created_at')
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset
