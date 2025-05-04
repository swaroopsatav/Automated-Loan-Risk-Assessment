from django.test import TestCase
from django.contrib.auth import get_user_model
from loanapplications.models import LoanApplication, LoanDocument
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class LoanApplicationCompletionPercentageTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create a loan application with minimal data
        self.loan = LoanApplication.objects.create(
            user=self.user,
            amount_requested=10000,
            purpose='Test purpose',
            term_months=12,
            monthly_income=5000,
            existing_loans=False,
            status='pending'
        )
    
    def test_initial_completion_percentage(self):
        """Test the initial completion percentage with minimal data."""
        # With just the required fields filled but no documents and pending status
        # Expected: 50% for fields + 0% for documents + 2.5% for status = 52.5%
        self.assertEqual(self.loan.completion_percentage(), 52.5)
    
    def test_with_documents(self):
        """Test completion percentage after adding documents."""
        # Add two documents
        for doc_type in ['bank_statement', 'id_proof']:
            LoanDocument.objects.create(
                loan=self.loan,
                document_type=doc_type,
                file=SimpleUploadedFile(f"{doc_type}.txt", b"test content")
            )
        
        # Recalculate: 50% for fields + 20% for documents (2/4) + 2.5% for status = 72.5%
        self.assertEqual(self.loan.completion_percentage(), 72.5)
    
    def test_with_status_change(self):
        """Test completion percentage after status change."""
        # Change status to under_review
        self.loan.status = 'under_review'
        self.loan.save()
        
        # Recalculate: 50% for fields + 0% for documents + 5% for status = 55%
        self.assertEqual(self.loan.completion_percentage(), 55.0)
    
    def test_complete_application(self):
        """Test completion percentage for a complete application."""
        # Add all documents
        for doc_type in LoanApplication.REQUIRED_DOCUMENT_TYPES:
            LoanDocument.objects.create(
                loan=self.loan,
                document_type=doc_type,
                file=SimpleUploadedFile(f"{doc_type}.txt", b"test content")
            )
        
        # Set credit score
        self.loan.credit_score_records = 750
        
        # Change status to approved
        self.loan.status = 'approved'
        self.loan.save()
        
        # Recalculate: 50% for fields + 40% for documents + 10% for status = 100%
        self.assertEqual(self.loan.completion_percentage(), 100.0)