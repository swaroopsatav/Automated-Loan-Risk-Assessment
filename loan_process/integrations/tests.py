from datetime import timedelta

from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.utils.timezone import now

from integrations.admin import MockKYCAdmin, MockExperianReportAdmin
from integrations.forms import MockExperianReportForm, MockKYCRecordForm
from integrations.models import MockKYCRecord, MockExperianReport

class MockKYCRecordTests(TestCase):
    def setUp(self):
        self.mock_kyc_record = MockKYCRecord(
            user=None,  # Replace with an actual user instance for real tests
            pan_number="ABCDE1234F",
            aadhaar_last_4="1234",
            pan_verified=True,
            aadhaar_verified=True,
            verification_status="Verified"
        )
        self.admin = MockKYCAdmin(MockKYCRecord, AdminSite())

    def test_pretty_mock_response_empty(self):
        response = self.admin.pretty_mock_response(self.mock_kyc_record)
        self.assertEqual(response, "-")

class MockExperianReportTests(TestCase):
    def setUp(self):
        self.mock_report = MockExperianReport(
            user=None,  # Replace with an actual user instance for real tests
            loan_application=None,  # Replace with a loan application instance for real tests
            bureau_score=750,
            score_band="Good",
            total_accounts=5,
            overdue_accounts=0,
            dpd_max=0
        )
        self.admin = MockExperianReportAdmin(MockExperianReport, AdminSite())

    def test_pretty_mock_raw_report_empty(self):
        response = self.admin.pretty_mock_raw_report(self.mock_report)
        self.assertEqual(response, "-")


from django.test import TestCase
from django.apps import apps

class TestIntegrationsConfig(TestCase):
    def test_app_config(self):
        """
        Test that the IntegrationsConfig is correctly configured.
        """
        app_config = apps.get_app_config('integrations')  # <-- Django will handle it

        # Verify the default_auto_field is properly set
        self.assertEqual(app_config.default_auto_field, "django.db.models.BigAutoField")

        # Verify the name of the app
        self.assertEqual(app_config.name, "integrations")

        # Verify the verbose_name of the app
        self.assertEqual(app_config.verbose_name, "Integrations")


from django.test import TestCase
from integrations.forms import MockKYCRecordForm, MockExperianReportForm
from django.utils.timezone import now
from datetime import timedelta

class MockKYCRecordFormTests(TestCase):
    def setUp(self):
        self.valid_mock_response = '{"key": "value"}'
        self.invalid_json = 'invalid-json'
        self.valid_dob = "2000-01-01"

    def test_valid_mock_response(self):
        """Test that a valid JSON mock_response is accepted."""
        # Create test user
        user = CustomUser.objects.create(username="testuser_kyc")

        form = MockKYCRecordForm(data={
            "mock_response": self.valid_mock_response,
            "dob": self.valid_dob,
            "user": user.id,
            "pan_number": "ABCDE1234F",
            "pan_holder_name": "Test User",
            "pan_verified": True,
            "aadhaar_last_4": "1234",
            "aadhaar_verified": True,
            "kyc_type": "full",
            "verification_status": "verified",
            "verification_source": "mock_provider"
        })
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
        self.assertTrue(form.is_valid())

    def test_invalid_mock_response(self):
        """Test that an invalid JSON mock_response is rejected."""
        form = MockKYCRecordForm(data={
            "mock_response": self.invalid_json,
            "dob": self.valid_dob,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("mock_response", form.errors)

    def test_dob_in_future(self):
        """Test that a DOB in the future is rejected."""
        future_date = (now() + timedelta(days=1)).date()
        form = MockKYCRecordForm(data={
            "mock_response": self.valid_mock_response,
            "dob": future_date,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("dob", form.errors)

class MockExperianReportFormTests(TestCase):
    def setUp(self):
        self.valid_mock_raw_report = '{"key": "value"}'
        self.valid_tradelines = '[{"account": "1234"}]'
        self.valid_enquiries = '[{"inquiry": "5678"}]'
        self.invalid_json = 'invalid-json'

    def test_valid_mock_raw_report(self):
        """Test that a valid JSON mock_raw_report is accepted."""
        # Create test user and loan application
        user = CustomUser.objects.create(username="testuser_form")
        loan_application = LoanApplication.objects.create(user=user, amount_requested=50000)

        form = MockExperianReportForm(data={
            "mock_raw_report": self.valid_mock_raw_report,
            "tradelines": '[]',
            "enquiries": '[]',
            "user": user.id,
            "loan_application": loan_application.id,
            "bureau_score": 750,
            "score_band": "good",
            "report_status": "completed",
            "total_accounts": 5,
            "active_accounts": 4,
            "overdue_accounts": 1,
            "dpd_max": 0,
            "credit_utilization_pct": 45.0,
            "emi_to_income_ratio": 0.3
        })
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
        self.assertTrue(form.is_valid())

    def test_invalid_mock_raw_report(self):
        """Test that an invalid JSON mock_raw_report is rejected."""
        form = MockExperianReportForm(data={
            "mock_raw_report": self.invalid_json,
            "tradelines": '[]',
            "enquiries": '[]',
        })
        self.assertFalse(form.is_valid())
        self.assertIn("mock_raw_report", form.errors)

    def test_valid_tradelines_and_enquiries(self):
        """Test that valid JSON for tradelines and enquiries is accepted."""
        # Create test user and loan application
        user = CustomUser.objects.create(username="testuser_form2")
        loan_application = LoanApplication.objects.create(user=user, amount_requested=50000)

        form = MockExperianReportForm(data={
            "mock_raw_report": self.valid_mock_raw_report,
            "tradelines": self.valid_tradelines,
            "enquiries": self.valid_enquiries,
            "user": user.id,
            "loan_application": loan_application.id,
            "bureau_score": 750,
            "score_band": "good",
            "report_status": "completed",
            "total_accounts": 5,
            "active_accounts": 4,
            "overdue_accounts": 1,
            "dpd_max": 0,
            "credit_utilization_pct": 45.0,
            "emi_to_income_ratio": 0.3
        })
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
        self.assertTrue(form.is_valid())

    def test_invalid_tradelines(self):
        """Test that an invalid JSON tradelines field is rejected."""
        form = MockExperianReportForm(data={
            "mock_raw_report": self.valid_mock_raw_report,
            "tradelines": self.invalid_json,
            "enquiries": '[]',
        })
        self.assertFalse(form.is_valid())
        self.assertIn("tradelines", form.errors)

    def test_invalid_enquiries(self):
        """Test that an invalid JSON enquiries field is rejected."""
        form = MockExperianReportForm(data={
            "mock_raw_report": self.valid_mock_raw_report,
            "tradelines": '[]',
            "enquiries": self.invalid_json,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("enquiries", form.errors)


from django.test import TestCase
from integrations.models import MockKYCRecord, MockExperianReport
from users.models import CustomUser
from loanapplications.models import LoanApplication
from django.core.exceptions import ValidationError
from datetime import date

class MockKYCRecordTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser")
        self.mock_kyc = MockKYCRecord.objects.create(
            user=self.user,
            pan_number="ABCDE1234F",
            pan_holder_name="Test User",
            pan_verified=True,
            aadhaar_last_4="1234",
            aadhaar_verified=True,
            dob=date(2000, 1, 1),
            kyc_type="full",
            verification_status="verified",
            verification_source="mock_provider",
            mock_response={"status": "success"}
        )

    def test_string_representation(self):
        """
        Test the string representation of MockKYCRecord.
        """
        self.assertEqual(str(self.mock_kyc), f"Mock KYC: {self.user.username}")

    def test_invalid_aadhaar_last_4(self):
        """
        Test that an invalid Aadhaar last 4 digits raises validation error.
        """
        self.mock_kyc.aadhaar_last_4 = "123"  # Invalid length
        with self.assertRaises(ValidationError):
            self.mock_kyc.full_clean()

class MockExperianReportTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser")
        self.loan_application = LoanApplication.objects.create(user=self.user, amount_requested=50000)
        self.mock_report = MockExperianReport.objects.create(
            loan_application=self.loan_application,
            user=self.user,
            bureau_score=750,
            score_band="good",
            report_status="completed",
            total_accounts=5,
            active_accounts=4,
            overdue_accounts=1,
            dpd_max=0,
            credit_utilization_pct=45.0,
            emi_to_income_ratio=0.3,
            tradelines=[{"account": "1234"}],
            enquiries=[{"inquiry": "5678"}],
            mock_raw_report={"status": "success"}
        )

    def test_string_representation(self):
        """
        Test the string representation of MockExperianReport.
        """
        self.assertEqual(
            str(self.mock_report),
            f"Experian Report (Loan #{self.loan_application.id}) for {self.user.username}"
        )

    def test_invalid_active_accounts(self):
        """
        Test that active accounts cannot exceed total accounts.
        """
        self.mock_report.active_accounts = 6  # More than total accounts
        with self.assertRaises(ValidationError):
            self.mock_report.full_clean()

    def test_invalid_overdue_accounts(self):
        """
        Test that overdue accounts cannot exceed active accounts.
        """
        self.mock_report.overdue_accounts = 5  # More than active accounts
        with self.assertRaises(ValidationError):
            self.mock_report.full_clean()

from rest_framework.test import APITestCase
from integrations.serializers import MockKYCSerializer, MockExperianReportSerializer
from integrations.models import MockKYCRecord, MockExperianReport
from users.models import CustomUser
from loanapplications.models import LoanApplication
from datetime import date
from django.core.exceptions import ValidationError

class MockKYCSerializerTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser")
        self.mock_kyc = MockKYCRecord.objects.create(
            user=self.user,
            pan_number="ABCDE1234F",
            pan_holder_name="Test User",
            pan_verified=True,
            aadhaar_last_4="1234",
            aadhaar_verified=True,
            dob=date(2000, 1, 1),
            kyc_type="full",
            verification_status="verified",
            verification_source="mock_provider",
            mock_response={"status": "success"}
        )

    def test_serialization(self):
        """
        Test that the MockKYCRecord is serialized correctly.
        """
        serializer = MockKYCSerializer(self.mock_kyc)
        data = serializer.data
        self.assertEqual(data['user'], self.mock_kyc.user.id)
        self.assertEqual(data['pan_number'], self.mock_kyc.pan_number)
        self.assertEqual(data['verification_status'], self.mock_kyc.verification_status)

    def test_read_only_fields(self):
        """
        Test that all fields are read-only.
        """
        serializer = MockKYCSerializer(data={})
        self.assertEqual(serializer.Meta.read_only_fields, serializer.Meta.fields)

class MockExperianReportSerializerTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser")
        self.loan_application = LoanApplication.objects.create(user=self.user, amount_requested=50000)
        self.mock_report = MockExperianReport.objects.create(
            loan_application=self.loan_application,
            user=self.user,
            bureau_score=750,
            score_band="good",
            report_status="completed",
            total_accounts=5,
            active_accounts=4,
            overdue_accounts=1,
            dpd_max=0,
            credit_utilization_pct=45.0,
            emi_to_income_ratio=0.3,
            tradelines=[{"account": "1234"}],
            enquiries=[{"inquiry": "5678"}],
            mock_raw_report={"status": "success"}
        )

    def test_serialization(self):
        """
        Test that the MockExperianReport is serialized correctly.
        """
        serializer = MockExperianReportSerializer(self.mock_report)
        data = serializer.data
        self.assertEqual(data['loan_application'], self.mock_report.loan_application.id)
        self.assertEqual(data['bureau_score'], self.mock_report.bureau_score)
        self.assertEqual(data['score_band'], self.mock_report.score_band)

    def test_read_only_fields(self):
        """
        Test that all fields are read-only.
        """
        serializer = MockExperianReportSerializer(data={})
        self.assertEqual(serializer.Meta.read_only_fields, serializer.Meta.fields)

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from integrations.views import MyMockKYCView, MockExperianReportView, AllMockExperianReportsView

class TestUrls(SimpleTestCase):
    def test_my_mock_kyc_url(self):
        """
        Test that the 'my-mock-kyc' URL resolves to the correct view.
        """
        url = reverse('integrations:my-mock-kyc')
        self.assertEqual(resolve(url).func.view_class, MyMockKYCView)

    def test_mock_experian_report_url(self):
        """
        Test that the 'mock-experian-report' URL resolves to the correct view.
        """
        url = reverse('integrations:mock-experian-report', args=[1])  # Example loan_id = 1
        self.assertEqual(resolve(url).func.view_class, MockExperianReportView)

    def test_all_mock_reports_url(self):
        """
        Test that the 'all-mock-reports' URL resolves to the correct view.
        """
        url = reverse('integrations:all-mock-reports')
        self.assertEqual(resolve(url).func.view_class, AllMockExperianReportsView)

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import CustomUser
from loanapplications.models import LoanApplication
from integrations.models import MockKYCRecord, MockExperianReport
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token


class MyMockKYCViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password123")

        # First create a LoanApplication object for the user
        self.loan_application = LoanApplication.objects.create(
            user=self.user,
            amount_requested=50000
        )

        # Then create MockKYCRecord with that loan_application
        self.mock_kyc = MockKYCRecord.objects.create(
            user=self.user,
            pan_number="ABCDE1234F",
            pan_holder_name="Test User",
            pan_verified=True,
            aadhaar_last_4="1234",
            aadhaar_verified=True,
            dob="2000-01-01",
            kyc_type="full",
            verification_status="verified",
            verification_source="mock_provider",
            mock_response={"status": "success"}
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_kyc_record(self):
        """
        Test that the authenticated user can retrieve their KYC record.
        """
        response = self.client.get("/api/integrations/mock/kyc/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Expect 200 OK
        self.assertEqual(response.data["pan_number"], self.mock_kyc.pan_number)

    def test_kyc_record_not_found(self):
        """
        Test that a 404 is returned if the user has no KYC record.
        """
        # Ensure there's no KYC record for the user
        MockKYCRecord.objects.all().delete()

        # Perform the GET request
        response = self.client.get("/api/integrations/mock/kyc/")

        # Ensure the status code is 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Parse response as JSON
        response_data = {"detail": response.content.decode()}

        # Check that the response contains a 'detail' field
        self.assertIn("detail", response_data)


class MockExperianReportViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password123")
        self.other_user = CustomUser.objects.create_user(username="otheruser", password="password123",
                                                         email="otheruser@test.com")

        self.loan_application = LoanApplication.objects.create(user=self.user, amount_requested=50000)

        self.mock_report = MockExperianReport.objects.create(
            loan_application=self.loan_application,
            user=self.user,
            bureau_score=750,
            score_band="good",
            report_status="completed",
            total_accounts=5,
            active_accounts=4,
            overdue_accounts=1,
            dpd_max=0,
            credit_utilization_pct=45.0,
            emi_to_income_ratio=0.3,
            tradelines=[{"account": "1234"}],
            enquiries=[{"inquiry": "5678"}],
            mock_raw_report={"status": "success"}
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_mock_experian_report(self):
        """
        Test that the authenticated user can retrieve their mock Experian report.
        """
        response = self.client.get(f"/api/integrations/mock/experian/loan/{self.loan_application.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Expect 200 OK
        self.assertEqual(response.data["bureau_score"], self.mock_report.bureau_score)

    def test_permission_denied_for_other_user(self):
        """
        Test that another user cannot access someone else's mock Experian report.
        """
        self.client = APIClient()
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(f"/api/integrations/mock/experian/loan/{self.loan_application.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_report_not_found(self):
        """
        Test that a 404 is returned if the mock Experian report does not exist.
        """
        MockExperianReport.objects.all().delete()  # Remove the report
        response = self.client.get(f"/api/integrations/mock/experian/loan/{self.loan_application.id}/")

        # Ensure the status code is 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AllMockExperianReportsViewTests(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_superuser(username="admin", password="password123")
        self.user = CustomUser.objects.create_user(username="testuser", password="password123",email="testuser@test.com")
        self.loan_application = LoanApplication.objects.create(user=self.user, amount_requested=50000)
        self.mock_report = MockExperianReport.objects.create(
            loan_application=self.loan_application,
            user=self.user,
            bureau_score=750,
            score_band="good",
            report_status="completed",
            total_accounts=5,
            active_accounts=4,
            overdue_accounts=1,
            dpd_max=0,
            credit_utilization_pct=45.0,
            emi_to_income_ratio=0.3,
            tradelines=[{"account": "1234"}],
            enquiries=[{"inquiry": "5678"}],
            mock_raw_report={"status": "success"}
        )
        self.client = APIClient()
        self.client.login(username="admin", password="password123")

    def test_list_all_mock_reports(self):
        """
        Test that an admin user can list all mock Experian reports.
        """
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)  # Log in as admin!

        response = self.client.get("/api/integrations/mock/experian/reports/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Expect 200 OK
        self.assertEqual(len(response.data), 1)  # Verify that there is 1 report in the response

    def test_filter_mock_reports_by_user(self):
        """
        Test that mock reports can be filtered by user ID.
        """
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)  # Log in as admin!

        response = self.client.get(f"/api/integrations/mock/experian/reports/?user_id={self.user.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Expect 200 OK
        self.assertEqual(len(response.data), 1)  # Verify that there is 1 report in the response
        self.assertEqual(response.data[0]["user"], self.user.id)

    def test_non_admin_access_denied(self):
        """
        Test that a non-admin user cannot access the list of mock Experian reports.
        """
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # Log in as regular user
        response = self.client.get("/api/integrations/mock/experian/reports/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


from django.test import TestCase
from unittest.mock import patch, MagicMock
from integrations.management.commands.generate_mock_data import Command
from users.models import CustomUser
from loanapplications.models import LoanApplication
from integrations.models import MockKYCRecord, MockExperianReport


class GenerateMockDataTests(TestCase):

    @patch('integrations.management.commands.generate_mock_data.MockKYCRecord.objects.create')
    @patch('integrations.management.commands.generate_mock_data.MockExperianReport.objects.create')
    @patch('integrations.management.commands.generate_mock_data.CustomUser.objects.exclude')
    @patch('integrations.management.commands.generate_mock_data.LoanApplication.objects.exclude')
    def test_handle_generate_mock_data(self, mock_exclude_loans, mock_exclude_users, mock_create_experian,
                                       mock_create_kyc):
        # Mock eligible users and loans
        mock_user = MagicMock(id=1, username="testuser")
        mock_loan = MagicMock(id=1)

        mock_exclude_users.return_value = [mock_user]
        mock_exclude_loans.return_value = [mock_loan]

        mock_create_kyc.return_value = MagicMock(verification_status="verified")
        mock_create_experian.return_value = MagicMock(bureau_score=750)

        # Create the command instance
        command = Command()
        options = {"count": 1, "verbose": True}

        # Call the handle method
        command.handle(**options)

        # Assertions
        mock_exclude_users.assert_called_once()
        mock_exclude_loans.assert_called_once()
        mock_create_kyc.assert_called_once()
        mock_create_experian.assert_called_once()
