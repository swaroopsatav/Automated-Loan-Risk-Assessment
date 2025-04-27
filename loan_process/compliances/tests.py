from django.test import TestCase
from django.contrib.admin.sites import site
from .models import ComplianceCheck, ComplianceAuditTrail
from .admin import ComplianceCheckAdmin, ComplianceAuditTrailAdmin

class AdminSiteTests(TestCase):

    def test_compliance_check_admin_registered(self):
        self.assertIn(ComplianceCheck, site._registry)
        self.assertIsInstance(site._registry[ComplianceCheck], ComplianceCheckAdmin)

    def test_compliance_audit_trail_admin_registered(self):
        self.assertIn(ComplianceAuditTrail, site._registry)
        self.assertIsInstance(site._registry[ComplianceAuditTrail], ComplianceAuditTrailAdmin)

    def test_compliance_check_list_display(self):
        admin_instance = site._registry[ComplianceCheck]
        self.assertEqual(admin_instance.list_display, (
            'loan_application', 'check_type', 'is_compliant',
            'user', 'created_at',
        ))

    def test_compliance_audit_trail_permissions(self):
        admin_instance = site._registry[ComplianceAuditTrail]
        self.assertFalse(admin_instance.has_add_permission(None))
        self.assertFalse(admin_instance.has_change_permission(None))
        self.assertFalse(admin_instance.has_delete_permission(None))


from django.apps import apps
from django.test import TestCase

class AppsConfigTests(TestCase):

    def test_compliances_config(self):
        app_config = apps.get_app_config("compliances")
        self.assertEqual(app_config.name, "compliances")
        self.assertEqual(app_config.verbose_name, "Compliances")

from django.test import TestCase
from django.utils.timezone import now
from .forms import ComplianceCheckForm, ComplianceAuditTrailForm
from .models import ComplianceCheck, ComplianceAuditTrail
from django.contrib.auth.models import User

class ComplianceFormsTest(TestCase):

    def setUp(self):
        # Create a sample user
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Create a sample loan application (if needed)
        self.loan_application = ComplianceCheck.objects.create(
            loan_application="12345",
            check_type="Type A",
            is_compliant="pending",
            user=self.user
        )

    def test_compliance_check_form_validation(self):
        # Test case with no user when status is not 'pending'
        form_data = {
            "check_type": "Type A",
            "is_compliant": "approved",
            "check_notes": "All good."
        }
        form = ComplianceCheckForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["__all__"][0],
            "A user must be assigned when marking compliance status."
        )

        # Test case with a user
        form_data["user"] = self.user.id
        form = ComplianceCheckForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_compliance_audit_trail_form_readonly(self):
        # Create a sample audit trail instance
        audit_trail = ComplianceAuditTrail.objects.create(
            actor=self.user,
            loan_application=self.loan_application,
            action="Test Action",
            timestamp=now(),
            notes="Sample note"
        )

        # Test form initialization
        form = ComplianceAuditTrailForm(instance=audit_trail)
        for field in form.fields.values():
            self.assertTrue(field.disabled)


from django.test import TestCase
from django.utils.timezone import now
from users.models import CustomUser
from loanapplications.models import LoanApplication
from .models import ComplianceCheck, ComplianceAuditTrail


class ModelsTest(TestCase):

    def setUp(self):
        # Create a sample user
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass")

        # Create a sample loan application
        self.loan_application = LoanApplication.objects.create(
            applicant_name="John Doe",
            loan_amount=5000
        )

    def test_compliance_check_creation(self):
        compliance_check = ComplianceCheck.objects.create(
            user=self.user,
            loan_application=self.loan_application,
            check_type="kyc",
            status="pending",
            is_compliant=False
        )
        self.assertEqual(compliance_check.status, "pending")
        self.assertEqual(str(compliance_check), "KYC Verification for Loan #1 - pending")

    def test_compliance_audit_trail_creation(self):
        audit_trail = ComplianceAuditTrail.objects.create(
            actor=self.user,
            loan_application=self.loan_application,
            action="approved",
            notes="Verified and approved."
        )
        self.assertEqual(audit_trail.action, "approved")
        self.assertEqual(str(audit_trail), "testuser - Approved - Loan #1")


from django.test import TestCase
from rest_framework.exceptions import ValidationError
from users.models import CustomUser
from loanapplications.models import LoanApplication
from .models import ComplianceCheck, ComplianceAuditTrail
from .serializers import (
    ComplianceCheckSerializer,
    ComplianceCheckUpdateSerializer,
    ComplianceAuditTrailSerializer
)


class SerializersTest(TestCase):

    def setUp(self):
        # Create a sample user
        self.user = CustomUser.objects.create_user(username="testuser", password="testpass")

        # Create a sample loan application
        self.loan_application = LoanApplication.objects.create(
            applicant_name="John Doe",
            loan_amount=5000
        )

        # Create a sample ComplianceCheck
        self.compliance_check = ComplianceCheck.objects.create(
            user=self.user,
            loan_application=self.loan_application,
            check_type="kyc",
            status="pending"
        )

        # Create a sample ComplianceAuditTrail
        self.audit_trail = ComplianceAuditTrail.objects.create(
            actor=self.user,
            loan_application=self.loan_application,
            action="approved",
            notes="Verified and approved."
        )

    def test_compliance_check_serializer(self):
        serializer = ComplianceCheckSerializer(instance=self.compliance_check)
        self.assertEqual(serializer.data['loan_id'], self.loan_application.id)
        self.assertEqual(serializer.data['check_type_display'], "KYC Verification")
        self.assertEqual(serializer.data['status_display'], "Pending")

    def test_compliance_check_update_serializer(self):
        update_data = {
            "status": "passed",
            "review_notes": "Everything is fine.",
            "reviewed_at": "2025-04-27T10:00:00Z"
        }
        serializer = ComplianceCheckUpdateSerializer(instance=self.compliance_check, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(self.compliance_check.status, "passed")

        # Test invalid status
        invalid_data = {"status": "invalid_status"}
        serializer = ComplianceCheckUpdateSerializer(instance=self.compliance_check, data=invalid_data, partial=True)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_compliance_audit_trail_serializer(self):
        serializer = ComplianceAuditTrailSerializer(instance=self.audit_trail)
        self.assertEqual(serializer.data['actor'], str(self.user))
        self.assertEqual(serializer.data['loan_id'], self.loan_application.id)
        self.assertEqual(serializer.data['action_display'], "Approved")

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import (
    ComplianceCheckListView,
    ComplianceCheckUpdateView,
    ComplianceAuditTrailListView,
)

class TestUrls(SimpleTestCase):

    def test_loan_compliance_checks_url(self):
        url = reverse('compliances:loan-compliance-checks', args=[1])
        self.assertEqual(resolve(url).func.view_class, ComplianceCheckListView)

    def test_update_compliance_check_url(self):
        url = reverse('compliances:update-compliance-check', args=[1])
        self.assertEqual(resolve(url).func.view_class, ComplianceCheckUpdateView)

    def test_compliance_audit_trail_url(self):
        url = reverse('compliances:compliance-audit-trail')
        self.assertEqual(resolve(url).func.view_class, ComplianceAuditTrailListView)

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser
from loanapplications.models import LoanApplication
from .models import ComplianceCheck, ComplianceAuditTrail

class ComplianceViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create admin and regular users
        self.admin_user = CustomUser.objects.create_superuser(username="admin", password="adminpass")
        self.regular_user = CustomUser.objects.create_user(username="user", password="userpass")

        # Create a loan application
        self.loan_application = LoanApplication.objects.create(
            applicant_name="John Doe",
            loan_amount=5000
        )

        # Create a compliance check
        self.compliance_check = ComplianceCheck.objects.create(
            user=self.regular_user,
            loan_application=self.loan_application,
            check_type="kyc",
            status="pending"
        )

        # Create an audit trail entry
        self.audit_trail = ComplianceAuditTrail.objects.create(
            actor=self.admin_user,
            loan_application=self.loan_application,
            action="approved",
            notes="Compliance approved."
        )

    def test_compliance_check_list_view(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(f'/loan/{self.loan_application.id}/checks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_compliance_check_update_view(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(f'/checks/{self.compliance_check.id}/', {"status": "passed"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.compliance_check.refresh_from_db()
        self.assertEqual(self.compliance_check.status, "passed")

    def test_compliance_audit_trail_list_view(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/audit-trail/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_permissions(self):
        # Test access denied for non-admin users on admin-only views
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/audit-trail/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


from django.test import TestCase
from django.core.management import call_command
from io import StringIO
from users.models import CustomUser
from loanapplications.models import LoanApplication
from compliances.models import ComplianceCheck


class RunComplianceChecksTest(TestCase):

    def setUp(self):
        # Create a sample user
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpass",
            is_kyc_verified=False,  # KYC not verified
            id_proof=None,
            address_proof=None,
            income_proof=None
        )

        # Create a loan application
        self.loan_application = LoanApplication.objects.create(
            applicant_name="John Doe",
            loan_amount=5000,
            user=self.user
        )

    def test_command_output_without_update(self):
        out = StringIO()
        call_command('run_compliance_checks', '--limit', '1', stdout=out)
        self.assertIn("⚠️ No records were updated", out.getvalue())
        self.assertIn("KYC not verified", out.getvalue())
        self.assertIn("Missing documents", out.getvalue())

    def test_command_output_with_update(self):
        out = StringIO()
        call_command('run_compliance_checks', '--update', '--limit', '1', stdout=out)
        self.assertIn("✅ Checked", out.getvalue())
        self.assertTrue(ComplianceCheck.objects.filter(loan_application=self.loan_application).exists())

    def test_compliance_check_creation(self):
        call_command('run_compliance_checks', '--update', '--limit', '1')
        compliance_check = ComplianceCheck.objects.get(loan_application=self.loan_application)
        self.assertFalse(compliance_check.is_compliant)
        self.assertIn("KYC not verified", compliance_check.check_notes)