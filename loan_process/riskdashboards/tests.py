from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.admin.sites import site

from users.models import CustomUser
from .models import RiskSnapshot, RiskTrend, ModelPerformanceLog
from .admin import RiskSnapshotAdmin, RiskTrendAdmin, ModelPerformanceLogAdmin


class TestAdminSiteRegistrations(TestCase):
    def test_risksnapshot_registered(self):
        self.assertIn(RiskSnapshot, site._registry)
        self.assertIsInstance(site._registry[RiskSnapshot], RiskSnapshotAdmin)

    def test_risktrend_registered(self):
        self.assertIn(RiskTrend, site._registry)
        self.assertIsInstance(site._registry[RiskTrend], RiskTrendAdmin)

    def test_modelperformancelog_registered(self):
        self.assertIn(ModelPerformanceLog, site._registry)
        self.assertIsInstance(site._registry[ModelPerformanceLog], ModelPerformanceLogAdmin)


from django.test import TestCase
from django.apps import apps
from riskdashboards.apps import RiskdashboardsConfig


class TestRiskdashboardsConfig(TestCase):
    def test_apps_config(self):
        # Assert that the AppConfig is correctly registered
        self.assertEqual(RiskdashboardsConfig.name, "riskdashboards")
        self.assertEqual(RiskdashboardsConfig.verbose_name, "Risk Dashboards")

    def test_apps_registry(self):
        # Assert that the app is correctly registered in the Django app registry
        app_config = apps.get_app_config("riskdashboards")
        self.assertIsInstance(app_config, RiskdashboardsConfig)


from django.test import TestCase
from riskdashboards.forms import (RiskSnapshotForm, RiskTrendForm, ModelPerformanceLogForm)
from riskdashboards.models import RiskSnapshot, RiskTrend, ModelPerformanceLog


class TestRiskSnapshotForm(TestCase):
    def test_form_fields(self):
        form = RiskSnapshotForm()
        expected_fields = {field.name for field in RiskSnapshot._meta.fields
                           if field.name not in ['id', 'created_at']}
        self.assertEqual(set(form.fields.keys()), expected_fields)
        for field, widget in form.fields.items():
            self.assertEqual(widget.widget.attrs.get('readonly'), 'readonly')
            self.assertIn('form-control', widget.widget.attrs.get('class', ''))


class TestRiskTrendForm(TestCase):
    def test_form_fields(self):
        form = RiskTrendForm()
        self.assertEqual(
            set(form.fields.keys()),
            set(field.name for field in RiskTrend._meta.fields if field.name != 'id')
        )
        for field, widget in form.fields.items():
            self.assertEqual(widget.widget.attrs.get('readonly'), 'readonly')
            self.assertIn('form-control', widget.widget.attrs.get('class', ''))


class TestModelPerformanceLogForm(TestCase):
    def test_form_fields(self):
        form = ModelPerformanceLogForm()
        self.assertIn('notes', form.fields.keys())
        self.assertEqual(form.fields['notes'].widget.attrs.get('rows'), 3)
        self.assertIn('form-control', form.fields['notes'].widget.attrs.get('class', ''))

    def test_clean_metric_valid(self):
        form = ModelPerformanceLogForm(data={
            'model_version': '1.0',
            'accuracy': 0.95,
            'precision': 0.87,
            'recall': 0.92,
            'auc_score': 0.98,
            'f1_score': 0.90,
            'notes': 'Test Note'
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['accuracy'], 0.95)

    def test_clean_metric_invalid(self):
        form = ModelPerformanceLogForm(data={
            'model_version': '1.0',
            'accuracy': 1.5,  # Invalid value
            'precision': 0.87,
            'recall': 0.92,
            'auc_score': 0.98,
            'f1_score': 0.90,
            'notes': 'Test Note'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('accuracy', form.errors)
        self.assertEqual(
            form.errors['accuracy'][0],
            "accuracy must be between 0 and 1"
        )

from django.test import TestCase

from riskdashboards.models import RiskSnapshot, RiskTrend, ModelPerformanceLog
from riskdashboards.serializers import (
    RiskSnapshotSerializer,
    RiskTrendSerializer,
    ModelPerformanceLogSerializer,
)


class TestRiskSnapshotSerializer(TestCase):
    def test_valid_data(self):
        data = {
            "snapshot_date": "2025-04-01",
            "total_applications": 100,
            "avg_risk_score": 50.5,
            "high_risk_count": 30,
            "low_risk_count": 70,
            "approved_count": 40,
            "rejected_count": 40,
            "under_review_count": 20,
            "model_version": "xgboost_v1",
        }
        serializer = RiskSnapshotSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_avg_risk_score(self):
        data = {
            "snapshot_date": "2025-04-01",
            "total_applications": 100,
            "avg_risk_score": 150.0,  # Invalid value
            "high_risk_count": 30,
            "low_risk_count": 70,
            "approved_count": 40,
            "rejected_count": 40,
            "under_review_count": 20,
            "model_version": "xgboost_v1",
        }
        serializer = RiskSnapshotSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('avg_risk_score', serializer.errors)


class TestRiskTrendSerializer(TestCase):
    def test_valid_data(self):
        data = {
            "date": "2025-04-01",
            "avg_score": 75.5,
            "approval_rate": 60.0,
            "rejection_rate": 40.0,
            "model_version": "xgboost_v1",
        }
        serializer = RiskTrendSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_rejection_rate(self):
        data = {
            "date": "2025-04-01",
            "avg_score": 75.5,
            "approval_rate": 60.0,
            "rejection_rate": 120.0,  # Invalid value
            "model_version": "xgboost_v1",
        }
        serializer = RiskTrendSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('rejection_rate', serializer.errors)


class TestModelPerformanceLogSerializer(TestCase):
    def test_valid_data(self):
        data = {
            "model_version": "xgboost_v1",
            "accuracy": 0.95,
            "precision": 0.87,
            "recall": 0.92,
            "auc_score": 0.98,
            "f1_score": 0.90,
            "notes": "Good performance",
        }
        serializer = ModelPerformanceLogSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_accuracy(self):
        data = {
            "model_version": "xgboost_v1",
            "accuracy": 1.6,  # Invalid value
            "precision": 0.87,
            "recall": 0.92,
            "auc_score": 0.98,
            "f1_score": 0.90,
            "notes": "Good performance",
        }
        serializer = ModelPerformanceLogSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('accuracy', serializer.errors)

from django.test import TestCase
from datetime import date
from .models import RiskSnapshot, RiskTrend, ModelPerformanceLog

class RiskSnapshotModelTest(TestCase):
    def test_valid_risk_snapshot(self):
        snapshot = RiskSnapshot(
            snapshot_date=date.today(),
            total_applications=100,
            avg_risk_score=50.0,
            high_risk_count=30,
            low_risk_count=70,
            approved_count=40,
            rejected_count=20,
            under_review_count=40,
            model_version='xgboost_v1'
        )
        snapshot.full_clean()  # Should not raise any validation error
        snapshot.save()
        self.assertEqual(RiskSnapshot.objects.count(), 1)

    def test_total_applications_mismatch(self):
        snapshot = RiskSnapshot(
            snapshot_date=date.today(),
            total_applications=100,
            avg_risk_score=50.0,
            high_risk_count=30,
            low_risk_count=70,
            approved_count=40,
            rejected_count=20,
            under_review_count=50,  # Mismatch here
            model_version='xgboost_v1'
        )
        with self.assertRaises(ValidationError):
            snapshot.full_clean()

    def test_risk_count_exceeds_total(self):
        snapshot = RiskSnapshot(
            snapshot_date=date.today(),
            total_applications=60,
            avg_risk_score=50.0,
            high_risk_count=60,  # Exceeds total applications
            low_risk_count=40,
            approved_count=20,
            rejected_count=10,
            under_review_count=30,
            model_version='xgboost_v1'
        )
        with self.assertRaises(ValidationError):
            snapshot.full_clean()

class RiskTrendModelTest(TestCase):
    def test_valid_risk_trend(self):
        trend = RiskTrend(
            date=date.today(),
            avg_score=50.0,
            approval_rate=60.0,
            rejection_rate=30.0,
            model_version='xgboost_v1'
        )
        trend.full_clean()  # Should not raise any validation error
        trend.save()
        self.assertEqual(RiskTrend.objects.count(), 1)

    def test_approval_rejection_rate_exceeds_100(self):
        trend = RiskTrend(
            date=date.today(),
            avg_score=50.0,
            approval_rate=70.0,
            rejection_rate=40.0,  # Sum exceeds 100%
            model_version='xgboost_v1'
        )
        with self.assertRaises(ValidationError):
            trend.full_clean()

class ModelPerformanceLogModelTest(TestCase):
    def test_valid_model_performance_log(self):
        log = ModelPerformanceLog(
            model_version='xgboost_v1',
            accuracy=0.85,
            precision=0.8,
            recall=0.75,
            auc_score=0.9,
            f1_score=0.78,
            notes='Test log entry'
        )
        log.full_clean()  # Should not raise any validation error
        log.save()
        self.assertEqual(ModelPerformanceLog.objects.count(), 1)

    def test_invalid_accuracy(self):
        log = ModelPerformanceLog(
            model_version='xgboost_v1',
            accuracy=1.1,  # Invalid, must be between 0 and 1
            precision=0.8,
            recall=0.75,
            auc_score=0.9,
            f1_score=0.78,
            notes='Test log entry'
        )
        with self.assertRaises(ValidationError):
            log.full_clean()

    def test_invalid_auc_score(self):
        log = ModelPerformanceLog(
            model_version='xgboost_v1',
            accuracy=0.85,
            precision=0.8,
            recall=0.75,
            auc_score=1.2,  # Invalid, must be between 0 and 1
            f1_score=0.78,
            notes='Test log entry'
        )
        with self.assertRaises(ValidationError):
            log.full_clean()

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from riskdashboards.views import (
    RiskSnapshotListView,
    RiskTrendListView,
    ModelPerformanceLogListView,
    ModelPerformanceLogCreateView,
)

class TestUrls(SimpleTestCase):
    def test_snapshots_url_is_resolved(self):
        url = reverse('riskdashboards:snapshots')
        self.assertEqual(resolve(url).func.view_class, RiskSnapshotListView)

    def test_trends_url_is_resolved(self):
        url = reverse('riskdashboards:trends')
        self.assertEqual(resolve(url).func.view_class, RiskTrendListView)

    def test_model_list_url_is_resolved(self):
        url = reverse('riskdashboards:model-list')
        self.assertEqual(resolve(url).func.view_class, ModelPerformanceLogListView)

    def test_model_create_url_is_resolved(self):
        url = reverse('riskdashboards:model-create')
        self.assertEqual(resolve(url).func.view_class, ModelPerformanceLogCreateView)

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser
from riskdashboards.models import RiskSnapshot, RiskTrend, ModelPerformanceLog


class TestRiskSnapshotListView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        RiskSnapshot.objects.create(
            snapshot_date="2025-04-01", 
            total_applications=100, 
            avg_risk_score=50.0,
            high_risk_count=30,
            low_risk_count=70,
            approved_count=40,
            rejected_count=20,
            under_review_count=40,
            model_version='xgboost_v1'
        )

    def test_get_snapshots(self):
        response = self.client.get("/api/risk/snapshots/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)



class TestRiskTrendListView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        RiskTrend.objects.create(
            date="2025-04-01", 
            avg_score=75.0, 
            approval_rate=60.0, 
            rejection_rate=40.0,
            model_version='xgboost_v1'
        )

    def test_get_trends(self):
        response = self.client.get("/api/risk/trends/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)



class TestModelPerformanceLogListView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        ModelPerformanceLog.objects.create(
            model_version="v1", 
            accuracy=0.95, 
            precision=0.90, 
            recall=0.85, 
            auc_score=0.92,
            f1_score=0.88
        )

    def test_get_model_logs(self):
        response = self.client.get("/api/risk/models/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)



class TestModelPerformanceLogCreateView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = CustomUser.objects.create_superuser(username="admin", password="password")
        self.client.force_authenticate(user=self.admin_user)

    def test_create_model_log(self):
        # Get the initial count of ModelPerformanceLog objects
        initial_count = ModelPerformanceLog.objects.count()

        data = {
            "model_version": "v1",
            "accuracy": 0.95,
            "precision": 0.90,
            "recall": 0.85,
            "auc_score": 0.92,
            "f1_score": 0.88,
            "notes": "Test log"
        }
        response = self.client.post("/api/risk/models/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that one new object was created
        self.assertEqual(ModelPerformanceLog.objects.count(), initial_count + 1)

    def test_create_model_log_invalid(self):
        data = {
            "model_version": "v1",
            "accuracy": 1.5,  # Invalid value
            "precision": 0.90,
            "recall": 0.85,
            "auc_score": 0.92,
            "f1_score": 0.88,
            "notes": "Test log"
        }
        response = self.client.post("/api/risk/models/create/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth import get_user_model
from loanapplications.models import LoanApplication
from integrations.models import MockExperianReport
from pathlib import Path
import json
import os

CustomUser = get_user_model()

class TestCustomerFinancialHistoryCommand(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="password",
            credit_score=720,
            annual_income=60000,
            employment_status="Employed",
        )

        # Create loan applications for the user
        self.loan1 = LoanApplication.objects.create(
            user=self.user,
            amount_requested=5000,
            status="Approved",
            ai_decision="Approved",
            risk_score=50,
            submitted_at="2025-04-01",
        )
        self.loan2 = LoanApplication.objects.create(
            user=self.user,
            amount_requested=10000,
            status="Rejected",
            ai_decision="Rejected",
            risk_score=80,
            submitted_at="2025-04-15",
        )

        # Create a mock Experian report for the most recent loan
        self.experian_report = MockExperianReport.objects.create(
            user=self.user,
            loan_application=self.loan1,
            dpd_max=3,
            emi_to_income_ratio=0.3,
            credit_utilization_pct=40,
            total_accounts=5,
            bureau_score=450,
            active_accounts=3,
            overdue_accounts=1,
        )

        # Directory to save the report
        self.output_dir = "test_reports"
        Path(self.output_dir).mkdir(exist_ok=True)

    def tearDown(self):
        # Cleanup any files or directories created during the test
        if os.path.exists(self.output_dir):
            for file in os.listdir(self.output_dir):
                file_path = os.path.join(self.output_dir, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            os.rmdir(self.output_dir)

    def test_generate_report(self):
        # Call the management command
        call_command(
            "customer_financial_history",
            user_id=self.user.id,
            output_dir=self.output_dir,
        )

        # Check if the report file is created
        report_filename = os.path.join(self.output_dir, f"user_{self.user.id}_financial_report.json")
        self.assertTrue(os.path.exists(report_filename))

        # Validate the contents of the report
        with open(report_filename, "r") as f:
            report = json.load(f)

        self.assertEqual(report["user"]["username"], self.user.username)
        self.assertEqual(report["user"]["credit_score"], 720)
        self.assertEqual(report["user"]["annual_income"], 60000)
        self.assertEqual(report["user"]["employment_status"], "Employed")
        self.assertEqual(len(report["loan_history"]), 2)
        self.assertEqual(report["experian"]["dpd_max"], 3)
        self.assertEqual(report["experian"]["emi_to_income_ratio"], 0.3)
        self.assertEqual(report["experian"]["credit_utilization_pct"], 40.0)
        self.assertEqual(report["experian"]["total_accounts"], 5)

    def test_user_not_found(self):
        # Call the command with a non-existent user ID
        with self.assertLogs(level="ERROR") as log:
            call_command(
                "customer_financial_history",
                user_id=999,  # Non-existent user
                output_dir=self.output_dir,
            )
        # Check if any log message contains the expected text
        self.assertTrue(any("User with ID 999 does not exist." in msg for msg in log.output))

    def test_no_loans_for_user(self):
        # Create a new user with no loans
        new_user = CustomUser.objects.create_user(username="newuser", password="password",email="newuser@test.com")

        # Call the command for the new user
        with self.assertLogs(level="WARNING") as log:
            call_command(
                "customer_financial_history",
                user_id=new_user.id,
                output_dir=self.output_dir,
            )
        # Check if any log message contains the expected text
        self.assertTrue(any(f"No loan applications found for user {new_user.id}" in msg for msg in log.output))

    def test_no_experian_report(self):
        # Remove the Experian report for the loan
        self.experian_report.delete()

        # Call the command
        with self.assertLogs(level="WARNING") as log:
            call_command(
                "customer_financial_history",
                user_id=self.user.id,
                output_dir=self.output_dir,
            )
        # Check if any log message contains the expected text
        self.assertTrue(any("No mock Experian report found for this user." in msg for msg in log.output))
